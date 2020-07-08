"""
File that stores the json schemas for valid request payloads
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
                        'type': 'string',
                    }
                },
                'required': ['entity_type', 'value', ],
            }
        },
    },
    'additionalProperties': False,
    'minProperties': 10,
}

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

