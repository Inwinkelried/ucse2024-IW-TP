# Generated by Django 5.1 on 2024-10-08 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_complejodepadel_cantidad_pistas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complejodepadel',
            old_name='presta_paleta',
            new_name='prestan_paletas',
        ),
    ]
