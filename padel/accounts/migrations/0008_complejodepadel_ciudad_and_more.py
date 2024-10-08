# Generated by Django 5.1 on 2024-08-28 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_usuario_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='complejodepadel',
            name='ciudad',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='complejodepadel',
            name='prestan_paletas',
            field=models.CharField(choices=[('prestan', 'Prestasn'), ('alquilan', 'Alquilan'), ('alquilan_y_prestan', 'Alquilan_y_prestan')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='complejodepadel',
            name='prestan_pelotas',
            field=models.CharField(choices=[('prestan', 'Prestasn'), ('alquilan', 'Alquilan'), ('alquilan_y_prestan', 'Alquilan_y_prestan')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='complejodepadel',
            name='provincia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='complejodepadel',
            name='tiene_duchas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='complejodepadel',
            name='tipo_instalacion',
            field=models.CharField(choices=[('indoor', 'Indoor'), ('outdoor', 'Outdoor'), ('ambas', 'Ambas')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='complejodepadel',
            name='habilitado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='complejodepadel',
            name='propietario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
