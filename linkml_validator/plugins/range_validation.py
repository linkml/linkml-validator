from typing import Dict
from linkml_runtime.utils.schemaview import SchemaView
from linkml_validator.models import SeverityEnum, ValidationMessage, ValidationResult
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.utils import (
    camelcase_to_sentencecase,
    snakecase_to_sentencecase,
)


class RangeValidationPlugin(BasePlugin):
    """
    Plugin to check whether fields of an object have the proper range.
    i.e. the value for the fields are in the correct form.

    :param schema: Path or URL to schema YAML
    :param kwargs:

    """

    NAME = "RangeValidationPlugin"

    def __init__(self, schema: str, **kwargs) -> None:
        super().__init__(schema)
        self.schemaview = SchemaView(schema)

    def process(self, obj: Dict, **kwargs) -> ValidationResult:  # noqa: C901
        """
        Perform validation on an object.

        
        :param obj: The object to validate
        :param target_class: The target class
        :return: Validation result that describes the outcome of validation.

        """
        if "target_class" not in kwargs:
            raise Exception("Need `target_class` argument")
        target_class = kwargs["target_class"]
        messages = []
        valid = True
        formatted_target_class = camelcase_to_sentencecase(target_class)
        class_def = self.schemaview.get_class(formatted_target_class)
        slot_usage = class_def.slot_usage
        enums = self.schemaview.all_enums()
        for field, value in obj.items():
            formatted_field = snakecase_to_sentencecase(field)
            slot_def = (
                slot_usage[formatted_field]
                if formatted_field in slot_usage
                else self.schemaview.get_slot(formatted_field)
            )
            if slot_def:
                range_class = slot_def.range
                if not range_class:
                    range_class = self.schemaview.get_slot(formatted_field).range
                    if not range_class:
                        range_class = "string"

                if range_class == "integer":
                    if not isinstance(value, int):
                        valid = False
                        message = ValidationMessage(
                            severity="Error",
                            message=f"{target_class}.{field} must have a value of type 'integer'",
                            field=field,
                            value=value
                        )
                        messages.append(message)
                elif range_class == "float":
                    if not isinstance(value, float):
                        valid = False
                        message = ValidationMessage(
                            severity="Error",
                            message=f"{target_class}.{field} must have a value of type 'float'",
                            field=field,
                            value=value
                        )
                        messages.append(message)
                elif range_class == "string":
                    if not isinstance(value, str):
                        valid = False
                        message = ValidationMessage(
                            severity="Error",
                            message=f"{target_class}.{field} must have a value of type 'string'",
                            field=field,
                            value=value
                        )
                        messages.append(message)
                elif range_class in enums:
                    enum_def = enums[range_class]
                    permissible_values = set(x for x in enum_def.permissible_values)
                    if value not in permissible_values:
                        valid = False
                        message = ValidationMessage(
                            severity="Error",
                            message=f"{target_class}.{field}"
                            + " must have a value from {permissible_values}",
                            field=field,
                            value=value
                        )
                        messages.append(message)
            else:
                valid = False
                message = ValidationMessage(
                    severity=SeverityEnum.error.value,
                    message=f"Cannot find {target_class}.{field} in schema.",
                    field=field,
                    value=value
                )
                messages.append(message)
        result = ValidationResult(
            plugin_name=self.NAME, valid=valid, validation_messages=messages
        )
        return result
