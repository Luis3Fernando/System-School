# Generated by Django 5.0.6 on 2024-07-08 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_usuarios_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='tipo_usuario',
        ),
    ]
