from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomParseError(ParseError):
    def __init__(self, error_code, detail):
        self.error_code = error_code
        self.detail = detail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomParseError):
        custom_response_data = {
            "error_code": exc.error_code,
            "message": exc.detail,
        }
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    return response
