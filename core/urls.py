from django.contrib import admin
from django.urls import path, include
from app_manutencao import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), # ESTA URLPERMITE ACESSAR ADMIN DO DJANGO
    path('', include('app_manutencao.urls')),

]   



