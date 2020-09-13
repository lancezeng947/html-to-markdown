"""html_to_markdown URL Configuration

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
from django.contrib import admin
from django.urls import path

#From <app> import <views>
from converter import views as converter_views
from registration import views as register_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', converter_views.home, name='home'),
    path('download/', converter_views.home, name='home'), #Force to download page goes to home page
    path(r'download/<str:file_name>', converter_views.download, name='download'),
    #path('register/', register_views.register, name='register'),
    path('about/', converter_views.about, name='about'),

]
