# Generated by Django 5.1 on 2024-08-31 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_complejodepadel_foto_complejo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='nombre',
            field=models.CharField(choices=[('JUGADOR', 'Jugador'), ('PROPIETARIO', 'PROPIETARIO')], max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='estado',
            field=models.CharField(choices=[('activo', 'Activo'), ('no_validado', 'No validado'), ('pendiente_aprobacion', 'Pendiente aprobacion')], default='pendiente_aprobacion', max_length=20, null=True),
        ),
    ]
