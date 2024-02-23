from rest_framework import status 
from rest_framework.response import Response

from .linked_users_methods import *

def processLinkedUsers(request):
    if request.method == 'GET':
        return getLinkedUsers(request)
    
    elif request.method == 'POST':
        return postLinkedUsers(request)
    
    elif request.method == 'DELETE':
        return deleteLinkedUsers(request)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)