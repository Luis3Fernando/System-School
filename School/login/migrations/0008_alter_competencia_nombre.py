# Generated by Django 5.0.6 on 2024-07-10 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_remove_curso_hora_fin_remove_curso_hora_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competencia',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]
