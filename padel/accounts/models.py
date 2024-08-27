from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


#Esta es la clase base desde la que vamos a manejar los diferentes tipos de usuario
class Usuario(AbstractUser): 
    class Rol(models.TextChoices): #Definimos una clase que pueda tener varios tipos
        ADMIN=  "ADMIN", 'admin'
        JUGADOR = "JUGADOR", 'Jugador'
        COMPLEJO = "COMPLEJO", 'Complejo'
    rol_base = Rol.JUGADOR #Definimos el rol base
    rol= models.CharField(max_length=20,choices= Rol.choices, null=True) #Campo
    def save(self, *args, **kwargs):
        if not self.pk and not self.rol:
            self.rol = self.rol_base
        super().save(*args, **kwargs)
        

#El manager se encarga de la logica de recuperacion de datos, filtrado, etc. Esto de momento lo dejo acá pero le tengo que preguntar a Fisa si es mas conveniente manejarlo desde acá o desde lass vistas.
class JugadorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role= Usuario.Rol.JUGADOR)
    

#Vamos a definir una clase de usuario, esta sirve para comportamientos especificos. Por ej, obttener todos los usuarios de tipo JUGADOR  
class Jugador(Usuario): 
    rol_base= Usuario.Rol.JUGADOR
    jugador = JugadorManager
    class Meta:
        proxy = True

class ComplejoManager(BaseUserManager): 
    pass

class Complejo(Usuario):
    rol_base = Usuario.Rol.COMPLEJO
    complejo = ComplejoManager
    class Meta:
        proxy = True

class ComplejoProfile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_complejo = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    

#Est genera la tabla que va a almacenar los datos especificos de los jugadores (Es solo una tabla intermedia que almacena los datos de los jugadores que no quiero que vayan en la tabla de usuarios)
class JugadorProfile(models.Model): 
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE) #Campo especifico
    categoria = models.IntegerField(null =True, blank=True, name='categoria') #Campo especifico
    telefono = models.IntegerField(null =True, blank=True,name='telefono') #Campo especifico

