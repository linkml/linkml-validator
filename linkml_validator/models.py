from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel


class SeverityEnum(str, Enum):
    """
    Enum to represent the severity of a validation message.
    """
    error = "Error"
    warn = "Warn"
    info = "Info"


class ValidationMessage(BaseModel):
    """
    ValidationMessage represents the warning or error message
    as reported during validation.
    """
    severity: SeverityEnum
    field: Optional[str] = None
    value: Optional[Any] = None
    message: str


class ValidationResult(BaseModel):
    """
    ValidationResult represents the results of validation
    by a plugin.
    """
    plugin_name: str
    valid: bool
    validation_messages: Optional[List[ValidationMessage]] = None


class ValidationReport(BaseModel):
    """
    ValidationReport represents the result of all types of
    validation for a given object.
    """
    object: Dict
    type: str
    valid: bool
    validation_results: List[ValidationResult]
