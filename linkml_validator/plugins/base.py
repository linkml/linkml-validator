from abc import ABC, abstractmethod
from typing import Dict
from linkml_validator.models import ValidationResult



class BasePlugin(ABC):
    """
    Base plugin class that all validation plugins should inherit from.

    :param schema: Path or URL to schema YAML
    :param kwargs:

    """

    NAME = "BasePlugin"

    def __init__(self, schema: str, **kwargs) -> None:
        """
        Initialize the plugin with the given schema YAML.

        Args:
            schema: Path or URL to schema YAML
            kwargs: Additional arguments that are used to instantiate the plugin

        """
        self.schema = schema

    @abstractmethod
    def process(self, obj: Dict, **kwargs) -> ValidationResult:
        """
        Run one or more operations on the given object and return
        the results.

        Args:
            obj: The object to process
            kwargs: Additional arguments that are used for processing

        """
        ...
