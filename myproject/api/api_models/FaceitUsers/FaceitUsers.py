from rest_framework import status 
from rest_framework.response import Response

from .faceit_methods import *

def processFaceitUsers(request):
    if request.method == 'GET':
        return getFaceitUsersData(request)
        
    elif request.method == 'POST':
        return postFaceitUsersData(request)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
def processFaceitUser(request, pk):
    if request.method == 'GET':
        return getFaceitUser(request, pk)

    if request.method == 'PUT':
        return putFaceitUser(request, pk)

    if request.method == 'PATCH':
        return patchFaceitUser(request, pk)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def processFaceitUnsavedUsers(request):
    return getFaceitUnsavedUsers(request)