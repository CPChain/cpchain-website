"""

CORS

"""
from django.http import JsonResponse

def open_access_middleware(get_response):
    def middleware(request):
        response = None
        if request.method.upper() == 'OPTIONS':
            response = JsonResponse({}, status=200)
        else:
            response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Access-Control-Allow-Methods"] = 'GET,POST,OPTIONS,DELETE,PATCH,PUT'
        return response
    return middleware
