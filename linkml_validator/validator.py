import json
from typing import Dict, List, Set

from linkml_validator.models import ValidationReport
from linkml_validator.utils import import_plugin

DEFAULT_PLUGINS = {
    "JsonschemaValidationPlugin": "linkml_validator.plugins.jsonschema_validation.JsonschemaValidationPlugin"
}


class Validator:
    """
    Metadata Validator to validate data against a given schema.

    :param schema: Path or URL to schema YAML
    :param plugins: A set of plugins names to use for validation

    """

    def __init__(self, schema: str, plugins: Set[str] = None) -> None:
        self.schema = schema
        self.plugins = set()
        if plugins:
            for plugin in plugins:
                plugin_module_name = ".".join(plugin.split(".")[:-1])
                plugin_class_name = plugin.split(".")[-1]
                plugin_class = import_plugin(plugin_module_name, plugin_class_name)
                instance = plugin_class(schema=self.schema)  # type: ignore
                self.plugins.add(instance)
        else:
            for plugin in DEFAULT_PLUGINS.values():
                plugin_module_name = ".".join(plugin.split(".")[:-1])
                plugin_class_name = plugin.split(".")[-1]
                plugin_class = import_plugin(plugin_module_name, plugin_class_name)
                instance = plugin_class(schema=self.schema)  # type: ignore
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
    ) -> List[ValidationReport]:
        """
        Validate all objets from a file.

        :param filename: The filename
        :param target_class: The target class which all objects from the input JSON are an instance of
        :param strict: Whether or not to perform strict validation, where any validation
            error stops the validation process. Defaults to False.
        :return: A list of validation reports that summarizes the validation

        """
        reports = []
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                if target_class:
                    for obj in data:
                        report = self.validate(
                            obj=obj, target_class=target_class, strict=strict
                        )
                        reports.append(report)
                else:
                    raise Exception(f"target_class not defined. Cannot validate array of objects from {filename}.")
            else:
                for target_class, objects in data.items():
                    for obj in objects:
                        report = self.validate(
                            obj=obj, target_class=target_class, strict=strict
                        )
                        reports.append(report)
        return reports
