from django.db import models

# Create your models here.
class DiscordUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 48, blank = True, null=True)

class FaceitPlayer(models.Model):
    id = models.CharField(max_length = 48, unique = True, primary_key=True)
    nickname = models.CharField(max_length = 24, unique = True)
    stats = models.JSONField(blank=True, null=True)

class DiscordUserFaceitAccount(models.Model):
    discord_id = models.OneToOneField(DiscordUser, on_delete=models.CASCADE, unique = True)
    faceit_id = models.OneToOneField(FaceitPlayer, on_delete=models.CASCADE, unique = True)