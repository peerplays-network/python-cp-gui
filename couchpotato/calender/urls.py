	
from django.urls import path ,re_path
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve 
from django.urls import path, include


urlpatterns = [
    
      path('',views.index,name=  'calender.html'),
        
]

urlpatterns += staticfiles_urlpatterns()