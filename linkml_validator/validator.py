import json
from typing import Dict, Generator, List, Set

from linkml_validator.models import ValidationReport
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.plugins.jsonschema_validation import JsonSchemaValidationPlugin


DEFAULT_PLUGINS = {
    "JsonschemaValidationPlugin": JsonSchemaValidationPlugin
}


class Validator:
    """
    Validator to validate data against a given schema.

    Args:
        schema: Path or URL to schema YAML
        plugins: A set of plugin classes to use for validation

    """

    def __init__(self, schema: str, plugins: List[Dict] = None) -> None:
        self.schema = schema
        self.plugins = set()
        if plugins:
            for plugin in plugins:
                plugin_class = plugin["plugin_class"]
                plugin_args = {}
                if "args" in plugin:
                    plugin_args = plugin["args"]
                if not issubclass(plugin_class, BasePlugin):
                    raise Exception(f"{plugin_class} must be a subclass of {BasePlugin}")
                instance = plugin_class(schema=self.schema, **plugin_args)
                self.plugins.add(instance)
        else:
            for plugin_class in DEFAULT_PLUGINS.values():
                instance = plugin_class(schema=self.schema)
                self.plugins.add(instance)

    def validate(
        self, obj: Dict, target_class: str, strict: bool = False, **kwargs
    ) -> ValidationReport:
        """
        Validate an object.

        Args:
            obj: The object to validate
            target_class: The type of object
            strict: Whether or not to perform strict validation, where any validation
                error stops the validation process. Defaults to `False`.
            kwargs: Any additional arguments

        Returns:
            ValidationReport: A validation report that summarizes the validation

        """
        validation_results = []
        valid = True
        if "exclude_object" in kwargs:
            exclude_object = kwargs["exclude_object"]
        else:
            exclude_object = False
        for plugin in self.plugins:
            validation_result = plugin.process(obj=obj, target_class=target_class, **kwargs)
            validation_results.append(validation_result)
            if not validation_result.valid:
                valid = False
                if strict:
                    break
        validation_report = ValidationReport(
            object=obj if not exclude_object else '<OMITTED>',
            type=target_class,
            valid=valid,
            validation_results=validation_results,
        )
        return validation_report

    def validate_file(
        self, filename: str, target_class: str = None, strict: bool = False
    ) -> Generator:
        """
        Validate all objects from a file.

        Args:
            filename: The filename
            target_class: The target class which all objects from the input JSON are an instance of
            strict: Whether or not to perform strict validation, where any validation
                error stops the validation process. Defaults to `False`.

        Returns:
            Generator: A generator that can be iterated to get a list of validation reports

        """
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                if target_class:
                    for obj in data:
                        report = self.validate(
                            obj=obj, target_class=target_class, strict=strict
                        )
                        yield report
                else:
                    raise Exception(f"target_class not defined. Cannot validate array of objects from {filename}.")
            else:
                for target_class, objects in data.items():
                    for obj in objects:
                        report = self.validate(
                            obj=obj, target_class=target_class, strict=strict
                        )
                        yield report
