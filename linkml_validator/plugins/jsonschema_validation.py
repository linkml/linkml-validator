from typing import List, Dict
import jsonschema
import copy
from linkml.utils.generator import Generator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml_validator.models import SeverityEnum, ValidationMessage, ValidationResult
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.utils import get_jsonschema, get_python_module, truncate
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.formatutils import camelcase


class JsonSchemaValidationPlugin(BasePlugin):
    """
    Plugin to perform JSONSchema validation.

    Args:
        schema: Path or URL to schema YAML
        jsonschema_generator: A generator to use for generating the JSONSchema
        generator_args: Arguments to instantiate the generator specified in `jsonschema_generator`
        kwargs: Additional arguments that are used to instantiate the plugin

    """

    NAME = "JsonSchemaValidationPlugin"

    def __init__(self, schema: str, jsonschema_generator: Generator = JsonSchemaGenerator, generator_args: Dict = None, **kwargs) -> None:
        super().__init__(schema)
        self.python_module = get_python_module(schema)
        self.jsonschema_generator = jsonschema_generator
        self.generator_args = generator_args if generator_args else {}
        self.jsonschema_obj_map = {}
        class_list = None
        if 'class_list' in kwargs:
            class_list = kwargs['class_list']
        self._generate_jsonschema(class_list=class_list)

    def _generate_jsonschema(self, class_list: List[str] = None) -> None:
        """
        Generate JSON Schema representation for all (or specific) classes
        in the schema.

        Args:
            class_list: A list of classes for which to generate JSONSchema

        """
        schemaview = SchemaView(self.schema)
        jsonschema_obj = None
        for class_name, class_def in schemaview.all_classes().items():
            if not class_def.mixin:
                formatted_name = camelcase(class_name)
                if class_list:
                    if formatted_name not in class_list:
                        continue
                if class_def.abstract:
                    # Skip abstract classes
                    continue
                py_target_class = self.python_module.__dict__[formatted_name]
                if formatted_name not in self.jsonschema_obj_map:
                    if not jsonschema_obj:
                        jsonschema_obj = get_jsonschema(
                            schema=self.schema,
                            py_target_class=py_target_class,
                            generator=self.jsonschema_generator,
                            **self.generator_args
                        )
                    target_jsonschema_obj = copy.deepcopy(jsonschema_obj)
                    target_jsonschema_obj['properties'] = jsonschema_obj["$defs"][formatted_name].get('properties', {})
                    target_jsonschema_obj['required'] = jsonschema_obj["$defs"][formatted_name].get('required', [])
                    self.jsonschema_obj_map[formatted_name] = target_jsonschema_obj

    def process(self, obj: Dict, **kwargs) -> ValidationResult:
        """
        Perform validation on an object.

        Args:
            obj: The object to validate
            kwargs: Additional arguments that are used for processing

        Returns:
            ValidationResult: A validation result that describes the outcome of validation

        """
        if "target_class" not in kwargs:
            raise Exception("Need `target_class` argument")
        if "truncate_message" in kwargs:
            truncate_message = kwargs["truncate_message"]
        else:
            truncate_message = False
        target_class = kwargs["target_class"]
        valid = True
        jsonschema_obj = self.jsonschema_obj_map[target_class]
        validator = jsonschema.Draft7Validator(jsonschema_obj)
        errors = [x for x in validator.iter_errors(obj)]
        result = ValidationResult(
            plugin_name=self.NAME,
            valid=valid,
            validation_messages=[]
        )
        if errors:
            valid = result.valid = False
            for error in errors:
                outer_validation_message = ValidationMessage(
                    severity=SeverityEnum.error.value,
                    message=truncate(error.message) if truncate_message else error.message,
                    field = ".".join(map(str, error.absolute_path)) if error.absolute_path else None,
                    value=error.instance if not isinstance(error.instance, dict) else None
                )
                for suberror in sorted(error.context, key=lambda e: e.schema_path):
                    inner_validation_message = ValidationMessage(
                        severity=SeverityEnum.error.value,
                        message=truncate(suberror.message) if truncate_message else suberror.message,
                        field = ".".join(map(str, suberror.absolute_path)) if suberror.absolute_path else outer_validation_message.field,
                        value=suberror.instance if not isinstance(suberror.instance, dict) else None
                    )
                    result.validation_messages.append(inner_validation_message)
                result.validation_messages.append(outer_validation_message)
        return result
