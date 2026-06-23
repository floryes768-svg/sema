from django.urls import path
from . import views

app_name = 'clases'

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.crear_clase, name='crear'),
    path('unirse/', views.unirse_clase, name='unirse'),
    path('<int:clase_id>/', views.detalle_clase, name='detalle'),
    path('materia/nombre/<str:nombre>/', views.especialidades_materia, name='especialidades'),
    path('materia/<int:materia_id>/', views.detalle_materia, name='detalle_materia'),
    path('materia/<int:materia_id>/editar/', views.editar_materia, name='editar_materia'),
    path('materia/<int:materia_id>/eliminar/', views.eliminar_materia, name='eliminar_materia'),
    path('grupo/<int:clase_id>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupo/<int:clase_id>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),
]