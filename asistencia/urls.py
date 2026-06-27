from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('clase/<int:clase_id>/', views.pasar_lista, name='pasar_lista'),
    path('clase/<int:clase_id>/historial/', views.historial, name='historial'),
]