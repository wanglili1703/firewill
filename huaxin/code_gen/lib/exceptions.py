__author__ = 'Shirley'

from functools import wraps

ERROR_MESSAGE_BORROWER_SERVICE_RESPONSE = 'Error occurred when send request url: %s, message is %s'
ERROR_MESSAGE_LENDER_SERVICE_RESPONSE = 'Error occurred when send request url: %s, message is %s'


def ignore_exception_deco(func):
    """
    It's used to catch negative case exceptions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BorrowerResponseException:
            pass
        except LenderResponseException:
            pass

    return wrapper


class BasicServiceException(Exception):
    """
    Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, request_url, message, result=None, content_apiReturn=None):
        self.request_url = request_url
        self.message = message
        self.result = result
        self.content_apiReturn = content_apiReturn
        self.exception_msg = None

    def __str__(self):
        exception_msg = "Error Message: %s " % unicode(self.exception_msg).encode('utf-8')
        return exception_msg


class BorrowerResponseException(BasicServiceException):
    def __init__(self, request_url, message, result=None, content_apiReturn=None):
        super(BorrowerResponseException, self).__init__(request_url, message, result, content_apiReturn)
        self.exception_msg = ERROR_MESSAGE_BORROWER_SERVICE_RESPONSE % (self.request_url, message)


class LenderResponseException(BasicServiceException):
    def __init__(self, request_url, message, result=None, content_apiReturn=None):
        super(LenderResponseException, self).__init__(request_url, message, result, content_apiReturn)
        self.exception_msg = ERROR_MESSAGE_BORROWER_SERVICE_RESPONSE % (self.request_url, message)
