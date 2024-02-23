from rest_framework import serializers
#from base.models import Player
from base.models import DiscordUser, FaceitPlayer, DiscordUserFaceitAccount

class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = '__all__'

class FaceitPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceitPlayer
        fields = '__all__'
    
    # def update(self, instance, validated_data):
    #     instance.id = validated_data.get('id')
    #     instance.id = validated_data.get('id')

class DiscordUserFaceitAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUserFaceitAccount
        fields = '__all__'