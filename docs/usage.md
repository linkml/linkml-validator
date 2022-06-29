# Using the LinkML Validator

## Running the LinkML Validator via CLI

To run the LinkML Validator,

```sh
linkml-validator --inputs <INPUT_JSON> \
    --schema <SCHEMA_YAML> \
    --output <OUTPUT>
```

You can pass filepath or a URL that points to the LinkML schema YAML.


### Input Data

#### Input data as a dictionary of objects

The input JSON can be a dictionary of objects keyed by the object type.

```json
{
    "<OBJECT_TYPE>": [
        {

        }
    ]
}
```

Where the `<OBJECT_TYPE>` is the pythonic representation of a class defined in the schema YAML. i.e. the class name is in CamelCase.

For example, consider [examples/example_data1.json](https://github.com/linkml/linkml-validator/blob/main/examples/example_data1.json):

```json
{
    "NamedThing": [
        {
            "id": "obj1",
            "name": "Object 1",
            "type": "X"
        },
        {
            "id": "obj2",
            "name": "Object 2",
            "type": "Y"
        }
    ]
}
```

In the above example, the `NamedThing` is the `target_class`, which is the pythonic
representation of the class `named thing` as defined in the
[examples/example_schema.yaml](https://github.com/linkml/linkml-validator/blob/main/examples/example_schema.yaml).

You can run the validator on the above data as follows:

```sh
linkml-validator --inputs examples/example_data1.json \
    --schema examples/example_schema.yaml \
    --output examples/example_data1_validation_report.json
```

#### Input data as an array of objects

The input JSON can also be an array of objects:

```json
[
    {},
    {}
]
```

In this case, one must also specify the object type via `--target-class` argument in the CLI.

For example, consider [examples/example_data2.json](https://github.com/linkml/linkml-validator/blob/main/examples/example_data2.json):

```json
[
    {
        "id": "obj1",
        "name": "Object 1",
        "type": "X"
    },
    {
        "id": "obj2",
        "name": "Object 2",
        "type": "Y"
    }
]
```

You can run the validator on the above data as follows:

```sh
linkml-validator --inputs examples/example_data2.json \
    --schema examples/example_schema.yaml \
    --output examples/example_data2_validation_report.json \
    --target-class NamedThing
```


### Running selected plugins

To run only certain plugins as part of the validation,

```sh
linkml-validator --inputs data.json \
    --schema schema.yaml \
    --output validation_results.json \
    --plugins JsonSchemaValidationPlugin
```

To perform strict validation,

```sh
linkml-validator --inputs data.json \
    --schema schema.yaml \
    --output validation_results.json \
    --plugins JsonSchemaValidationPlugin \
    --strict
```

Under normal (default) mode, the validator will run all the checks defined in all
referenced plugins on a given object.

When in strict mode, the validator will stop the validation for an object if even one
of the plugins report a failed validation.

### Running your own plugins with the Validator (via CLI)

To run your custom plugin as part of the validation,

```sh
linkml-validator --inputs data.json \
    --schema schema.yaml \
    --output validation_results.json \
    --plugins JsonSchemaValidationPlugin \
    --plugins <CUSTOM_PLUGIN_CLASS>
```
where `<CUSTOM_PLUGIN_CLASS>` is the reference to a custom plugin class.

**Note:** The custom plugin class must be a subclass of `linkml_validator.plugins.base.BasePlugin` and must implement all the methods defined in `BasePlugin` class.



## Using LinkML Validator as a module

You can use the `linkml_validator.validator.Validator` class directly in your codebase
to perform validation on objects that you are working with.

The following code snippet provides a quick way of instantiating the Validator class
and performing validation on an object:

```py
from linkml_validator.validator import Validator

data_obj = {
    "id": "obj1",
    "name": "Object 1",
    "type": "X"
}
validator = Validator(schema="examples/example_schema.yaml")
validator.validate(obj=data_obj, target_class="NamedThing")
```

**Note:** The above code makes the assumption that there is a class `named thing` defined
in the [examples/example_schema.yaml](https://github.com/linkml/linkml-validator/blob/main/examples/example_schema.yaml) and that `NamedThing`
is its Pythonic name.


You can also provide your own custom plugin class to run with the Validator,

```py
from linkml_validator.validator import Validator
from linkml_validator.plugins.base import BasePlugin
from linkml_validator.models import ValidationResult

class MyCustomPlugin(BasePlugin):
    NAME = "MyCustomPlugin"

    def __init__(self, schema: str, **kwargs) -> None:
        super().__init__(schema)

    def process(self, obj: dict, **kwargs) -> ValidationResult:
        # Add your custom logic for processing and validating the incoming object
        valid = False
        print("In MyCustomPlugin.process method")
        result = ValidationResult(
            plugin_name=self.NAME,
            valid=valid,
            validation_messages=[]
        )
        return result

data_obj = {
    "id": "obj1",
    "name": "Object 1",
    "type": "X"
}
validator = Validator(schema="examples/example_schema.yaml", plugins={MyCustomPlugin})
validator.validate(obj=data_obj, target_class="NamedThing")

```
