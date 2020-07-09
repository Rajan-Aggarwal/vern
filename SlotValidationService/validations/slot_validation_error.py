"""
defining the custom exceptions here
"""

from rest_framework import status

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