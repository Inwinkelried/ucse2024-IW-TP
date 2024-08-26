from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save #Esto sirve para que cuando un usuario sea creado, envie una señal (Empleado para derivar ottras tareas.)
from django.dispatch import receiver

class Usuario(AbstractUser): #Esta es la clase base desde la que vamos a manejar los diferentes tipos de usuario
    class Rol(models.TextChoices): #Definimos una clase que pueda tener varios tipos
        ADMIN=  "ADMIN", 'admin'
        JUGADOR = "JUGADOR", 'Jugador'
        COMPLEJO = "COMPLEJO", 'Complejo'
    rol_base = Rol.JUGADOR #Definimos el rol base
    rol= models.CharField(max_length=20,choices= Rol.choices, null=True) #Campo

    def save(self, *args, **kwargs): #Lo que hace esto es que al crear un nuevo usuario tenga el rol JUGADOR establecido por default.
        if not self.pk:
            self.rol = self.rol_base
            return super().save(*args, **kwargs)



class JugadorManager(BaseUserManager): #Usamos esto para obttener la lista de usuarios de tipo Jugador
    def get_queryset(self, *args, kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role= Usuario.Rol.JUGADOR)

class Jugador(Usuario): #Vamos a definir una clase de usuario, para que tengas campos necesarios para el usuario
    rol_base= Usuario.Rol.JUGADOR
    jugador = JugadorManager
    class Metat:
        proxy = True

class JugadorProfile(models.Model): #Esta tabla va a almacenar los perfiles de los jugadores (Perfiles con datos detallados de los jugadores)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    categoria = models.IntegerField(null =True, blank=True)
    telefono = models.IntegerField(max_length= 10, null =True, blank=True)

@receiver(post_save, sender=Jugador)
def  crear_perfil_jugador(sender, instance, created, **kwargs): # Esto va a tomar la captacion de un perfil de usuario y lo va a derivar a una nueva tabla.
    if created and instance.rol == "JUGADOR":
        JugadorProfile.objects.create(user=instance)


# Create your models here.
