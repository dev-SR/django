from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to format all errors into a consistent structure.
    """
    # Call the default DRF exception handler to get the standard error response
    response = exception_handler(exc, context)
    print(response.data)

    if response is not None:
        # Check if `response.data` is a dictionary
        if isinstance(response.data, dict):
            # Format the dictionary into a consistent error structure
            formatted_errors = []
            for key, value in response.data.items():
                if isinstance(value, list):  # Field-specific errors
                    for error in value:
                        if key in ["non_field_errors"]:
                            key = None
                        formatted_errors.append({"field": key, "message": error})
                else:  # General error message
                    if key in ["detail"]:
                        key = None
                    formatted_errors.append({"field": key, "message": value})
        elif isinstance(response.data, list):  # Non-field-specific errors in a list
            formatted_errors = [
                {"field": None, "message": error} for error in response.data
            ]
        else:  # Handle other unexpected response data
            formatted_errors = [{"field": None, "message": str(response.data)}]

        # Create a unified response format
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "errors": formatted_errors,
        }

    else:
        # Handle errors that DRF couldn't handle (e.g., JSON parsing errors)
        formatted_errors = [{"field": None, "message": str(exc)}]
        response = Response(
            {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "errors": formatted_errors,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
