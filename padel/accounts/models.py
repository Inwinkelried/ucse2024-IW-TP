from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.Model):
    JUGADOR = 'JUGADOR'
    PROPIETARIO = 'PROPIETARIO'

    ROL_CHOICES = [
        (JUGADOR, 'Jugador'),
        (PROPIETARIO, 'Propietario')
    ]
    nombre = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    ESTADOS = [
        ('activo', 'Activo'),
        ('no_validado', 'No validado'),
        ('pendiente_aprobacion', 'Pendiente aprobación')
    ]
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, name='rol', null=True, default='JUGADOR')
    estado = models.CharField(choices=ESTADOS, max_length=20, name='estado', null=True, default='activo')
    telefono = models.IntegerField(unique=True, name='telefono', null=True)
    es_dueño_pendiente = models.BooleanField(default=False, name='es_dueño_pendiente')

    def __str__(self):
        return self.username

class UsersRoles(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre}"
      

class ComplejoDePadel(models.Model):
    TIPOS_INSTALACION = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('ambas', 'Ambas'),
    ]
    PALETAS_PELOTAS = [
        ('no', 'No'),
        ('prestan', 'Prestan'),
        ('alquilan', 'Alquilan'),
        ('alquilan_y_prestan', 'Alquilan y prestan')
    ]
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    nombre_complejo = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    foto_complejo = models.ImageField(upload_to='fotos/', null=True, blank=True)
    habilitado = models.BooleanField(default=False)
    tipo_instalacion = models.CharField(max_length=10, choices=TIPOS_INSTALACION, null=True, blank=True)
    tiene_duchas = models.BooleanField(default=False, null=True, blank=True)
    tiene_bar = models.BooleanField(default=False, null=True, blank=True)
    prestan_paletas = models.CharField(choices=PALETAS_PELOTAS, max_length=20, default='no')
    prestan_pelotas = models.CharField(choices=PALETAS_PELOTAS, max_length=20, default='no')

    def __str__(self):
        return self.nombre_complejo

class JugadorProfile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)
    categoria = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Categoría {self.categoria}"


