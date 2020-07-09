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
            'items': {},
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
                    'value': {}
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
                    # any type is allowed here
                    'value': {}
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
