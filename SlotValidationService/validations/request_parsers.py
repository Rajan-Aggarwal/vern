"""
Parsers for JSON validation for API request payloads
+
Creates a custom content negotiator to allow only server to set
content types in the API
"""
import logging
import jsonschema
import ast
from rest_framework.exceptions import ParseError
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

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Override the parse method to validate using the schema
        as well. Refer to this for more info: 
        
        https://www.django-rest-framework.org/api-guide/parsers/#custom-parsers

        :param stream: incoming data body
        :param media_type: media type of request
        :param parser_context: to give extra context for parsing
            if required
        """
        data = super(FiniteValidationJsonParser, self).parse(
            stream, media_type, parser_context,
        )
        # validate the json using the schema
        try:
            jsonschema.validate(data, schemas.finite_values_json)
        except Exception as error:
            logger.error('Error while validating the json - {}'.format(error))
            raise ParseError(detail='JSON validation failed. Check logs...')
        return data


class NumericValidationJsonParser(parsers.JSONParser):
    """
    Custom parser to parse request JSON according to
    schema for numeric validation defined in schema
    module
    """
    def is_constraint_valid(self, constraint):
        """
        To check if constraint is a valid python expression
        
        :param constraint: a string which is supposed to be a python
            expression
        """
        try:
            ast.parse(constraint)
        except SyntaxError as e:
            return False
        return True

    def parse(self, stream, media_type=None, parser_context=None):
        """
        verride the parse method to validate using the schema
        as well. Refer to this for more info: 
        
        https://www.django-rest-framework.org/api-guide/parsers/#custom-parsers

        :param stream: incoming data body
        :param media_type: media type of request
        :param parser_context: to give extra context for parsing
            if required
        """
        data = super(NumericValidationJsonParser, self).parse(
            stream, media_type, parser_context,
        )
        # validate the json using the schema
        try:
            jsonschema.validate(data, schemas.numeric_values_json)
        except Exception as error:
            logger.error('Error while validating the json - {}'.format(error))
            raise ParseError(detail='JSON validation failed. Check logs...')
        # validate if 
        #   1. the constraint is a python expression
        #   2. var_name is present in the expression
        if not self.is_constraint_valid(data['constraint']):
            logger.error('Constraint is not a valid python expression')
            raise ParseError('Constraint should be a valid python expression')
        if data['var_name'] not in data['constraint']:
            logger.error('Var name is not present in the expression.')
            raise ParseError(detail='Var name should be present in the constraint')
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



