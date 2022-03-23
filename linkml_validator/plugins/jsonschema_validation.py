from typing import Dict
import jsonschema
from linkml_validator.models import SeverityEnum, ValidationMessage, ValidationResult
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.utils import get_jsonschema, get_python_module


class JsonschemaValidationPlugin(BasePlugin):
    """
    Plugin to perform JSONSchema validation.

    :param schema: Path or URL to schema YAML
    :param kwargs:

    """

    NAME = "JsonschemaValidationPlugin"

    def __init__(self, schema: str, **kwargs) -> None:
        super().__init__(schema)
        self.python_module = get_python_module(schema)

    def process(self, obj: Dict, **kwargs) -> ValidationResult:
        """
        Perform validation on an object.

        :param obj: The object to validate
        :param target_class: The target class
        :return: A Validation result that describes the outcome of validation

        """
        if "target_class" not in kwargs:
            raise Exception("Need `target_class` argument")
        target_class = kwargs["target_class"]
        msg = None
        valid = True
        py_target_class = self.python_module.__dict__[target_class]
        jsonschema_obj = get_jsonschema(self.schema, py_target_class)
        try:
            jsonschema.validate(obj, schema=jsonschema_obj)
            valid = True
            result = ValidationResult(
                plugin_name=self.NAME, valid=valid, validation_messages=[]
            )
        except jsonschema.ValidationError as error:
            msg = error.message
            field = ".".join(error.relative_path) if error.relative_path else None
            valid = False
            msg = ValidationMessage(
                severity=SeverityEnum.error.value,
                message=msg,
                field=field,
                value=error.instance
            )
            result = ValidationResult(
                plugin_name=self.NAME, valid=valid, validation_messages=[msg]
            )
        return result
