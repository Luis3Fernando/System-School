from django.shortcuts import render, redirect, get_object_or_404
from administrador.utils import fecha_actual
from login.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .utils import create_pdf
from django.template.loader import get_template
from django.conf import settings
import os

@login_required
def Student(request):
    try:
        usuario = Usuario.objects.get(dni=request.user)
        estudiante = Estudiante.objects.get(idUsuario=usuario)
    except Estudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    cursos = Curso.objects.all()
    total_cursos = cursos.count()
    asistencia = Asistencia.objects.get(idstudent=estudiante)
    context = {
        "estudiante": estudiante,
        "fecha": fecha_actual(),
        "cursos": cursos,
        "total_cursos": total_cursos,
        "asistencia": asistencia
    }
    return render(request, 'student.html', context)

def Cursos(request):
    cursos = Curso.objects.all()
    context = {
        "cursos": cursos
    }
    return render(request, 'cursos-student.html', context)

def Notas(request):
    try:
        usuario = Usuario.objects.get(dni=request.user.username)
        estudiante = Estudiante.objects.get(idUsuario=usuario)
    except Estudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")

    cursos = Curso.objects.all()
    notas_por_curso = {}

    for curso in cursos:
        notas = Nota.objects.filter(idStudent=estudiante, idCompetencia__idCurso=curso).select_related('idCompetencia')
        if notas:
            notas_por_curso[curso.nombre] = notas

    context = {
        'notas_por_curso': notas_por_curso,
    }

    return render(request, 'notas-student.html', context)

@login_required
def Perfil(request):
    try:
        usuario = Usuario.objects.get(dni=request.user)
        estudiante = Estudiante.objects.get(idUsuario=usuario)
    except Estudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    context = {
        "estudiante": estudiante,
    }
    return render(request, 'perfil-student.html', context)


def actualizar_estudiante(request, dni):
    usuario = get_object_or_404(Usuario, dni=dni)
    estudiante = get_object_or_404(Estudiante, idUsuario=usuario)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        celular = request.POST.get('celular')
        dni = request.POST.get('dni')
        apoderado = request.POST.get('apoderado')
        grado_id = request.POST.get('grado')

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        usuario.direccion = direccion
        usuario.fecha_nacimiento = fecha_nacimiento
        usuario.celular = celular
        usuario.dni = dni
        usuario.save()

        grado = get_object_or_404(Grado, idGrado=grado_id)
        estudiante.grado = grado
        estudiante.apoderado = apoderado
        estudiante.save()

        return redirect('perfil-student')
    else:
        grados = Grado.objects.all()
        context = {
            'usuario': usuario,
            'estudiante': estudiante,
            'grados': grados
        }
        return render(request, 'actualizar_estudiante.html', context)

def generate_pdf(request):
    try:
        usuario = Usuario.objects.get(dni=request.user.username)
        estudiante = Estudiante.objects.get(idUsuario=usuario)
    except Estudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")

    profesor = Profesore.objects.get(grado=estudiante.grado)
    notas = Nota.objects.filter(idStudent=estudiante)
    notas_array = [None] * 19

    for i, nota in enumerate(notas):
        if i < 19:
            notas_array[i] = nota.nota
            
    context = {
        'profesor': profesor,
        'estudiante': estudiante,
        'notas': notas_array
    }

    ruta_template ='C:/Users/Luis Fernando/Documents/Unamba/Projects/System School/School/static/pdf/pdf_template.html'
    
    #ruta_css = os.path.join(settings.STATIC_ROOT, 'styles', 'pdf_styles.css')
    ruta_css = ''

    ruta_pdf = create_pdf(ruta_template, context, rutacss=ruta_css)

    with open(ruta_pdf, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="resultado.pdf"'
        return response