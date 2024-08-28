from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import JugadorProfile, Usuario, Roles, ComplejoDePadel


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
        # Asigna 'habilitado' como False
        complejo.habilitado = False
        if commit:
            complejo.save()
        return complejo
        
class JugadorRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15)
    categoria = forms.CharField(max_length=50)
    class Meta:
        model = Usuario
        fields = ( 'username','email','password1','password2', 'telefono', 'categoria')

    def save(self, commit=True):
        user = super().save(commit=False)
        rol_jugador = Roles.objects.get(nombre=Roles.JUGADOR)
        user.rol = rol_jugador  # Asigna la instancia de Rol
        if commit:
            user.save()
            # Aquí creamos el perfil asociado con los datos del formulario
            JugadorProfile.objects.create(
                user=user,
                categoria=self.cleaned_data['categoria']
            )
        return user