# Generated by Django 5.1 on 2024-09-27 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_roles_nombre_alter_usuario_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complejodepadel',
            name='prestan_paletas',
            field=models.CharField(choices=[('no', 'No'), ('prestan', 'Prestan'), ('alquilan', 'Alquilan'), ('alquilan_y_prestan', 'Alquilan y prestan')], default='no', max_length=20),
        ),
        migrations.AlterField(
            model_name='complejodepadel',
            name='prestan_pelotas',
            field=models.CharField(choices=[('no', 'No'), ('prestan', 'Prestan'), ('alquilan', 'Alquilan'), ('alquilan_y_prestan', 'Alquilan y prestan')], default='no', max_length=20),
        ),
    ]
