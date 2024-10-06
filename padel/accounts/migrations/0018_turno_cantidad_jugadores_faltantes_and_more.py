# Generated by Django 5.1 on 2024-09-30 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_turno_disponible_turno_estado_turno_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='cantidad_jugadores_faltantes',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='estado',
            field=models.CharField(blank=True, choices=[('reservado', 'Reservado'), ('cancelado', 'Cancelado'), ('pendiente', 'Pendiente'), ('disponible', 'Disponible'), ('finalizado', 'Finalizado'), ('por_jugarse', 'Por jugarse'), ('buscando_gente', 'Buscando jugadores')], default='disponible', max_length=20, null=True),
        ),
    ]