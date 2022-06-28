import json
import click
from linkml_validator.utils import import_plugin
from linkml_validator.validator import DEFAULT_PLUGINS, Validator


PLUGINS = {
    "JsonschemaValidationPlugin": "linkml_validator.plugins.jsonschema_validation.JsonschemaValidationPlugin",
    "RangeValidationPlugin": "linkml_validator.plugins.range_validation.RangeValidationPlugin",
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
    plugin_class_references = set()
    if not plugins:
        plugins = DEFAULT_PLUGINS.values()
    for plugin in plugins:
        if plugin in PLUGINS:
            plugin = PLUGINS[plugin]
        plugin_module_name = ".".join(plugin.split(".")[:-1])
        plugin_class_name = plugin.split(".")[-1]
        plugin_class = import_plugin(plugin_module_name, plugin_class_name)
        plugin_class_references.add(plugin_class)
    validator = Validator(schema=schema, plugins=plugin_class_references)
    for filename in inputs:
        reports = [x for x in validator.validate_file(filename=filename, target_class=target_class, strict=strict)]
        if output:
            with open(output, "w", encoding="UTF-8") as file:
                json.dump([x.dict() for x in reports], file, indent=2)
        else:
            print(json.dumps([x.dict() for x in reports], indent=2))
