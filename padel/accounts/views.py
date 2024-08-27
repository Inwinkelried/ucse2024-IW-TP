from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth import login, authenticate, logout
from .forms import JugadorRegisterForm , ComplejoRegisterForm
from django.urls import reverse_lazy





#Esta es la view que maneja el formulario de registro de los complejos. Si la solicitud es un POST, envia el formulario y genera el nuevo usuario tomando el form de registro de complejo, si la solicitud es un GET devuelve el formulario.
def ComplejoRegisterView(request):
    context = {}
    if request.method == 'POST':
        form = ComplejoRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('vista_complejos')
        else:
            context['registro_complejo'] = form
    else:
        form = ComplejoRegisterForm()
        context['registro_complejo'] = form
    return render(request, 'registration/registro_complejos.html', {'form': form})



#Esta es la view que maneja el formulario de registro de los jugadores. Si la solicitud es un POST, envia el formulario y genera el nuevo usuario tomando el form de registro de complejo, si la solicittud es un GET devuelve el formulario.
def JugadorRegisterView(request):
    context = {}
    if request.method == 'POST':
        form = JugadorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context['register_form'] = form
    else:
        form = JugadorRegisterForm()
        context['register_form'] = form
    return render(request, 'registration/signup.html', {'form': form})



class LoginPersonalizado(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = False  # Redirige incluso si ya está autenticado
    def get_success_url(self):
        user = self.request.user
        if user.rol == Usuario.Rol.COMPLEJO:
            return reverse_lazy('vista_complejos')
        else:
            return reverse_lazy('home')








