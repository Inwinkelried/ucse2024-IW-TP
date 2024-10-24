# Generated by Django 5.1 on 2024-10-02 18:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_turno_cantidad_jugadores_faltantes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='turnousuario',
            name='turno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.turno'),
        ),
        migrations.AddField(
            model_name='turnousuario',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usuario',
            name='categoria',
            field=models.CharField(choices=[('profesional', 'Profesional'), ('1', 'Primera'), ('2', 'Segunda'), ('3', 'Tercera'), ('4', 'Cuarta'), ('5', 'Quinta'), ('6', 'Sexta'), ('7', 'Septima'), ('8', 'Octava')], default='8', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='complejo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.complejodepadel'),
        ),
        migrations.AlterField(
            model_name='turno',
            name='usuario',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
