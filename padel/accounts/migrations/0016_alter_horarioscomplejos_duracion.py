# Generated by Django 5.1 on 2024-09-23 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_horarioscomplejos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horarioscomplejos',
            name='duracion',
            field=models.DurationField(),
        ),
    ]
