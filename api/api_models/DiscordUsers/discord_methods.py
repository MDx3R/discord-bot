from rest_framework import status 
from rest_framework.response import Response

from base.models import DiscordUser
from api.serializers import DiscordUserSerializer

def getDiscordUsersData(request):
    users = DiscordUser.objects.all()
    if users.exists():
        serializer = DiscordUserSerializer(users, many=True)

        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

def postDiscordUsersData(request):
    serializer = DiscordUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
def getDiscordUserData(request, pk):
    user = DiscordUser.objects.filter(id = pk)
    if user.exists():
        serializer = DiscordUserSerializer(user[0])

        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)