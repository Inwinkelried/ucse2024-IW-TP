# Generated by Django 5.1 on 2024-10-15 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_rename_presta_paleta_complejodepadel_prestan_paletas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complejodepadel',
            name='tipo_instalacion',
            field=models.CharField(blank=True, choices=[('indoor', 'Indoor'), ('outdoor', 'Outdoor'), ('ambas', 'Ambas')], default='indoor', max_length=10, null=True),
        ),
    ]
