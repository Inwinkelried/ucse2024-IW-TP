# Generated by Django 5.1 on 2024-10-01 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_complejodepadel_prestan_paletas_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complejodepadel',
            old_name='prestan_paletas',
            new_name='presta_paletas',
        ),
    ]
