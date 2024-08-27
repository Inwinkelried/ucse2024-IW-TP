from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import JugadorProfile, Usuario, ComplejoProfile


class ComplejoRegisterForm(UserCreationForm): 
    nombre_complejo = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    direccion = forms.CharField(max_length=100)
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'nombre_complejo', 'telefono', 'direccion')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.Rol.COMPLEJO  # Asigna el rol de COMPLEJO
        if commit:
            user.save()
            # Aquí creamos el perfil asociado con los datos del formulario
            ComplejoProfile.objects.create(
                user=user,
                nombre_complejo=self.cleaned_data['nombre_complejo'],
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion']
            )
        return user
#Form para registrarse como un jugador
class JugadorRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15)
    categoria = forms.CharField(max_length=50)
    class Meta:
        model = Usuario
        fields = ( 'username','email','password1','password2', 'telefono', 'categoria')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.Rol.JUGADOR  # Asigna el rol de JUGADOR
        if commit:
            user.save()
            # Aquí creamos el perfil asociado con los datos del formulario
            JugadorProfile.objects.create(
                user=user,
                telefono=self.cleaned_data['telefono'],
                categoria=self.cleaned_data['categoria']
            )
        return user