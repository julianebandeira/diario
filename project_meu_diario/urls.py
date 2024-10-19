from django.contrib import admin
from django.urls import path
from app_meu_diario import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro-usuario/', views.registro_view, name='registro_usuario'),
    path('novo-registro/', views.novo_registro, name='novo_registro'),
    path('ler-registros/', views.ler_registros, name='ler_registros'),
    path('editar-registro/<int:registro_id>/', views.editar_registro, name='editar_registro'),
]