
from django.urls import path ,re_path
from django.conf.urls import url, include

from . import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve 

urlpatterns = [
    path('', views.Home, name='index'),
    path('select/', views.LoadSelectOptions, name='createselect'),
    path('usimple/', views.UpdateListSimple, name='udebug'),
    path('history/', views.History, name='history'),
    path('settingspanel/', views.admin, name='admin'),
    path('save_features', views.SaveApplicationFeatures, name='savefeatures'),
    path('delete_user', views.DeleteUser, name='delete_user'),
    path('save_user_status', views.SaveUserStatus, name='savefeatures'),
    path('logout/', views.LogoutUser, name='logout'),
    path('login/', views.AuthenticateUser, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('post_create', views.CreatePost, name='post_create'),
    path('post_update', views.UpdatePost, name='post_update'),
    path('accounts/logout/', views.LogoutSwagger, name='swagger_logout') ,
    url(r'^events/$', views.GetEventsForCalender, name='events'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
     
]

urlpatterns += staticfiles_urlpatterns()
