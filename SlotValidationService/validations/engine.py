"""
This is where the business logic for entity
validation resides
"""
import ast
import logging
from typing import List, Dict, Callable, Tuple

from .slot_validation_error import SlotValidationError

# alias for slot validation result tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

logger = logging.getLogger(__name__)

def is_value_valid_finite(
        value_dict: Dict[str, str], 
        supported_values: List[str] = None
    ) -> bool:
    """
    To check whether a value is valid. This essentially means that the value
    is present in the list of supported values.

    NOTE: I didn't understand the purpose of entity-type in validation
        so I am taking it as an argument too in case of future possible
        changes.

    :param value: a dictionary with entity-type and value keys
    :param supported_values: a list of values that are valid
    :return: boolean value
    """
    logger.info('Validating value - {}'.format(value_dict['value']))
    if 'value' not in value_dict:
        logger.error('Dictionary given in value did not have values key.')
        raise SlotValidationError('Values dict cannot have an empty value.')
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
        (it has no usage since pick_first is given but it's given in the method defn)
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    if not invalid_trigger:
        # none or empty
        logger.error('Invalid trigger is {}'.format(invalid_trigger))
        raise SlotValidationError('No invalid trigger provided.')
    if not key:
        logger.error('Key is {}'.format(key))
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
            param_list = []
            for v in values:
                if isinstance(v['value'], str):
                    param_list.append(v['value'].upper())
                else:
                    param_list.append(v['value'])
            params = {key: param_list}
        return (filled, partially_filled, '', params)
    else:
        return (filled, partially_filled, invalid_trigger, {})

def is_value_valid_numeric(
        var_name: str,
        value_dict: Dict[str, str],
        numeric_constraint: str = None,
    ) -> bool:
    """
    Checks if a numeric constraint hold true for the given value
    in the value dictionary using ast module.

    The constraint is assumed to be given in a valid python format
    as the request JSON is validated through custom validators
    given in request_parsers module. Morever, the same validation
    ensures that var_name is present in the constraint string.

    NOTE: I didn't understand the purpose of entity-type in validation
        so I am taking it as an argument too in case of future possible
        changes.

    :param var_name: name of the variable using which constraint is
        written
    :param value_dict: the dictionary with entity_type and value keys
    :param numeric_constraint: the string expression to be applied
        over var_name
    :return: boolean, whether the value conforms to the constraint
    """
    value = value_dict['value']
    logger.info('Validating numerically value - {}'.format(value))
    if not numeric_constraint:
        # if no constraint is given, value is assumed to be valid
        return True

    # compile the assignment
    try:
        if isinstance(value, str):
            # add extra quotations in case of string values
            value = '"{}"'.format(value)
        code = ast.parse('{} = {}'.format(var_name, value))
        exec(compile(code, '', mode='exec'))
    except Exception as error:
        logger.error('Failure during assignment operation for AST - {}'.format(str(error)))
        raise SlotValidationError('Var name could not be assigned.')
    
    # check if the condition holds true
    try:
        code = ast.parse(numeric_constraint, mode='eval')
        res = eval(compile(code, '', mode='eval'))
    except Exception as error:
        logger.error('Failure during constraint evaluation - {}'.format(str(error)))
        raise SlotValidationError('Constraint could not be parsed by AST.')
    
    # check the expression returns a boolean value
    if not isinstance(res, bool):
        logger.error('Constraint expression returned a non boolean value = {}'.format(res))
        raise SlotValidationError('Constraint should resolve to a boolean.')
    
    return res

def validate_numeric_entity(
        values: List[Dict],
        invalid_trigger: str = None,
        key: str = None,
        support_multiple: bool = True,
        pick_first: bool = False,
        constraint=None,
        var_name=None,
        **kwargs
    ) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
        (has no usage here either, keeping it as per method definition)
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    if not invalid_trigger:
        # none or empty
        logger.error('Invalid trigger is {}'.format(invalid_trigger))
        raise SlotValidationError('No invalid trigger provided.')
    if not key:
        logger.error('Key is {}'.format(key))
        raise SlotValidationError('No key provided.')
    if not values:
        # list is empty
        return (False, False, invalid_trigger, {})
    # store all the valid values in a list
    valid_value_list = []
    for value_dict in values:
        if is_value_valid_numeric(var_name, value_dict, constraint):
            valid_value_list.append(value_dict['value'])
    if len(valid_value_list) == len(values):
        # all values were valid
        filled = True
        partially_filled = False
        trigger = ''
    else:
        filled = False
        partially_filled = True
        trigger = invalid_trigger
    if len(valid_value_list) == 0:
        # no value was valid
        params = {}
    elif pick_first:
        params = { key: valid_value_list[0] }
    else:
        # all valid values must be added
        params_list = []
        for v in valid_value_list:
            if isinstance(v, str):
                params_list.append(v.upper())
            else:
                params_list.append(v)
        params = { key: params_list }
    return (filled, partially_filled, trigger, params)
    






    