# Generated by Django 5.0.6 on 2024-07-08 16:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_remove_usuarios_tipo_usuario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Administradores',
            new_name='Administradore',
        ),
        migrations.RenameModel(
            old_name='Competencias',
            new_name='Competencia',
        ),
        migrations.RenameModel(
            old_name='Estudiantes',
            new_name='Estudiante',
        ),
        migrations.RenameModel(
            old_name='Notas',
            new_name='Nota',
        ),
        migrations.RenameModel(
            old_name='Profesores',
            new_name='Profesore',
        ),
        migrations.RenameModel(
            old_name='Usuarios',
            new_name='Usuario',
        ),
    ]
