import json
from typing import Dict, Generator, List, Set

from linkml_validator.models import ValidationReport
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.plugins.jsonschema_validation import JsonschemaValidationPlugin


DEFAULT_PLUGINS = {
    "JsonschemaValidationPlugin": JsonschemaValidationPlugin
}


class Validator:
    """
    Validator to validate data against a given schema.

    :param schema: Path or URL to schema YAML
    :param plugins: A set of plugin classes to use for validation

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
        self, obj: Dict, target_class: str, strict: bool = False
    ) -> ValidationReport:
        """
        Validate an object.

        :param obj: The object to validate
        :param target_class: The type of object
        :param strict: Whether or not to perform strict validation, where any validation
            error stops the validation process. Defaults to False.
        :return: A validation report that summarizes the validation

        """
        validation_results = []
        valid = True
        for plugin in self.plugins:
            validation_result = plugin.process(obj=obj, target_class=target_class)
            validation_results.append(validation_result)
            if not validation_result.valid:
                valid = False
                if strict:
                    break
        validation_report = ValidationReport(
            object=obj,
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

        :param filename: The filename
        :param target_class: The target class which all objects from the input JSON are an instance of
        :param strict: Whether or not to perform strict validation, where any validation
            error stops the validation process. Defaults to False.
        :return: A generator that can be iterated to get a list of validation reports

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
