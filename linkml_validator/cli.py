import json
import click
from linkml_validator.validator import DEFAULT_PLUGINS, Validator


PLUGINS = {
    "JsonschemaValidationPlugin": "jsonschema_validation.JsonschemaValidationPlugin",
    "RangeValidationPlugin": "range_validation.RangeValidationPlugin",
}


@click.command()
@click.option(
    "--inputs",
    "-i",
    required=True,
    multiple=True,
    type=click.Path(exists=True),
    help="Files to validate",
)
@click.option("--schema", "-s", required=True, help="The metadata schema in YAML")
@click.option(
    "--output",
    "-o",
    required=False,
    help="Output file to write validation reports",
    type=click.Path(exists=False),
)
@click.option(
    "--target-class",
    "-t",
    required=False,
    help="The target class which all objects from the input JSON are an instance of",
)
@click.option(
    "--plugins",
    "-p",
    multiple=True,
    default=DEFAULT_PLUGINS.keys(),
    help="The plugins to use for validation",
)
@click.option(
    "--strict",
    default=False,
    is_flag=True,
    help="Whether or not to perform strict validation",
)
def cli(inputs, schema, output, target_class, plugins, strict):
    """
    Run the Validator on data from one or more files.
    """
    for plugin in plugins:
        if plugin not in PLUGINS:
            raise ValueError(
                f"Invalid plugin name: {plugin}. Available plugins are {list(PLUGINS.keys())}"
            )
    validator = Validator(schema=schema, plugins=set(PLUGINS[x] for x in plugins))
    for filename in inputs:
        messages = validator.validate_file(filename=filename, target_class=target_class, strict=strict)
        if output:
            with open(output, "w", encoding="UTF-8") as file:
                json.dump([x.dict() for x in messages], file, indent=2)
        else:
            print(json.dumps([x.dict() for x in messages], indent=2))
