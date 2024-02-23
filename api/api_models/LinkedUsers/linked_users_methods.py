from rest_framework import status 
from rest_framework.response import Response

from base.models import FaceitPlayer, DiscordUserFaceitAccount
from api.serializers import DiscordUserFaceitAccountSerializer

def getLinkedUsers(request):
    if 'discord_id' in request.data or 'faceit_id' in request.data or 'faceit_nickname' in request.data:
        if 'discord_id' in request.data:
            linked_user = DiscordUserFaceitAccount.objects.filter(discord_id = request.data['discord_id'])
            if linked_user.exists():
                serializer = DiscordUserFaceitAccountSerializer(linked_user[0])

                return Response(serializer.data)
            
        elif 'faceit_id' in request.data:
            linked_user = DiscordUserFaceitAccount.objects.filter(faceit_id = request.data['faceit_id'])
            if linked_user.exists():
                serializer = DiscordUserFaceitAccountSerializer(linked_user[0])

                return Response(serializer.data)
            
        else:
            faceit_id = FaceitPlayer.objects.filter(nickname = request.data['faceit_nickname'])
            if faceit_id.exists():
                linked_user = DiscordUserFaceitAccount.objects.filter(faceit_id = faceit_id[0].id)
                if linked_user.exists():
                    serializer = DiscordUserFaceitAccountSerializer(linked_user[0])

                    return Response(serializer.data)            
    else:
        linked_users = DiscordUserFaceitAccount.objects.all()
        if linked_users.exists():
            serializer = DiscordUserFaceitAccountSerializer(linked_users, many=True)

            return Response(serializer.data)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

def postLinkedUsers(request):
    serializer = DiscordUserFaceitAccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

def deleteLinkedUsers(request):
    if 'discord_id' in request.data or 'faceit_id' in request.data or 'faceit_nickname' in request.data:
        if 'discord_id' in request.data:
            linked_user = DiscordUserFaceitAccount.objects.filter(discord_id = request.data['discord_id'])
            if linked_user.exists():
                linked_user.delete()

                return Response(status=status.HTTP_200_OK)
            
        elif 'faceit_id' in request.data:
            linked_user = DiscordUserFaceitAccount.objects.filter(faceit_id = request.data['faceit_id'])
            if linked_user.exists():
                linked_user.delete()

                return Response(status=status.HTTP_200_OK)

        else:
            faceit_id = FaceitPlayer.objects.filter(nickname = request.data['faceit_nickname'])
            if faceit_id.exists():
                linked_user = DiscordUserFaceitAccount.objects.filter(faceit_id = faceit_id[0].id)
                if linked_user.exists():
                    linked_user.delete()

                    return Response(status=status.HTTP_200_OK)
                
    return Response(status=status.HTTP_400_BAD_REQUEST)