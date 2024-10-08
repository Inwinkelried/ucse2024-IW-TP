from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
class Roles(models.Model):
    JUGADOR = 'JUGADOR'
    PROPIETARIO = 'PROPIETARIO'

    ROL_CHOICES = [
        (JUGADOR,'Jugador'),
        (PROPIETARIO, 'PROPIETARIO')
    ]
    nombre = models.CharField(max_length=20, choices=ROL_CHOICES)
    def __str__(self):
        return self.nombre
class Usuario(AbstractUser): 
    ESTADOS= [
        ('activo', 'Activo'),
        ('no_validado', 'No validado'),
        ('pendiente_aprobacion', 'Pendiente aprobacion')
    ]
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE,name='rol', null=True)
    estado = models.CharField(choices=ESTADOS,max_length=20, name='estado', null = True, default='pendiente_aprobacion')
    telefono = models.IntegerField(unique=True, name='telefono', null=True)
    

    
class ComplejoDePadel(models.Model):
    TIPOS_INSTALACION = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('ambas', 'Ambas'),
    ]
    PALETAS_PELOTAS= [
        ('no', 'No'),
        ('prestan', 'Prestan'),
        ('alquilan', 'Alquilan'),
        ('alquilan_y_prestan', 'Alquilan y prestan')
    ]
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, name='propietario',null=True)
    nombre_complejo = models.CharField(max_length=100, null=True, blank=True, name='nombre_complejo')
    provincia = models.CharField(max_length=100, null=True, blank=True, name='provincia')
    ciudad = models.CharField(max_length=100, null=True, blank=True, name='ciudad')
    direccion = models.CharField(max_length=200, null=True, blank=True, name='direccion')
    telefono = models.CharField(max_length=20, null=True, blank=True, name='telefono')
    foto_complejo = models.ImageField(upload_to='fotos/', null=True, blank=True, name='foto_complejo') #Este es de prueba

    habilitado = models.BooleanField(name='habilitado', default=False)
    tipo_instalacion =  models.CharField( max_length=10, choices=TIPOS_INSTALACION, null=True, blank=True)
    tiene_duchas = models.BooleanField(name='tiene_duchas', default = False, null=True, blank=True)
    tiene_bar = models.BooleanField(name='tiene_bar', default = False, null=True, blank=True),
    presta_paleta= models.CharField(choices=PALETAS_PELOTAS,max_length=20, name='presta_paleta', default='no' )
    prestan_pelotas = models.CharField(choices=PALETAS_PELOTAS,max_length=20, name='prestan_pelotas', default='no')
    def __str__(self):
        return self.nombre_complejo


class JugadorProfile(models.Model): 
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True) #Campo especifico
    categoria = models.IntegerField(null =True, blank=True, name='categoria') #Campo especifico

