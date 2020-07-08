"""
Controller for the service
"""
import logging
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import views, status

from . import request_parsers

logger = logging.getLogger(__name__)

def get_error_response_dict(message):
    """
    Method to get dict of the following format:
    {
        'status': 'error',
        'message': <message>,
    }

    :param message: message to be sent to the client
    """
    return {'status': 'error', 'message': str(message)}

class FiniteValuesValidationView(views.APIView):
    """
    Entity validation performed over finite values
    """
    renderer_classes = [JSONRenderer, ]
    parser_classes = (
        # will implicitly utilize the custom parser
        # while parsing the JSON payload
        request_parsers.FiniteValidationJsonParser,
    )
    content_negotiation_class = request_parsers.IgnoreClientContentNegotiation

    def post(self, request, *args, **kwargs):
        """
        Override the post method for POST requests

        :param request: the http request object
        """
        try:
            # parse the input payload
            request.data
        except ParseError as e:
            return Response(
                get_error_response_dict(e.detail),
                status=status.HTTP_400_BAD_REQUEST,
            )
        # TODO: business logic
        return Response({'status': 'success'})

class NumericValuesValidationView(views.APIView):
    """
    Entity validation performed over numeric values
    """
    renderer_classes = [JSONRenderer, ]
    parser_classes = (
        request_parsers.NumericValidationJsonParser,
    )
    content_negotiation_class = request_parsers.IgnoreClientContentNegotiation

    def post(self, request, *args, **kwargs):
        """
        Override the post method for POST requests

        :param request: the http request object
        """
        try:
            # parse the input payload
            request.data
        except ParseError as e:
            return Response(
                get_error_response_dict(e.detail),
                status=status.HTTP_400_BAD_REQUEST,
            )
        # TODO: business logic
        return Response({'status': 'success'})

