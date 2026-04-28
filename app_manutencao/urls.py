from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  # FAZER LOGIN E EFETUAR REGISTRO NO APP MANUTENÇÃO
    path('', auth_views.LoginView.as_view(), name='login'), # O login é a raiz do site
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),


    # RELATÓRIOS
    path('relatorio/', views.relatorio_equipamentos, name='relatorio'),
  #  path('relatoriogeral/', views.relatorio, name='relatorio_geral'),
    path('relatorio/pdf/', views.relatorio_pdf, name='relatorio_pdf'),

    # CADASTROS DE EQUIPAMENTOS E MANUTENÇÕES
    path('equipamentos/novo/', views.cadastro_equipamento, name='cadastro_equipamento'),
    path('manutencao/novo/', views.cadastro_manutencao, name='cadastro_manutencao'),

]


