"""
Parsers for JSON validation for API request payloads
+
Creates a custom content negotiator to allow only server to set
content types in the API
"""
import jsonschema
from rest_framework.exceptions import ParseError
from rest_framework import parsers
from rest_framework import negotiation

from . import schemas



class FiniteValidationJsonParser(parsers.JSONParser):
    """
    Custom parser to parse request JSON according to
    schema finite validation schema defined in schema
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
        try:
            jsonschema.validate(data, schemas.finite_values_json)
        except Exception as error:
            print(str(error))
            raise ParseError(detail='JSON validation failed. Check logs...')
        else:
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



