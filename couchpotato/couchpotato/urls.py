"""GameInBlockChain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Developers note :
    #   23-12-2020 > Openapi2 with the library django-rest-swagger not supporting


from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Couch Potato API",
      default_version='1.0',
      description="Open APIs Listing",
      terms_of_service="/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)   


urlpatterns = [
    path('', include('home.urls')),
    path('openapi/' , include('game.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]

#     path('openapi-schema/', get_schema_view(
#     title="Couch Potato",  # Title of your app
#     description="Couch Potato",  # Description of your app
#     version="1.0.0",
#     public=True,
# ), name='openapi-schema'), 

#  path('swagger-ui/', TemplateView.as_view(
#         template_name='swagger-ui.html',
#         extra_context={'schema_url':'openapi-schema'}
#     ), name='swagger-ui'),
