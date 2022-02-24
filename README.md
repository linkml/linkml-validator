# LinkML Validator

The LinkML Validator is a library for performing validation on data objects that
conform to a given LinkML schema.

The Validator is initialized using a LinkML schema YAML, and is designed to allow
for flexible validation where each type of validation is done by a plugin.

For example, JSONSchema validation is performed by
[JsonschemaValidationPlugin](linkml_validator/plugins/jsonschema_validation.py).

## Installation

```sh
python setup.py install
```


## Running the LinkML Validator via CLI

To run the LinkML Validator,

```sh
linkml-validator --input data.json \
    --schema schema.yaml
    --output validation_results.json
```

You can pass filepath or a URL that points to the LinkML schema YAML.


### Input data as a dictionary of objects

The input JSON can be a dictionary of objects keyed by the object type.

```json
{
    "<OBJECT_TYPE>": [
        {

        }
    ]
}
```

Where the `<OBJECT_TYPE>` is a class name defined in the schema YAML.

For example,

```json
{
    "NamedThing": [
        {

        }
    ]
}
```

In the above example, the `NamedThing` is the `target_class`.

### Input data as an array of ojbects

The input JSON can also be an array of objects:

```json
[
    {},
    {}
]
```

In this case, one must also specify the object type via `--target_class` argument in the CLI.

## Running selected plugins

To run only certain plugins as part of the validation,

```sh
linkml-validator --input data.json \
    --schema schema.yaml
    --output validation_results.json
    --plugin JsonschemaValidationPlugin
```

To perform strict validation,

```sh
linkml-validator --input data.json \
    --schema schema.yaml
    --output validation_results.json
    --plugin JsonschemaValidationPlugin
    --strict
```

Under normal (default) mode, the validator will run all the checks defined in all
referenced plugins on a given object.

When in strict mode, the validator will stop the validation for an object if even one
of the plugins report a failed validation.
