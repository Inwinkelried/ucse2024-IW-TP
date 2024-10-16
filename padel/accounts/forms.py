from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import JugadorProfile, Usuario, Roles, ComplejoDePadel, Turno, HorariosComplejos
from datetime import timedelta

class ComplejoRegisterForm(forms.ModelForm): 
    nombre_complejo = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    provincia = forms.CharField(max_length=100)
    ciudad = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=100)
    class Meta:
        model = ComplejoDePadel
        fields = ('nombre_complejo','telefono','provincia', 'ciudad','direccion')
    def save(self, commit=True):
        complejo = super().save(commit=False)
        complejo.habilitado = False #Un complejo se crea como no habilitado, es decir no se muestra.
        if commit:
            complejo.save()
        return complejo
        
class ComplejoEditForm(forms.ModelForm):
    nombre_complejo = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    provincia = forms.CharField(max_length=100)
    ciudad = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=100)
    tipo_instalacion =  forms.ChoiceField( choices=ComplejoDePadel.TIPOS_INSTALACION, required=False)
    tiene_duchas = forms.BooleanField(required=False)
    tiene_bar = forms.BooleanField(required=False)
    prestan_paletas = forms.ChoiceField(choices=ComplejoDePadel.PALETAS_PELOTAS,  required=False)
    prestan_pelotas = forms.ChoiceField(choices=ComplejoDePadel.PALETAS_PELOTAS, required=False)
    cantidad_pistas = forms.IntegerField(required=False)
    class Meta:
        model = ComplejoDePadel
        fields = ('nombre_complejo', 'telefono', 'provincia', 'ciudad', 'direccion', 'tipo_instalacion', 'tiene_duchas', 'tiene_bar', 'prestan_paletas', 'prestan_pelotas', 'foto_complejo', 'cantidad_pistas')

class JugadorRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15)
    categoria = forms.ChoiceField(choices=Usuario.CATEGORIAS, max_length=50)
    class Meta:
        model = Usuario
        fields = ( 'username','email','password1','password2', 'telefono', 'categoria')

    def save(self, commit=True):
        user = super().save(commit=False)
        rol_jugador = Roles.objects.get(nombre=Roles.JUGADOR)
        user.rol = rol_jugador  # Un Usuario comienza creado como Jugador.
        if commit:
            user.save()
            JugadorProfile.objects.create(
                user=user,
                categoria=self.cleaned_data['categoria']
            )
        return user
    
class RegistrarTurnoForm(forms.ModelForm):
    DURACIONES = [
    ('01:00:00', '1 hora'),
    ('01:30:00', '1 hora 30 minutos'),
    ('02:00:00', '2 horas'),
]
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), help_text = 'Se debe cargar el rango horario en el que habra turnos disponibles.')
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    duracion = forms.ChoiceField(widget =forms.Select, choices=DURACIONES, )
    class Meta:
        model = HorariosComplejos
        fields = ['duracion', 'hora_inicio', 'hora_fin']
    #Funcion que sobreescribe el metodo clean_duracion para que la duracion sea un objeto timedelta, ya que lo recibe como un string.
    def clean_duracion(self):
        duracion_str = self.cleaned_data['duracion']  
        try:
            horas, minutos, segundos = map(int, duracion_str.split(':'))
            duracion_timedelta = timedelta(hours=horas, minutes=minutos, seconds=segundos)
            return duracion_timedelta
        except ValueError:
            raise forms.ValidationError("Formato inválido para la duración. Use HH:MM:SS.")
