from rest_framework.decorators import api_view

from .api_models.DiscordUsers.DiscordUsers import processDiscordUsers, processDiscordUser
from .api_models.FaceitUsers.FaceitUsers import processFaceitUsers, processFaceitUser, processFaceitUnsavedUsers
from .api_models.LinkedUsers.LinkedUsers import processLinkedUsers

@api_view(['GET', 'POST'])
def getDiscordUsers(request):
    return processDiscordUsers(request)

@api_view(['GET'])
def getDiscordUser(request, pk):
    return processDiscordUser(request, pk)

@api_view(['GET', 'POST'])
def getFaceitUsers(request):
    return processFaceitUsers(request)

@api_view(['GET'])
def getFaceitUnsavedUsers(request):
    return processFaceitUnsavedUsers(request)

@api_view(['GET', 'PATCH'])
def getFaceitUser(request, pk):
    return processFaceitUser(request, pk)

@api_view(['GET', 'POST', 'DELETE'])
def getFaceitLinkedUsers(request):
    return processLinkedUsers(request)