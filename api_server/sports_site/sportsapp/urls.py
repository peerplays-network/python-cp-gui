
from django.conf.urls import include, url
from sportsapp.game.game import Game

urlpatterns = [
	url(r'api/game/$', Game.as_view(), name = 'Game'),
]
