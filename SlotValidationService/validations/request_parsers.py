"""
Parsers for JSON validation for API request payloads
+
Creates a custom content negotiator to allow only server to set
content types in the API
"""
import logging
import jsonschema
import ast
from rest_framework.exceptions import ValidationError
from rest_framework import parsers
from rest_framework import negotiation

from . import schemas

logger = logging.getLogger(__name__)

class FiniteValidationJsonParser(parsers.JSONParser):
    """
    Custom parser to parse request JSON according to
    schema for finite validation defined in schema
    module
    """
    JSON_SCHEMA = schemas.finite_values_json

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Override the parse method to validate using the schema
        as well. Refer to this for more info: 
        
        https://www.django-rest-framework.org/api-guide/parsers/#custom-parsers

        :param stream: incoming data body
        :param media_type: media type of request
        :param parser_context: to give extra context for parsing
            if required
        :return: dictionary of request data, if valid
        """
        data = super(FiniteValidationJsonParser, self).parse(
            stream, media_type, parser_context,
        )
        # validate the json using the schema
        try:
            jsonschema.validate(data, self.JSON_SCHEMA)
        except Exception as error:
            logger.error('Error while validating the json - {}'.format(error))
            raise ValidationError(detail='JSON validation failed. Check logs...')
        if data['pick_first'] == data['support_multiple']:
            # both being equal makes no sense
            logger.error('Both pick_first and support_multiple are {}'.format(data['pick_first']))
            raise ValidationError(detail='pick_first and support_multiple both cannot be {}'.format(
                    data['pick_first'],
                )
            )
        return data


class NumericValidationJsonParser(parsers.JSONParser):
    """
    Custom parser to parse request JSON according to
    schema for numeric validation defined in schema
    module
    """
    JSON_SCHEMA = schemas.numeric_values_json

    def is_constraint_valid(self, constraint):
        """
        To check if constraint is a valid python expression
        
        :param constraint: a string which is supposed to be a python
            expression
        :return: a boolean value (true if syntax is correct)
        """
        try:
            ast.parse(constraint)
        except SyntaxError as e:
            return False
        return True
    
    def numeric_validation(self, constraint, var_name):
        """
        Validate the following conditions:
            1. the constraint is a python expression
            2. var_name is present in the expression
        Raise error if validation fails.
        
        :param constraint: the conditional expression
        :param var_name: the variable name upon which constraint is applied
        """
        if not self.is_constraint_valid(constraint):
            logger.error('Constraint is not a valid python expression')
            raise ValidationError('Constraint should be a valid python expression')
        if var_name not in constraint:
            logger.error('Var name is not present in the expression.')
            raise ValidationError(detail='Var name should be present in the constraint')
        

    def parse(self, stream, media_type=None, parser_context=None):
        """
        verride the parse method to validate using the schema
        as well. Refer to this for more info: 
        
        https://www.django-rest-framework.org/api-guide/parsers/#custom-parsers

        :param stream: incoming data body
        :param media_type: media type of request
        :param parser_context: to give extra context for parsing
            if required
        :return: dictionary of request data, if valid
        """
        data = super(NumericValidationJsonParser, self).parse(
            stream, media_type, parser_context,
        )
        # validate the json using the schema
        try:
            jsonschema.validate(data, self.JSON_SCHEMA)
        except Exception as error:
            logger.error('Error while validating the json - {}'.format(error))
            raise ValidationError(detail='JSON validation failed. Check logs...')
        self.numeric_validation(data['constraint'], data['var_name'])
        return data


class IgnoreClientContentNegotiation(negotiation.BaseContentNegotiation):
    """
    Directly taken from the documentation of DRF:
        https://www.django-rest-framework.org/api-guide/content-negotiation/
    
    Makes server the sole entity to decide the content and media types
    for the negotiations for an API.
    """

    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]
 
    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)



