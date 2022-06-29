from typing import Dict
import jsonschema
from linkml.utils.generator import Generator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml_validator.models import SeverityEnum, ValidationMessage, ValidationResult
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.utils import get_jsonschema, get_python_module


class JsonSchemaValidationPlugin(BasePlugin):
    """
    Plugin to perform JSONSchema validation.

    Args:
        schema: Path or URL to schema YAML
        kwargs: Additional arguments that are used to instantiate the plugin

    """

    NAME = "JsonSchemaValidationPlugin"

    def __init__(self, schema: str, jsonschema_generator: Generator = JsonSchemaGenerator, **kwargs) -> None:
        super().__init__(schema)
        self.python_module = get_python_module(schema)
        self.jsonschema_generator = jsonschema_generator

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
        target_class = kwargs["target_class"]
        msg = None
        valid = True
        py_target_class = self.python_module.__dict__[target_class]
        jsonschema_obj = get_jsonschema(self.schema, py_target_class, generator=self.jsonschema_generator)
        validator = jsonschema.Draft7Validator(jsonschema_obj)
        errors = [x for x in validator.iter_errors(obj)]
        result = ValidationResult(
            plugin_name=self.NAME, valid=valid, validation_messages=[]
        )
        if errors:
            valid = result.valid = False
            for error in errors:
                msg = error.message
                field = ".".join(map(str, error.relative_path)) if error.relative_path else None
                validation_message = ValidationMessage(
                    severity=SeverityEnum.error.value,
                    message=msg,
                    field=field,
                    value=error.instance
                )
                result.validation_messages.append(validation_message)
        return result
