from django.shortcuts import render, redirect
from login.models import Estudiante, Profesore, Curso, Administradore, Usuario, Grado
from .utils import fecha_actual, GetPerson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def Administrador(request):
    try:
        usuario = Usuario.objects.get(dni=request.user)
        administrador = Administradore.objects.get(idUsuario=usuario)
    except Administradore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    total_profesores = Profesore.objects.all().count
    total_estudiantes = Estudiante.objects.all().count
    total_cursos = Curso.objects.all().count
    cursos = Curso.objects.all()
    context = {
        "total_estudiantes": total_estudiantes,
        "total_profesores": total_profesores,
        "total_cursos": total_cursos,
        "fecha": fecha_actual(),
        "cursos": cursos,
        "administrador": administrador 
    }
    return render(request, 'admin.html', context)

def Estudiantes(request):
    estudiantes = Estudiante.objects.all()
    context = {
        "students": estudiantes
    }
    return render(request, 'estudiantes.html', context)

def Cursos(request):
    cursos = Curso.objects.all()
    context ={
        "cursos": cursos
    }
    return render(request, 'cursos.html', context)

@login_required
def Perfil(request):
    try:
        usuario = Usuario.objects.get(dni=request.user)
        administrador = Administradore.objects.get(idUsuario=usuario)
    except Administradore.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    context = {
        "administrador": administrador
    }
    
    return render(request, 'perfil-admin.html', context)

def Profesores(request):
    profesores = Profesore.objects.all()
    
    context = {
        "profesores": profesores
    }
    return render(request, 'profesores.html', context)

@login_required
def agregar_estudiante(request):
    if request.method == 'POST':
        if 'buscar_dni' in request.POST:
            dni = request.POST.get('dni_buscar')
            try:
                usuario = GetPerson(dni)
                grados = Grado.objects.all()
                context={
                    'grados': grados,
                    'usuario': usuario
                }
                return render(request, 'agregar_estudiante.html', context)
            except:
                return HttpResponseForbidden("Hay un error en la API")
            

        elif 'agregar_estudiante' in request.POST:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            direccion = request.POST.get('direccion')
            password = request.POST.get('password')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            celular = request.POST.get('celular')
            dni = request.POST.get('dni')
            apoderado = request.POST.get('apoderado')
            grado_id = request.POST.get('grado')
            
            user = User.objects.create_user(username=dni, password=password, email=email)
            user.first_name = nombre
            user.last_name = apellido
            user.save()

            usuario = Usuario.objects.create(
                user=user,
                nombre=nombre,
                apellido=apellido,
                email=email,
                direccion=direccion,
                password=password,
                fecha_nacimiento=fecha_nacimiento,
                celular=celular,
                dni=dni
            )

            grado = Grado.objects.get(idGrado=grado_id)
            Estudiante.objects.create(idUsuario=usuario, grado=grado, apoderado=apoderado)
            
            return redirect('estudiantes') 
    else:
        grados = Grado.objects.all()
        return render(request, 'agregar_estudiante.html', {'grados': grados})

@login_required    
def agregar_profesor(request):
    if request.method == 'POST':
        if 'buscar_dni' in request.POST:
            dni = request.POST.get('dni_buscar')
            try:
                usuario = GetPerson(dni)
                grados = Grado.objects.all()
                context={
                    'grados': grados,
                    'usuario': usuario
                }
                return render(request, 'agregar_profesor.html', context)
            except:
                return HttpResponseForbidden("Hay un error en la API")

        elif 'agregar_profesor' in request.POST:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            direccion = request.POST.get('direccion')
            password = request.POST.get('password')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            celular = request.POST.get('celular')
            dni = request.POST.get('dni')
            especialidad = request.POST.get('especialidad')
            grado_id = request.POST.get('grado')
            img = request.FILES.get('img', 'media/perfil.jpg')

            user = User.objects.create_user(username=dni, email=email, password=password)
            usuario = Usuario.objects.create(
                user=user,
                nombre=nombre,
                apellido=apellido,
                email=email,
                direccion=direccion,
                password=password,
                fecha_nacimiento=fecha_nacimiento,
                celular=celular,
                dni=dni
            )

            grado = Grado.objects.get(idGrado=grado_id)
            Profesore.objects.create(idUsuario=usuario, especialidad=especialidad, grado=grado, img=img)
            
            return redirect('profesores') 
    else:
        grados = Grado.objects.filter(profesores__isnull=True)
        return render(request, 'agregar_profesor.html', {'grados': grados})
    
def agregar_administrador(request):
    if request.method == 'POST':
        if 'buscar_dni' in request.POST:
            dni = request.POST.get('dni_buscar')
            try:
                usuario = GetPerson(dni)
                context={
                    'usuario': usuario
                }
                return render(request, 'agregar_administrador.html', context)
            except:
                return HttpResponseForbidden("Hay un error en la API")

        elif 'agregar_administrador' in request.POST:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            direccion = request.POST.get('direccion')
            password = request.POST.get('password')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            celular = request.POST.get('celular')
            dni = request.POST.get('dni')

            user = User.objects.create_user(username=dni, email=email, password=password)
            usuario = Usuario.objects.create(
                user=user,
                nombre=nombre,
                apellido=apellido,
                email=email,
                direccion=direccion,
                password=password,
                fecha_nacimiento=fecha_nacimiento,
                celular=celular,
                dni=dni
            )

            Administradore.objects.create(idUsuario=usuario)
            
            return redirect('administrador') 
    else:
        return render(request, 'agregar_administrador.html')
    
    
def agregar_curso(request):
    if request.method == 'POST':
        nombre = request.POST.get('apellido')
        if nombre:
            curso = Curso(nombre=nombre)
            curso.save()
            messages.success(request, 'Curso agregado exitosamente.')
            return redirect('cursos') 
        else:
            messages.error(request, 'El nombre del curso es requerido.')

    return render(request, 'agregar-curso.html')