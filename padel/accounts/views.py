from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Roles, ComplejoDePadel
from django.contrib.auth import login, authenticate, logout
from .forms import JugadorRegisterForm , ComplejoRegisterForm, ComplejoEditForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from .utils import send_activation_email  

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def activate(request, uidb64, token):
    try:
        # Decodifica uidb64 y convierte a string
        uid = force_str(urlsafe_base64_decode(uidb64))
        # Obtén el usuario basado en el ID
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('home')  # Cambia a tu vista de inicio
    else:
        return render(request, 'registration/activation_invalid.html')








def Visualizar_mis_complejos_view(request):
    user = request.user
    context = {}
    complejos_del_usuario = []
    complejo = ComplejoDePadel.objects.filter(propietario=user)
    complejos_del_usuario.append(complejo)
    context['complejos'] = complejos_del_usuario
    return render(request, 'visualizar_mis_complejos.html', context)    


def Editar_complejo_view(request, id_complejo):
    complejo_a_editar = get_object_or_404(ComplejoDePadel, id=id_complejo)
    if request.method == 'POST':
        form = ComplejoEditForm(request.POST,request.FILES, instance=complejo_a_editar)
        if form.is_valid():
            form.save()
            return redirect('mis_complejos')
    else:
        form = ComplejoEditForm(instance = complejo_a_editar)
    return render(request,'editar_un_complejo.html', {'form':form})




#Esta es la view que maneja el formulario de registro de los complejos. Si la solicitud es un POST, envia el formulario y genera el nuevo usuario tomando el form de registro de complejo, si la solicitud es un GET devuelve el formulario.
def ComplejoRegisterView(request):
    user = request.user
    if request.method == 'POST':
        form = ComplejoRegisterForm(request.POST)
        if form.is_valid():
            complejo = form.save(commit=False)
            complejo.propietario = request.user
            complejo.save()
            if user.rol != Roles.objects.get(nombre=Roles.COMPLEJO):  # Si el usuario no es un complejo
                user.estado = 'pendiente_aprobacion'  # Actualiza el estado del usuario, ya que la primera vez que quiera ser un complejo se tien que dar de alta.
                user.rol = Roles.objects.get(nombre=Roles.COMPLEJO)  # Actualiza el rol del usuario
                user.save()  # Guarda los cambios  
            return redirect('vista_complejos')  # Lo redirecciona a la otra vista
        else:
            return render(request, 'registration/registro_complejos.html', {'form': form})
    else: #Si recibe un GET
        if user.rol == Roles.objects.get(nombre=Roles.COMPLEJO): #Si esta registrado como un complejo
            return redirect('vista_complejos') # Lo redirecciona a la otra vista
        else:
            form = ComplejoRegisterForm()
            return render(request, 'registration/registro_complejos.html', {'form': form})






from .utils import send_activation_email  # Asegúrate de que la función esté importada correctamente

def JugadorRegisterView(request):
    context = {}
    if request.method == 'POST':
        form = JugadorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            send_activation_email(user, request)
            # Redirigir a una página de confirmación o éxito
            return redirect('registration_complete')  # Asegúrate de que esta URL exista
            
        else:
            context['register_form'] = form
    else:
        form = JugadorRegisterForm()
        context['register_form'] = form

    return render(request, 'registration/signup.html', {'form': form})
  
def registration_complete(request):
    return render(request, 'registration/registration_complete.html')








class LoginPersonalizado(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = False  # Redirige incluso si ya está autenticado
    def get_success_url(self):
        user = self.request.user
        if user.rol == 'Complejo':
            return reverse_lazy('vista_complejos')
        else:
            return reverse_lazy('home')








