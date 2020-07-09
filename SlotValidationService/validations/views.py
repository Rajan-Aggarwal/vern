"""
Controller for the service
"""
import logging
from typing import List, Dict, Callable, Tuple
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import views, status

from . import request_parsers
from . import engine
from .engine import SlotValidationResult

logger = logging.getLogger(__name__)

def get_error_response_dict(message: str) -> Dict:
    """
    Method to get dict of the following format:
    {
        'status': 'error',
        'message': <message>,
    }

    :param message: message to be sent to the client
    :return: a dictionary of the above mentioned format
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

    def create_dict_from_validation_tuple(
            self, validation_tuple: SlotValidationResult
        ) -> Dict:
        """
        Converts the tuple retrieved from validation method from 
        engine into a dictionary

        :param validation_tuple: a tuple of (filled, partially_filled, trigger, params)
        :return: a dictionary of the tuple with keys as mentioned above
        """
        return {
            'filled': validation_tuple[0],
            'partially_filled': validation_tuple[1],
            'trigger': validation_tuple[2],
            'parameters': validation_tuple[3],
        }

    def validate_slots(self, request_data: Dict) -> Dict:
        """
        Validates the incoming request data with slot
        validation from engine. It unpacks data as well.

        :param request_data: a dictionary of request json
        :return: return the response dict
        """
        try:
            validation_tuple = engine.validate_finite_values_entity(
                request_data['values'],
                request_data['supported_values'],
                request_data['invalid_trigger'],
                request_data['key'],
                request_data['support_multiple'],
                request_data['pick_first'],
            )
        except engine.SlotValidationError as e:
            return Response(
                get_error_response_dict(e.error_msg),
                status=e.status_code,
            )
        return self.create_dict_from_validation_tuple(validation_tuple)    

    def post(self, request, *args, **kwargs):
        """
        Override the post method for POST requests

        :param request: the http request object
        :return: a response object
        """
        try:
            # parse the input payload
            request.data
        except ValidationError as e:
            return Response(
                get_error_response_dict(e.detail[0]),
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_dict = self.validate_slots(request.data)
        return Response(response_dict)

class NumericValuesValidationView(FiniteValuesValidationView):
    """
    Entity validation performed over numeric values
    """
    parser_classes = (
        request_parsers.NumericValidationJsonParser,
    )

    # TODO: override validate method


