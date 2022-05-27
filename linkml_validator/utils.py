import importlib
import json
from functools import lru_cache
from typing import Dict

import stringcase
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator

from linkml_validator.plugins.base import BasePlugin


@lru_cache()
def get_python_module(schema: str) -> object:
    """
    Get Python representation of the schema.

    :param schema: Path or URL to schema YAML
    :return: The Python module compiled from schema YAML

    """
    python_module = PythonGenerator(schema).compile_module()
    return python_module


@lru_cache()
def get_jsonschema(schema: str, py_target_class: object = None) -> Dict:
    """
    Get JSONSchema representation of the schema.

    :param schema: Path or URL to schema YAML
    :param py_target_class: The Python representation of the target class
    :return: The JSONSchema compiled from the schema YAML

    """
    jsonschemastr = JsonSchemaGenerator(
        schema,
        mergeimports=True,
        top_class=py_target_class.class_name if py_target_class else None,
        not_closed=False,
    ).serialize(not_closed=False)
    jsonschema_obj = json.loads(jsonschemastr)
    return jsonschema_obj


def import_plugin(plugin_module_name: str, plugin_class_name: str) -> BasePlugin:
    """
    Import a plugin class.

    :param plugin_module_name: The name of the plugin module
    :param plugin_class_name: The name of the class in the plugin module
    :return: The plugin class

    """
    plugin_module = importlib.import_module(plugin_module_name)
    plugin_class = getattr(plugin_module, plugin_class_name)
    if not issubclass(plugin_class, BasePlugin):
        raise Exception(f"{plugin_module_name}.{plugin_class_name} must be a subclass of {BasePlugin}")
    return plugin_class


def camelcase_to_sentencecase(name: str) -> str:
    """
    Convert a given string from CamelCase to sentence case.

    :param name: A string in CamelCase
    :return: The converted string in sentence case

    """
    return stringcase.sentencecase(stringcase.snakecase(name)).lower()


def snakecase_to_sentencecase(name: str) -> str:
    """
    Convert a given string from snake_case to sentence case.

    :param name: A string in snake_case
    :return: The converted string in sentence case

    """
    return stringcase.sentencecase(name).lower()
