# Design Principle

There are many ways to go about validation and writing a validator.

This document lists series of design principles that were taken into consideration
when building linkml-validator:

- **Schema Agnostic:** The validator must be schema agnostic and must not make any assumptions of the data outside of the scope of LinkML metamodel. i.e. The validator runs for any linkml schema
- **Plugin Architecture:** Each type of validation is its own plugin. So any subsequent vendor-specific or technology-specific validation scenarios must be its own plugin. For example, `JsonSchemaValidationPlugin` performs JSONSchema validation on one or more objects. There are two types of plugins that are supported:
    - *in-house plugins:* These are plugins that are defined in the linkml-validator repository
    - *external plugins:* These are plugins that live outside of the linkml-validator repository. But one main key characteristic of these external plugins is that they implement the linkml-validator's `BasePlugin` abstract class. This is to ensure that the external plugin class is compatible and plays well with the validator and other plugins
- **Easy to Configure**: Each plugin is instantiated with default arguments but these arguments can be overridden by providing the arguments at runtime
- **Flexible Generators:** Plugins use default generators provided by LinkML. But plugins can also provide ways to accept custom generators. This ensures that if a project is using an extended version of a LinkML generator then it is possible with existing plugins
- **Parseable Validation Messages:** The Validator returns easy to parse validation messages with a defined structure.
    - Each time a validation is run on an object, the Validator returns a `ValidationReport` for that object
    - Each `ValidationReport` has one (or more) `ValidationResult`, where each `ValidationResult` is from one (or more) plugin
    - Each `ValidationResult` has one (or more) `ValidationMessage` (a structured message that describes the validation error)
