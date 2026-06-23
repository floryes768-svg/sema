from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar/<int:clase_id>/', views.agregar_nota, name='agregar'),
    path('editar/<int:nota_id>/', views.editar_nota, name='editar'),
]