from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import JugadorProfile, Usuario




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