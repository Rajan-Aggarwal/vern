"""
File that stores the json schemas for valid request payloads
"""

"""
EXAMPLE FINITE VALUE JSON:
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
    "passport",
    "local"
  ],
  "type": [
    "id"
  ],
  "validation_parser": "finite_values_entity",
  "values": [
    {
      "entity_type": "id",
      "value": "college"
    }
  ]
}
"""

finite_values_json = {
    'name': 'Finite',
    'properties': {
        'invalid_trigger': {
            'type': 'string',
        },
        'key': {
            'type': 'string',
        },
        'name': {
            'type': 'string',
        },
        'reuse': {
            'type': 'boolean',
        },
        'support_multiple': {
            'type': 'boolean',
        },
        'pick_first': {
            'type': 'boolean',
        },
        'supported_values': {
            'type': 'array',
            'items': {'type': 'string'},
        },
        'type': {
            'type': 'array',
            'items': {'type': 'string'},
        },
        'validation_parser': {
            'enum': ['finite_values_entity', ],
        },
        'values': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'entity_type': {
                        'type': 'string',
                    },
                    'value': {
                        'type': ['string', 'number'],
                    }
                },
                'required': ['entity_type', 'value', ],
            }
        },
    },
    # to ensure all values are required
    # and no extra values can be given
    'additionalProperties': False,
    'minProperties': 10,
}

"""
{
  "invalid_trigger": "invalid_age",
  "key": "age_stated",
  "name": "age",
  "reuse": true,
  "pick_first": true,
  "type": [
    "number"
  ],
  "validation_parser": "numeric_values_entity",
  "constraint": "x>=18 and x<=30",
  "var_name": "x",
  "values": [
    {
      "entity_type": "number",
      "value": 23
    }
  ]
}
"""

numeric_values_json = {
    'name': 'Numeric',
    'properties': {
        'invalid_trigger': {
            'type': 'string',
        },
        'key': {
            'type': 'string',
        },
        'name': {
            'type': 'string',
        },
        'reuse': {
            'type': 'boolean',
        },
        'pick_first': {
            'type': 'boolean',
        },
        'type': {
            'type': 'array',
            'items': {'type': 'string'},
        },
        'validation_parser': {
            'enum': ['numeric_values_entity', ],
        },
        'constraint': {
            'type': 'string',
        },
        'var_name': {
            'type': 'string',
        },
        'values': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'entity_type': {
                        'type': 'string',
                    },
                    'value': {
                        'type': ['string', 'number'],
                    }
                },
                'required': ['entity_type', 'value', ],
            }
        },
    },
    # to ensure all values are required
    # and no extra values can be given
    'additionalProperties': False,
    'minProperties': 10,
}
