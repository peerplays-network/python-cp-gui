
from django.urls import path ,re_path

from . import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.tests import Test
from django.views.static import serve 

urlpatterns = [
    path('', views.Home, name='index'),
    path('create/<int:num>', views.CreateList, name='create'),
    path('u/', views.UpdateList, name='update_new'),
    path('settingspanel/', views.admin, name='admin'),
    path('save_features', views.SaveApplicationFeatures, name='savefeatures'),
    path('save_user_status', views.SaveUserStatus, name='savefeatures'),
    path('logout/', views.LogoutUser, name='logout'),
    path('login/', views.AuthenticateUser, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('post_create', views.CreatePost, name='post_create'),
    path('post_update', views.UpdatePost, name='post_update'),
    path('t/', Test, name='test'), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
     
]

urlpatterns += staticfiles_urlpatterns()
