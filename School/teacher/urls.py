from django.urls import path
from . import views

urlpatterns = [
    path('', views.Teacher, name='teacher'),
    path('asistencia/', views.Asistencias, name='asistencia'),
    path('estudiantes/', views.Estudiantes, name='estudiantes'),
    path('notas/', views.Notas, name='notas'),
    path('perfil-profesor/', views.Perfil, name='perfil-profesor'),
    path('actualizar-profesor/<int:profesor_id>/', views.actualizar_profesor, name='actualizar-profesor'),
    path('curso/<int:curso_id>/notas/', views.visualizar_notas, name='visualizar_notas'),
    path('curso/<int:curso_id>/editar_notas/<int:estudiante_id>/', views.editar_notas_estudiante, name='editar_notas_estudiante'),
    path('agregar_competencia/', views.agregar_competencia, name='agregar_competencia'),   
    path('guardar_asistencia/<int:id_student>/', views.guardar_asistencia, name='guardar_asistencia'),
]