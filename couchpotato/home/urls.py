
from django.urls import path

from . import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.tests import Test

urlpatterns = [
    path('', views.Home, name='index'),
    path('create/<int:num>', views.CreateList, name='create'),
    path('u/', views.UpdateList, name='update_new'),
    path('a/', views.admin, name='admin'),
    path('save_features', views.SaveApplicationFeatures, name='savefeatures'),
    path('save_user_status', views.SaveUserStatus, name='savefeatures'),
    path('logout/', views.LogoutUser, name='logout'),
    path('login/', views.AuthenticateUser, name='login'),
    path('signup/', views.SignUp, name='signup'),
    # path('register/', views.Register, name='register'),
    path('post_create', views.CreatePost, name='post_create'),
    path('post_update', views.UpdatePost, name='post_update'),
    path('t/', Test, name='test'), 
     
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
