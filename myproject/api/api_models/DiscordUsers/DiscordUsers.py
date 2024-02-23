from rest_framework import status 
from rest_framework.response import Response

from .discord_methods import *

def processDiscordUsers(request):
    if request.method == 'GET':
        return getDiscordUsersData(request)
        
    elif request.method == 'POST':
        return postDiscordUsersData(request)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def processDiscordUser(request, pk):
    return getDiscordUserData(request, pk)