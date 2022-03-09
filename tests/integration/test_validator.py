import os
import pytest

from linkml_validator.validator import Validator
from tests import BASE_DIR


@pytest.mark.parametrize(
    "schema,filename,plugins,validation_status",
    [
        (
            os.path.join(BASE_DIR, "resources", "schema", "test_schema1.yml"),
            os.path.join(BASE_DIR, "resources", "data", "test_schema1_data.json"),
            {"jsonschema_validation.JsonschemaValidationPlugin"},
            [True, False, False, False],
        ),
        (
            os.path.join(BASE_DIR, "resources", "schema", "test_schema1.yml"),
            os.path.join(BASE_DIR, "resources", "data", "test_schema1_data.json"),
            {"range_validation.RangeValidationPlugin"},
            [True, True, False, False],
        ),
        (
            os.path.join(BASE_DIR, "resources", "schema", "test_schema1.yml"),
            os.path.join(BASE_DIR, "resources", "data", "test_schema1_data.json"),
            {
                "jsonschema_validation.JsonschemaValidationPlugin",
                "range_validation.RangeValidationPlugin",
            },
            [True, False, False, False],
        ),
    ],
)
def test_validator(schema, filename, plugins, validation_status):
    validator = Validator(
        schema=schema,
        plugins=plugins,
    )
    reports = validator.validate_file(filename=filename)
    for i in range(0, len(validation_status)):
        assert reports[i].valid == validation_status[i]