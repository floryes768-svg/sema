from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('maestro/', views.maestro_home, name='maestro_home'),
    path('alumno/', views.alumno_home, name='alumno_home'),
    path('perfil/', views.perfil, name='perfil'),
]