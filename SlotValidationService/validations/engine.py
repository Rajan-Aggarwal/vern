"""
This is where the business logic for entity
validation resides
"""
import ast
from typing import List, Dict, Callable, Tuple
from rest_framework import status

# alias for slot validation result tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

class SlotValidationError(Exception):
    """
    Custom exception for all errors thrown while validating
    a slot.
    """

    def __init__(self, error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        """
        Constructor of the custom exception.
        It can be caught and raised in the controller along
        with the parameters concerning API response

        :param error_msg: Description of the error to be sent
            to the client with the error response
        :param status_code: HTTP response status code to be
            sent to the client for the error response
        """
        self.error_msg = error_msg
        self.status_code = status_code
        super().__init__(self.error_msg)


def is_value_valid_finite(
        value_dict: Dict[str, str], 
        supported_values: List[str] = None
    ) -> bool:
    """
    To check whether a value is valid. This essentially means that the value
    is present in the list of supported values.

    :param value: a dictionary with entity-type and value keys
    :param supported_values: a list of values that are valid
    :return: boolean value
    """
    if 'value' not in value_dict:
        raise SlotValidationError('Dictionary given in value did not have values key')
    return value_dict['value'] in supported_values

def validate_finite_values_entity(
        values: List[Dict], 
        supported_values: List[str] = None,
        invalid_trigger: str = None, 
        key: str = None,
        support_multiple: bool = True, 
        pick_first: bool = False, 
        **kwargs
    ) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    if not invalid_trigger:
        # none or empty
        raise SlotValidationError('No invalid trigger provided.')
    if not key:
        raise SlotValidationError('No key provided.')
    if not values:
        # list is empty
        return (False, False, invalid_trigger, {})
    if not supported_values:
        # if there are no values supported it means validation 
        # must fail regardless of entities
        return (filled, False, invalid_trigger, {})
    partially_filled = False
    for value_dict in values:
        if not is_value_valid_finite(value_dict, supported_values):
            partially_filled = True
            break
    filled = not partially_filled
    if filled:
        # a param dictionary must be sent back
        params = {}
        if pick_first:
            # only first slot must be picked
            params = { 
                key: values[0]['value'].upper() 
            }
        else:
            # if not pick first, support_multiple must be true
            # according to the JSON validation
            params = { 
                key: [ v['value'].upper() for v in values ] 
            }
        return (filled, partially_filled, '', params)
    else:
        return (filled, partially_filled, invalid_trigger, {})
            



    