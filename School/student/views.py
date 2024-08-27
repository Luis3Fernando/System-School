from django.shortcuts import render, redirect, get_object_or_404
from administrador.utils import fecha_actual
from login.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .utils import create_pdf
from django.template.loader import get_template
from django.conf import settings
import os
from django.contrib import messages
from django.utils import timezone


@login_required
def Student(request):
    hoy = timezone.now().date()
    try:
        usuario = Usuario.objects.get(dni=request.user)
        estudiante = Estudiante.objects.get(idUsuario=usuario)
        profesor = Profesore.objects.get(grado=estudiante.grado)
    
    except Estudiante.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    try:
        asistencia = Asistencia.objects.get(idstudent=estudiante,fecha=hoy )
    except:
        asistencia =[]
    cursos = Curso.objects.all()
    total_cursos = cursos.count()
    
    
    context = {
        "estudiante": estudiante,
        "fecha": fecha_actual(),
        "cursos": cursos,
        "total_cursos": total_cursos,
        "asistencia": asistencia,
        "profesor": profesor
    }
    return render(request, 'student.html', context)

@login_required
def EnviarMensaje(request):
    if request.method == 'POST':
        mensaje_texto = request.POST.get('apellido')

        if mensaje_texto:
            try:
                usuario = Usuario.objects.get(user=request.user)
                estudiante = Estudiante.objects.get(idUsuario=usuario)
                
                hoy = timezone.now().date()
                asistencia = Asistencia.objects.get(idstudent=estudiante, fecha=hoy)
                
                mensaje = MensajesJustificacion(
                    mensaje=mensaje_texto,
                    idAsistencia=asistencia
                )
                mensaje.save()
                messages.success(request, 'Mensaje enviado exitosamente.')
                return redirect('student') 
            
            except Estudiante.DoesNotExist:
                messages.error(request, 'No tienes permiso para ver esta página.')
            except Asistencia.DoesNotExist:
                messages.error(request, 'No se encontró asistencia para hoy.')
        else:
            messages.error(request, 'El mensaje es requerido.')

    return render(request, "enviar-mensaje.html")

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

def valor_a_calificacion(promedio):
    """
    Convierte un valor numérico promedio de vuelta a una calificación.
    """
    if promedio >= 18:
        return 'AD'
    elif promedio >= 14:
        return 'A'
    elif promedio >= 11:
        return 'B'
    else:
        return 'C'

def calificacion_a_valor(nota):
    """
    Convierte una calificación en una escala numérica.
    """
    valores = {
        'C': 5,   # Promedio de 0 a 10
        'B': 12,  # Promedio de 11 a 13
        'A': 15.5,  # Promedio de 14 a 17
        'AD': 19  # Promedio de 18 a 20
    }
    return valores.get(nota, 0)

def calcular_promedio_curso(estudiante, nombre_curso):
    """
    Calcula el promedio de un curso específico para un estudiante
    y lo convierte a una calificación (A, B, C, AD).
    Si falta alguna nota para alguna competencia de ese curso, el promedio es None.
    """
    try:
        curso = Curso.objects.get(nombre=nombre_curso)
        competencias = Competencia.objects.filter(idCurso=curso)
        
        total_valor = 0
        total_notas = 0
        
        bandera = False
        print("llegamos antes del for")
        for competencia in competencias:
            nota = Nota.objects.filter(idStudent=estudiante, idCompetencia=competencia).first()
            if nota is None:
                # Si falta alguna nota, retornamos None
                bandera = True
                break
            total_valor += calificacion_a_valor(nota.nota)
            total_notas += 1
        
        print("total notas: ",total_notas)
        if not bandera and total_notas!=0:
            promedio_numerico = total_valor / total_notas
            return valor_a_calificacion(promedio_numerico)
        
        else:
            return None
        
    except Curso.DoesNotExist:
        return None

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

    # Calcular promedios para cada curso
    promedio_comunicacion = calcular_promedio_curso(estudiante, "Comunicación")
    promedio_matematicas = calcular_promedio_curso(estudiante, "Matemáticas")
    promedio_religion = calcular_promedio_curso(estudiante, "Religión")
    promedio_arte = calcular_promedio_curso(estudiante, "Arte y Cultura")
    promedio_ciencia = calcular_promedio_curso(estudiante, "Ciencia y Ambiente")
    promedio_personal = calcular_promedio_curso(estudiante, "Persona Social")

    context = {
        'profesor': profesor,
        'estudiante': estudiante,
        'notas': notas_array,
        'promedio_comunicacion': promedio_comunicacion,
        'promedio_matematicas': promedio_matematicas,
        'promedio_religion': promedio_religion,
        'promedio_arte': promedio_arte,
        'promedio_ciencia': promedio_ciencia,
        'promedio_personal': promedio_personal,
    }

    ruta_template = 'C:/Users/Luis Fernando/Documents/Unamba/Projects/System School/School/static/pdf/pdf_template.html'
    ruta_css = ''  # Ruta del CSS si es necesario

    ruta_pdf = create_pdf(ruta_template, context, rutacss=ruta_css)

    with open(ruta_pdf, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="resultado.pdf"'
        return response
