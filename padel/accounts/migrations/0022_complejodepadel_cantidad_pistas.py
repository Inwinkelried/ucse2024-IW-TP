# Generated by Django 5.1 on 2024-10-08 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_turnousuario_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='complejodepadel',
            name='cantidad_pistas',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
