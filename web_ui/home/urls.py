
from django.urls import path

from . import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='index'),
    path('create/<int:num>', views.create, name='create'),
    path('post_create', views.post_create, name='post_create'),
    path('post_update', views.post_update, name='post_update'),
    path('update/', views.update, name='update'),
    path('u/', views.update_new, name='update_new'),
     
     
] 

urlpatterns += staticfiles_urlpatterns()