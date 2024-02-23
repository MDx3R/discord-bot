from rest_framework import status 
from rest_framework.response import Response

from faceit import faceit_api, stats
from base.models import FaceitPlayer
from api.serializers import FaceitPlayerSerializer

def getFaceitUsersData(request):
    if 'nickname' in request.data:   
        user = FaceitPlayer.objects.filter(nickname = request.data['nickname'])
        if user.exists():
            serializer = FaceitPlayerSerializer(user[0])

            return Response(serializer.data)
    else:
        users = FaceitPlayer.objects.all()
        if users.exists():
            serializer = FaceitPlayerSerializer(users, many = True)

            return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

def postFaceitUsersData(request):
    if 'id' in request.data:
        player_id = request.data['id']
        if FaceitPlayer.objects.filter(id = player_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if 'nickname' in request.data:
            nickname = request.data['nickname']
        else:
            #Добавить обработчик ошибок
            nickname = faceit_api.faceit_get_player_nickname(player_id)
        
        serializer = FaceitPlayerSerializer(data={'id': player_id, 'nickname': nickname, 'stats': stats.get_stats(nickname, player_id)})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

    elif 'nickname' in request.data:
        nickname = request.data['nickname']
        if FaceitPlayer.objects.filter(nickname = nickname).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        #Добавить обработчик ошибок
        player_id = faceit_api.faceit_get_player_id(nickname)
        
        serializer = FaceitPlayerSerializer(data={'id': player_id, 'nickname': nickname, 'stats': stats.get_stats(nickname, player_id)})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
    return Response(status=status.HTTP_400_BAD_REQUEST)
        
def getFaceitUser(request, pk):
    user = FaceitPlayer.objects.filter(id = pk)
    if user.exists():
        serializer = FaceitPlayerSerializer(user[0])

        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

def putFaceitUser(request, pk):
    user = FaceitPlayer.objects.filter(id = pk)
    if user.exists():
        if 'nickname' in request.data:
            user[0].nickname = request.data['nickname']
            if 'stats' not in request.data:
                user[0].stats = 0
            else:
                user[0].stats = request.data['stats']

            user[0].save()

            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

def patchFaceitUser(request, pk):
    #Реализовать вычисления статистики на сервере по запросу ?update_stats=True ?
    user = FaceitPlayer.objects.filter(id = pk)
    if user.exists():
        if 'stats' in request.data:
            user[0].stats = request.data['stats']
        
        if 'nickname' in request.data:
            if request.data['nickname'] == faceit_api.faceit_get_player_nickname(pk):
                user[0].nickname = request.data['nickname']
        
        user[0].save()
        user[0].refresh_from_db()
        serializer = FaceitPlayerSerializer(user[0])

        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)
    
def getFaceitUnsavedUsers(request):
    if 'id' in request.data:
        return Response(stats.get_stats(nickname=faceit_api.faceit_get_player_nickname(request.data['id']), player_id=request.data['id']))
    
    elif 'nickname' in request.data:
        return Response(stats.get_stats(nickname=request.data['nickname'], player_id=faceit_api.faceit_get_player_id(request.data['nickname'])))
    
    return Response(status=status.HTTP_400_BAD_REQUEST)    