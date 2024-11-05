from django.db import models
from django.core.validators import RegexValidator
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
        ('pendiente_aprobacion', 'Pendiente aprobacion'),
        ("suspendido", "Suspendido"),
        ("eliminado", "Eliminado"),
    ]
    CATEGORIAS = [
        ('no', 'No especificado'),
        ('profesional', 'Profesional'),
        ('1', 'Primera'),
        ('2', 'Segunda'),
        ('3', 'Tercera'),
        ('4', 'Cuarta'),
        ('5', 'Quinta'),
        ('6', 'Sexta'),
        ('7', 'Septima'),
        ('8', 'Octava'),
        ('principiante', 'Principiante')
    ]
    CATEGORIAS = [
        ('profesional', 'Profesional'),
        ('1', 'Primera'),
        ('2', 'Segunda'),
        ('3', 'Tercera'),
        ('4', 'Cuarta'),
        ('5', 'Quinta'),
        ('6', 'Sexta'),
        ('7', 'Septima'),
        ('8', 'Octava'),
    ]
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE,name='rol', null=True)
    categoria = models.CharField(choices=CATEGORIAS, max_length=30,name='categoria', default = '8', null = True)
    estado = models.CharField(choices=ESTADOS,max_length=20, name='estado', null = True, default='pendiente_aprobacion')
    telefono = models.CharField(max_length=15, unique=True, name='telefono',validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="El número de teléfono debe ingresarse en el formato: '+999999999'. Hasta 15 dígitos permitidos."),])


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
    foto_complejo = models.ImageField(upload_to='fotos/', null=True, blank=True, name='foto_complejo') 
    habilitado = models.BooleanField(name='habilitado', default=False)
    tipo_instalacion =  models.CharField(max_length=10, choices=TIPOS_INSTALACION, null=True, blank=True, default='indoor')
    tiene_duchas = models.BooleanField(name='tiene_duchas', default = False, null=True, blank=True)
    tiene_bar = models.BooleanField(name='tiene_bar', default = False, null=True, blank=True),
    prestan_paletas= models.CharField(choices=PALETAS_PELOTAS,max_length=20, name='prestan_paletas', default='no' )
    prestan_pelotas = models.CharField(choices=PALETAS_PELOTAS,max_length=20, name='prestan_pelotas', default='no')
    cantidad_pistas = models.IntegerField(name = 'cantidad_pistas', default=1, null=True)
    def __str__(self):
        return self.nombre_complejo


class JugadorProfile(models.Model): 
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)
    categoria = models.IntegerField(null =True, blank=True, name='categoria') 


#-----------------------------------------------------------------------------------------------
class HorariosComplejos (models.Model):
    complejo = models.ForeignKey(ComplejoDePadel,  on_delete=models.CASCADE,  name= 'complejo', null = False)
    hora_inicio_turnos = models.TimeField(name = 'hora_inicio')
    hora_fin_turnos = models.TimeField(name = 'hora_fin')
    duracion = models.DurationField(name = 'duracion')
    
class Turno(models.Model): 
    Estados_Turnos = [
        ('reservado', 'Reservado'),
        ('cancelado', 'Cancelado'),
        ('pendiente', 'Pendiente'),
        ('disponible', 'Disponible'),
        ('finalizado', 'Finalizado'),
        ('buscando_gente', 'Buscando jugadores')
    ]
    complejo = models.ForeignKey(ComplejoDePadel,on_delete=models.SET_NULL, name = 'complejo', null = True)
    usuario = models.ForeignKey(Usuario,on_delete=models.SET_NULL, name = 'usuario', blank= True, null= True, default=None)
    horario = models.DateTimeField(name = 'horario', null = False)
    estado = models.CharField( max_length=20, choices=Estados_Turnos, null=True, blank=True, default='disponible', name = 'estado')
    duracion = models.DurationField(name = 'duracion', null = False)
    cantidad_jugadores_faltantes = models.IntegerField(default = 0, null = True,name='cantidad_jugadores_faltantes')
    def __str__(self):
        fecha = self.horario.strftime("%Y-%m-%d %H:%M")
        return self.complejo.nombre_complejo +' ' + fecha
class TurnoUsuario(models.Model): 
    Estados_Solicitud_Unirse = [
        ('pendiente',  'Pendiente'), #El usuario solicito unirse a un turno y esta esperando la confirmación.
        ('pendiente_confirmacion_complejo', 'Pendiente confirmacion complejo'), 
        ('aceptado', 'Aceptado'), #El usuario fue aceptado en el turno
        ('rechazado', 'Rechazado'),
        ('confirmado_por_el_complejo', 'Confirmado por el complejo'),
        
    ]
    turno = models.ForeignKey(Turno,on_delete=models.SET_NULL, name='turno',null=True)
    usuario = models.ForeignKey(Usuario,on_delete=models.SET_NULL, name = 'usuario', null=True)
    estado = models.CharField(max_length = 40, choices=Estados_Solicitud_Unirse, null = True, blank= True, name = 'estado')
    fecha = models.DateTimeField(auto_now_add=False, name='fecha')

class ComplejosFotos(models.Model): 
    pass



