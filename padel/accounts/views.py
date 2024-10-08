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
from django.contrib.auth.decorators import login_required

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('home')  
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


def ComplejoRegisterView(request):
    user = request.user
    if request.method == 'POST':
        form = ComplejoRegisterForm(request.POST)
        if form.is_valid():
            complejo = form.save(commit=False)
            complejo.propietario = request.user
            complejo.save()
            if user.rol != Roles.objects.get(nombre=Roles.PROPIETARIO):
                user.estado = 'pendiente_aprobacion'
                user.rol = Roles.objects.get(nombre=Roles.PROPIETARIO)  
                user.save()  
                return redirect('vista_complejos')  
            else:
                return redirect('mis_complejos') #Hay que hacer una vista que diga, Tu complejo se registro exitosamente!
        else:
            return render(request, 'registration/registro_complejos.html', {'form': form})
    else: 
        if user.rol == Roles.objects.get(nombre=Roles.PROPIETARIO) and user.estado == 'pendiente_aprobacion': 
              return redirect('mis_complejos') 
        else:
            form = ComplejoRegisterForm()
            return render(request, 'registration/registro_complejos.html', {'form': form})  

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
    redirect_authenticated_user = False
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url  
        user = self.request.user
        if user.rol == 'Complejo':
            return reverse_lazy('vista_complejos')
        else:
            return reverse_lazy('home')
        
def ComplejosListView(request):
    complejos = ComplejoDePadel.objects.all()

    tipo_instalacion = request.GET.get('tipo_instalacion')
    tiene_duchas = request.GET.get('tiene_duchas')
    alquiler_paletas = request.GET.get('prestan_paletas')

    if tipo_instalacion:
        complejos = complejos.filter(tipo_instalacion=tipo_instalacion)

    if tiene_duchas == 'true':  
        complejos = complejos.filter(tiene_duchas=True)
    elif tiene_duchas == 'false':
        complejos = complejos.filter(tiene_duchas=False)

    if alquiler_paletas:
        complejos = complejos.filter(presta_paleta=alquiler_paletas)

    return render(request, 'complejos.html', {'complejos': complejos})

def DetalleComplejoView(request, id):
    complejo = get_object_or_404(ComplejoDePadel, id=id)
    return render(request, 'detalle_complejo.html', {'complejo': complejo})

@login_required(login_url='login')
def ReservarTurnoView(request):
    return render(request, 'reservar_turno.html')



