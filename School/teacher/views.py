from django.shortcuts import render, redirect, get_object_or_404
from login.models import *
from django.utils import timezone
from administrador.utils import fecha_actual
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from administrador.utils import fecha_actual
import json

@login_required
def Teacher(request):    
    try:
        usuario = Usuario.objects.get(dni=request.user)
        profesor = Profesore.objects.get(idUsuario=usuario)
    except Profesore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    cursos = Curso.objects.all()
    hoy = date.today()

    # Obtener todas las asistencias de hoy
    asistencias_hoy = Asistencia.objects.filter(fecha=hoy)

    total_alumnos = Estudiante.objects.count()
    total_ausentes = asistencias_hoy.filter(estado='F').count()
    total_justificados = asistencias_hoy.filter(estado='J').count()
    total_presentes = asistencias_hoy.filter(estado='P').count()

    context = {
        'courses': cursos,
        'profesor': profesor,
        'fecha': hoy,
        'total_alumnos': total_alumnos,
        'total_ausentes': total_ausentes,
        'total_justificados': total_justificados,
        'total_presentes': total_presentes,
    }

    return render(request, 'teacher.html', context)

@login_required
def Asistencias(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        profesor = Profesore.objects.get(idUsuario=usuario)
    except Profesore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    estudiantes = Estudiante.objects.filter(grado=profesor.grado)
    hoy = timezone.now().date()
    
    # Obtener asistencias de hoy
    asistencias_hoy = Asistencia.objects.filter(fecha=hoy, idstudent__grado=profesor.grado)
    
    mensajes_justificacion_hoy = MensajesJustificacion.objects.filter(
        fecha_envio__date=hoy,
        idAsistencia__idstudent__grado=profesor.grado
    )
    estados = ['P', 'T', 'F', 'J']
    
    context = {
        'students': estudiantes,
        'asistencias': asistencias_hoy,
        'mensajes_justificacion': mensajes_justificacion_hoy,
        'estados': estados,
        "fecha": fecha_actual()
    }
    
    if request.method == "POST":
        for student in estudiantes:
            estado = request.POST.get(f"status_{student.id}")
            Asistencia.objects.update_or_create(
                fecha=hoy,
                idstudent=student,
                defaults={'estado': estado}
            )
        return redirect('asistencias')
    
    return render(request, 'asistencia-teacher.html', context)

@login_required
def Estudiantes(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        profesor = Profesore.objects.get(idUsuario=usuario)
    except Profesore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    estudiantes = Estudiante.objects.filter(grado=profesor.grado)
    context = {
        'students': estudiantes
    }
    return render(request, 'estudiantes-teacher.html', context)

def Notas(request):
    cursos = Curso.objects.all()
    context ={
        "cursos": cursos
    }
    return render(request, 'notas-teacher.html', context)

def Perfil(request):
    try:
        usuario = Usuario.objects.get(dni=request.user)
        profesor = Profesore.objects.get(idUsuario=usuario)
    except Profesore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    context = {
        "profesor": profesor,
    }
    
    return render(request, 'perfil-teacher.html', context)

@login_required
def visualizar_notas(request, curso_id):
    try:
        usuario = Usuario.objects.get(user=request.user)
        profesor = Profesore.objects.get(idUsuario=usuario)
    except Profesore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    curso = get_object_or_404(Curso, idCurso=curso_id)
    estudiantes = Estudiante.objects.filter(grado=profesor.grado)
    competencias = Competencia.objects.filter(idCurso=curso)
    total_competencias = competencias.count()
    
    datos_notas = []
    for estudiante in estudiantes:
        fila_notas = {
            'estudiante': estudiante,
            'notas': [Nota.objects.filter(idStudent=estudiante, idCompetencia=competencia).first().nota if Nota.objects.filter(idStudent=estudiante, idCompetencia=competencia).first() else '' for competencia in competencias]
        }
        datos_notas.append(fila_notas)

    context = {
        'estudiantes': estudiantes,
        'competencias': competencias,
        'datos_notas': datos_notas,
        'curso': curso,
        'total_competencias': total_competencias
    }
    
    return render(request, "visualizar-notas.html", context)


@login_required
def editar_notas_estudiante(request, estudiante_id, curso_id):
    estudiante = get_object_or_404(Estudiante, idEstudiantes=estudiante_id)
    curso = Curso.objects.get(pk=curso_id)
    competencias = Competencia.objects.filter(idCurso=curso)

    if request.method == 'POST':
        for competencia in competencias:
            nota_valor = request.POST.get(f'nota_{competencia.idCompetencias}')
            if nota_valor:
                nota, created = Nota.objects.update_or_create(
                    idStudent=estudiante,
                    idCompetencia=competencia,
                    defaults={'nota': nota_valor}
                )
        return redirect('visualizar_notas', curso_id=curso.idCurso)

    notas = {}
    for competencia in competencias:
        nota = Nota.objects.filter(idStudent=estudiante, idCompetencia=competencia).first()
        notas[competencia.idCompetencias] = nota.nota if nota else ''

    context = {
        'estudiante': estudiante,
        'competencias': competencias,
        'notas': notas,
    }
    
    return render(request, "editar-notas-estudiante.html", context)

@login_required
def actualizar_profesor(request, profesor_id):
    usuario = get_object_or_404(Usuario, dni=profesor_id)
    profesor = get_object_or_404(Profesore, idUsuario=usuario)

    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.email = request.POST.get('email')
        usuario.direccion = request.POST.get('direccion')
        usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        usuario.celular = request.POST.get('celular')
        usuario.save()

        profesor.especialidad = request.POST.get('especialidad')
        if 'img' in request.FILES:
            profesor.img = request.FILES['img']
        profesor.save()

        return redirect('perfil-profesor')

    context = {
        'profesor': profesor
    }
    return render(request, 'actualizar_profesor.html', context)

def agregar_competencia(request):
    cursos = Curso.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        curso_id = request.POST['curso']
        curso = Curso.objects.get(pk=curso_id)
        competencia = Competencia.objects.create(nombre=nombre, idCurso=curso)
        return redirect('notas')
    
    return render(request, 'agregar-competencia.html', {'cursos': cursos})

def guardar_asistencia(request, id_student):
    if request.method == 'POST':
        data = json.loads(request.body)
        estado = data.get('estado')

        estudiante = get_object_or_404(Estudiante, idEstudiantes=id_student)
        hoy = date.today()

        # Busca si ya hay una asistencia para hoy
        asistencia, created = Asistencia.objects.get_or_create(
            idstudent=estudiante, 
            fecha=hoy,
            defaults={'estado': estado}
        )

        # Si la asistencia ya existía, actualiza el estado
        if not created:
            asistencia.estado = estado
            asistencia.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)