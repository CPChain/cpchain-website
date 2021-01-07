from rest_framework.views import exception_handler
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['message'] = str(exc)
    else:
        err_data = {
            'code': 503,
            'message': str(exc)
        }
        return JsonResponse(err_data, safe=False, status=503)
    return response
