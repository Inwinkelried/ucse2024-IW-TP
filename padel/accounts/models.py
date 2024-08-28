from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Roles(models.Model):
    JUGADOR = 'JUGADOR'
    COMPLEJO = 'COMPLEJO'

    ROL_CHOICES = [
        (JUGADOR,'Jugador'),
        (COMPLEJO, 'Complejo')
    ]
    nombre = models.CharField(max_length=20, choices=ROL_CHOICES)


#Esta es la clase base desde la que vamos a manejar los diferentes tipos de usuario
class Usuario(AbstractUser): 
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE,name='rol', null=True)
    telefono = models.IntegerField(unique=True, name='telefono', null=True)
    

    
class ComplejoDePadel(models.Model):
    TIPOS_INSTALACION = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('ambas', 'Ambas'),
    ]
    PALETAS_PELOTAS= [
        ('prestan', 'Prestasn'),
        ('alquilan', 'Alquilan'),
        ('alquilan_y_prestan', 'Alquilan_y_prestan')
    ]
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, name='propietario',null=True)
    nombre_complejo = models.CharField(max_length=100, null=True, blank=True, name='nombre_complejo')
    provincia = models.CharField(max_length=100, null=True, blank=True, name='provincia')
    ciudad = models.CharField(max_length=100, null=True, blank=True, name='ciudad')
    direccion = models.CharField(max_length=200, null=True, blank=True, name='direccion')
    telefono = models.CharField(max_length=20, null=True, blank=True, name='telefono')

    habilitado = models.BooleanField(name='habilitado', default=False)
    tipo_instalacion =  models.CharField( max_length=10, choices=TIPOS_INSTALACION, null=True)
    tiene_duchas = models.BooleanField(name='tiene_duchas', default = False)
    tiene_bar = models.BooleanField(name='tiene_bar', default = False),
    presta_paleta= models.CharField(choices=PALETAS_PELOTAS,max_length=20, name='prestan_paletas', null = True)
    prestan_pelotas = models.CharField(choices=PALETAS_PELOTAS,max_length=20, name='prestan_pelotas', null = True)


class JugadorProfile(models.Model): 
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE) #Campo especifico
    categoria = models.IntegerField(null =True, blank=True, name='categoria') #Campo especifico

