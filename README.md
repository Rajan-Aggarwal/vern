# Slot Validation Service

Recruitment assignment for Vernacular.ai.

This Django RESTful service, made upon DRF, implements the requirements in https://outline.vernacular.ai/share/5efb1bc9-874b-450b-bccf-48f3519db6f4.

# Files to read code

in the folder validations/

- views.py has the controller of endpoints (FiniteValuesValidationView and NumericValuesValidationView), the latter inherits the former.
- engine.py has the business logic
- request_parsers.py provides JSON validation to the input
- schemas.py has the valid JSON schemas for both APIs
- slot_validation_error.py houses the custom exception

# Contract of the REST API

Using jsonschema library, no other format other than as mentioned in the requirements doc is allowed. Custom validations are provided in validations/request_parsers.py

Furthermore, only JSON input and JSON outputs are accepted, and client is not allowed to negotiate this contract: implementations again in validations/request_parsers.py

There are some more validations done during the time input JSON is processed:

1. In case of numeric validation, it is checked if constraint is a valid python expression using ast lib.
2. var_name is also checked if present in constraint expression.
3. There is no limit in the types of values and supported_values and operations used in constraints, however, rest of the input json keys are subject to type checking according to schema in validations/schemas.py
4. first_pick and support_multiple are not allowed to have the same value.
5. no extra key in the input JSON is allowed, and no key should be missed.

There are more validations done during the code execution, but these are to be met for the input JSON to be accepted.

## Where exceptions are thrown during business logic execution:

1. invalid_trigger in empty
2. key is empty
3. no key called 'value' in any of the item in 'values' list
4. the constraint expression doesn't resolve into a boolean value

In all these cases a message of the format:

```
{"status": "error", "message": <description of the error>}
```

will be returned.

# Running the service

Dockerfile is given here, which runs the django server as an entrypoint. Port 8000 is exposed.

```
docker build -t <name>
```

```
docker run -p <port>:8000 <name>
```

Image size is 1.01 GB.

Logging is done on stdout only for convenience, you can change it's configurations in the settings.py file. The level is 'INFO' right now.

# End-points

1. For finite, use /validate/finite/
2. For numeric, use /validate/numeric/

(final backslash is mandatory)

# Testing

All inputs and outputs pair from the document are tested with some additional ones:

1. Usage of types like lists and dictionaries in finite validation

### List
```
{
    "invalid_trigger": "invalid_ids_stated",
    "key": "ids_stated",
    "name": "govt_id",
    "reuse": true,
    "support_multiple": true,
    "pick_first": false,
    "supported_values": [
      "pan",
      "aadhaar",
      "college",
      "corporate",
      "dl",
      "voter",
      [1, 2, 3],
      "local"
    ],
    "type": [
      "id"
    ],
    "validation_parser": "finite_values_entity",
    "values": [
      {
        "entity_type": "id",
        "value": [1, 2, 3]
      }
    ]
  }
```

```
{
   "filled":true,
   "partially_filled":false,
   "trigger":"",
   "parameters":{
      "ids_stated":[
         [1, 2, 3]
      ]
   }
}
```

### Dictionary
```
{
    "invalid_trigger": "invalid_ids_stated",
    "key": "ids_stated",
    "name": "govt_id",
    "reuse": true,
    "support_multiple": true,
    "pick_first": false,
    "supported_values": [
      "pan",
      "aadhaar",
      "college",
      "corporate",
      "dl",
      "voter",
      {
        "hello": "world"
      },
      "local"
    ],
    "type": [
      "id"
    ],
    "validation_parser": "finite_values_entity",
    "values": [
      {
        "entity_type": "id",
        "value": { "hello": "world" }
      }
    ]
  }
```

```
{
   "filled":true,
   "partially_filled":false,
   "trigger":"",
   "parameters":{
      "ids_stated":[
         {
            "hello":"world"
         }
      ]
   }
}
```

2. Numeric constraints on string and list operations

Since ast is used, the constraint can be as complex as possible, given it returns a boolean value and is based on a single variable.

### String

```
{
    "invalid_trigger": "invalid_age",
    "key": "age_stated",
    "name": "age",
    "reuse": true,
    "pick_first": true,
    "type": [
      "string"
    ],
    "validation_parser": "numeric_values_entity",
    "constraint": "x in 'hello world'",
    "var_name": "x",
    "values": [
      {
        "entity_type": "string",
        "value": "hello"
      }
    ]
  }
```

```
{
   "filled":true,
   "partially_filled":false,
   "trigger":"",
   "parameters":{
      "age_stated":"hello"
   }
}
```

### List

```
{
    "invalid_trigger": "invalid_age",
    "key": "age_stated",
    "name": "age",
    "reuse": true,
    "pick_first": true,
    "type": [
      "int"
    ],
    "validation_parser": "numeric_values_entity",
    "constraint": "x in [32, 41, 21]",
    "var_name": "x",
    "values": [
      {
        "entity_type": "int",
        "value": 32
      }
    ]
  }
```

```
{
   "filled":true,
   "partially_filled":false,
   "trigger":"",
   "parameters":{
      "age_stated":32
   }
}
```

# NOTES

I didn't understand the usage of entity_type and type key in input JSON so I didn't implement any validations there. Even the method definition was such. More info about implementation can be found in the in-code documentation. 
