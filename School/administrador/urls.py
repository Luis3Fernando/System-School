from django.urls import path
from . import views

urlpatterns = [
    path('', views.Administrador, name='administrador'),
    path('cursos/', views.Cursos, name='cursos'),
    path('estudiantes/', views.Estudiantes, name='estudiantes'),
    path('profesores/', views.Profesores, name='profesores'),
    path('perfil/', views.Perfil, name='perfil'),
    path('agregar-estudiante/', views.agregar_estudiante, name='agregar-estudiante'),
    path('agregar-profesor/', views.agregar_profesor, name='agregar-profesor'),
    path('agregar-administrador/', views.agregar_administrador, name='agregar-administrador'),
]