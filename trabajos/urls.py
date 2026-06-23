from django.urls import path
from . import views

app_name = 'trabajos'

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.crear_trabajo, name='crear'),
    path('<int:trabajo_id>/', views.detalle_trabajo, name='detalle'),
    path('calificar/<int:entrega_id>/', views.calificar_entrega, name='calificar'),
]