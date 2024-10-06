# Generated by Django 5.1 on 2024-09-27 21:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_horarioscomplejos_duracion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='disponible',
        ),
        migrations.AddField(
            model_name='turno',
            name='estado',
            field=models.CharField(blank=True, choices=[('reservado', 'Reservado'), ('cancelado', 'Cancelado'), ('pendiente', 'Pendiente'), ('disponible', 'Disponible')], default='disponible', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='turno',
            name='usuario',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]