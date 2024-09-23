from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import JugadorProfile, Usuario, Roles, ComplejoDePadel, Turno, HorariosComplejos


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
    presta_paleta = forms.ChoiceField(choices=ComplejoDePadel.PALETAS_PELOTAS,  required=False)
    prestan_pelotas = forms.ChoiceField(choices=ComplejoDePadel.PALETAS_PELOTAS, required=False)

    class Meta:
        model = ComplejoDePadel
        fields = ('nombre_complejo', 'telefono', 'provincia', 'ciudad', 'direccion', 'tipo_instalacion', 'tiene_duchas', 'tiene_bar', 'presta_paleta', 'prestan_pelotas', 'foto_complejo')

class JugadorRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15)
    categoria = forms.CharField(max_length=50)
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
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), help_text = 'Puedes cargar los horarios individuales, o cargar un rango horario en el que habra horarios intermedios. Por ejemplo, si colocamos de 13:30 a 18 los turnos seran: 13:30, 15:00 y 16:30 sin incluir las 18 hs.')
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    duracion = forms.ChoiceField(widget =forms.Select, choices=DURACIONES, )
    class Meta:
        model = HorariosComplejos
        fields = ['duracion', 'hora_inicio', 'hora_fin']

