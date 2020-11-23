
from django.urls import path

from . import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.Home, name='index'),
    path('create/<int:num>', views.CreateList, name='create'),
    path('u/', views.UpdateList, name='update_new'),
    path('t/', views.Test, name='test'),
    path('logout/', views.LogoutUser, name='logout'),
    path('login/', views.AuthenticateUser, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('register/', views.Register, name='register'),
    path('post_create', views.CreatePost, name='post_create'),
    path('post_update', views.UpdatePost, name='post_update'),
     
     
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
