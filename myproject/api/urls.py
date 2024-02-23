from django.urls import path
from . import views

urlpatterns = [
    path('api/discord/users', views.getDiscordUsers),
    path('api/faceit/users', views.getFaceitUsers),
    path('api/faceit/unsaved/users', views.getFaceitUnsavedUsers),
    path('api/discord/users/<int:pk>', views.getDiscordUser),
    path('api/faceit/users/<str:pk>', views.getFaceitUser),
    path('api/faceitlinked/users', views.getFaceitLinkedUsers),
]