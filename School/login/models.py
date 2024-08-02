from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', null=True)
    idUsuarios = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    dni = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Grado(models.Model):
    idGrado = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=10)
    aula = models.CharField(max_length=10)
    seccion = models.CharField(max_length=10)
 
    def __str__(self):
        return f"Grado: {self.grado} - Sección: {self.seccion}"
    
class Estudiante(models.Model):
    idEstudiantes = models.AutoField(primary_key=True)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='estudiantes')
    grado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, related_name='estudiantes')
    apoderado = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.idUsuario.nombre} {self.idUsuario.apellido}"

 
class Administradore(models.Model):
    idAdministradores = models.AutoField(primary_key=True)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='administradores')

    def __str__(self):
        return f"{self.idUsuario.nombre} {self.idUsuario.apellido}"


class Profesore(models.Model):
    idProfesores = models.AutoField(primary_key=True)
    especialidad = models.CharField(max_length=50, null=True)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='profesores')
    img = models.ImageField(upload_to='media/fotosPerfil', default='media/perfil.jpg')
    grado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, related_name='profesores')

    def __str__(self):
        return f"{self.idUsuario.nombre} {self.idUsuario.apellido}"


class Curso(models.Model):
    idCurso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre


class Competencia(models.Model):
    idCompetencias = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    idCurso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='competencias')

    def __str__(self):
        return self.nombre


class Nota(models.Model):
    idNotas = models.AutoField(primary_key=True)
    nota = models.CharField(max_length=2, choices=[('C', 'C'), ('B', 'B'), ('A', 'A'), ('AD', 'AD')])
    idStudent = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='notas')
    idCompetencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, related_name='notas')

    def __str__(self):
        return f"Nota: {self.nota} - Estudiante: {self.idStudent}"


class Asistencia(models.Model):
    idasistencia = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=1, choices=[('P', 'Presente'), ('T', 'Tardanza'), ('F', 'Falta'), ('J', 'Justificado')], default='P')
    idstudent = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')

    def __str__(self):
        return f"Asistencia de {self.idstudent} el {self.fecha}"


class MensajesJustificacion(models.Model):
    idmensajes_justificacion = models.AutoField(primary_key=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    idAsistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE, related_name='mensajes_justificacion')

    def __str__(self):
        return f"Mensaje de {self.idAsistencia.idstudent}"
 