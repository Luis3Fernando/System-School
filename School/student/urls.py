from django.urls import path
from . import views

urlpatterns = [
    path('', views.Student, name='student'),
    path('cursos/', views.Cursos, name='cursos'),
    path('notas/', views.Notas, name='notas'),
    path('perfil-student/', views.Perfil, name='perfil-student'),
    path('actualizar-estudiante/<str:dni>/', views.actualizar_estudiante, name='actualizar-estudiante'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]