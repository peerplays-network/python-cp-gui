	
from django.urls import path ,re_path

from . import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.tests import Test
from django.views.static import serve 
from game.restapi import CreatePotatos , UpdatePotatos
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
  
urlpatterns = [
    
      # path('', Game.as_view(), name = 'Game'),
      path('create_potato/',CreatePotatos.as_view(),name=  'create_potato'),
      path('update_potato/',UpdatePotatos.as_view(),name=  'update_potato'),
      path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
      
]

urlpatterns += staticfiles_urlpatterns()
