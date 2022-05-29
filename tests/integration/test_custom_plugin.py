import os
from typing import Dict
from linkml_validator.models import ValidationReport, ValidationResult
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.validator import Validator
from tests import BASE_DIR


def test_custom_validation_plugin():
    class CustomPlugin(BasePlugin):
        NAME = "CustomPlugin"
        def __init__(self, schema: str, **kwargs) -> None:
            super().__init__(schema, **kwargs)
        def process(self, obj: Dict, **kwargs):
            # Always report False
            valid = False
            result = ValidationResult(
                plugin_name=self.NAME,
                valid=valid,
                validation_messages=[]
            )
            return result
    schema = os.path.join(BASE_DIR, "resources", "schema", "test_schema1.yml")
    filename = os.path.join(BASE_DIR, "resources", "data", "test_schema1_data.json")
    validator = Validator(schema=schema, plugins={CustomPlugin})
    reports = validator.validate_file(filename=filename)
    for report in reports:
        assert not report.valid

