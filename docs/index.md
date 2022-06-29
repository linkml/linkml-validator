# LinkML Validator

The LinkML Validator is a library for performing validation on data objects that conform to a given LinkML schema.

The Validator is initialized using a LinkML schema YAML, and is designed to allow for flexible validation where each type of validation is done by a plugin.

For example, JSONSchema validation is performed by `JsonSchemaValidationPlugin`.


The LinkML Validator is built with the following goals in mind:

- the Validator should respond with parseable validation messages
- the Validator should not break the validation process even if one object from a list of objects fail validation
- the Validator should provide the ability to perform more than one type of validation on an object

Check out [Design Principles](design.md) for more information about the design principles that went into building the LinkML Validator.



