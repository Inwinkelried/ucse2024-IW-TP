from collections import defaultdict
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Roles, ComplejoDePadel, Turno
from django.contrib.auth import login, authenticate, logout
from .forms import JugadorRegisterForm , ComplejoRegisterForm, ComplejoEditForm, RegistrarTurnoForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from .utils import send_activation_email, enviar_email_confirmacion_turno
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


def Registrar_Turno_View(request, id_complejo):
    complejo = get_object_or_404(ComplejoDePadel, id= id_complejo)
    form = RegistrarTurnoForm()
    if request.method == 'POST':
        form = RegistrarTurnoForm(request.POST)
        if form.is_valid():
            turno_nuevo = form.save(commit = False)
            turno_nuevo.complejo = complejo
            turno_nuevo.save()
            generar_turnos(turno_nuevo)
            messages.success(request, 'Turno cargado exitosamente!')
            return render(request, 'cargar_turno.html', {'form': form})
        else:
            return render(request, 'cargar_turno.html', {'form': form})
    else:
        return render (request, 'cargar_turno.html', {'form': form})

def generar_turnos(horario):
    hora_inicio = horario.hora_inicio
    hora_fin = horario.hora_fin
    duracion = horario.duracion
    hoy = datetime.now().date()
    for i in range(14):
        fecha_actual = hoy + timedelta(days=i)
        fechaCargar = datetime.combine(fecha_actual, hora_inicio)
        while fechaCargar.time() < hora_fin:
            turno = Turno(complejo=horario.complejo, horario=fechaCargar, duracion=duracion)
            turno.save()
            fechaCargar += duracion


def generar_turnos_por_dia(turnos):
    turnos_por_dia = defaultdict(list)
    for turno in turnos:
        fecha = turno.horario.date()  
        turnos_por_dia[fecha].append(turno)
    return turnos_por_dia

def Mostrar_Turnos_View(request, id_complejo):
    complejo = get_object_or_404(ComplejoDePadel, id=id_complejo)
    turnos = Turno.objects.filter(complejo=complejo).order_by('horario')
    turnos_por_dia = generar_turnos_por_dia(turnos)
    context = {
        'complejo': complejo,
        'turnos_por_dia': dict(turnos_por_dia), 
    }
    return render(request, 'ver_turnos.html', context)

@login_required(login_url = 'login')
def Reservar_Turno_View(request, id_complejo, id_turno):
    complejo = get_object_or_404(ComplejoDePadel, id=id_complejo)
    turno = get_object_or_404(Turno, id=id_turno)
    context = {
        'complejo': complejo,
        'turno': turno,
    }
    return render(request, 'reservar_turno.html',context) 

def Confirmar_Reserva_View(request,id_complejo, id_turno):
    turno = get_object_or_404(Turno, id=id_turno)
    complejo = get_object_or_404(ComplejoDePadel, id=id_complejo)
    usuario = request.user
    turno.estado = 'pendiente'
    turno.usuario = usuario
    propietario = get_object_or_404(Usuario, id=complejo.propietario.id)
    turno.save()
    enviar_email_confirmacion_turno(propietario, request, id_complejo)
    messages.success(request, 'Turno reservado exitosamente!')
    return redirect('home') 

@login_required(login_url='login')
def Ver_Reservas_Realizadas_View(request, id_complejo):
    complejo = get_object_or_404(ComplejoDePadel,  id=id_complejo)
    turnos = Turno.objects.filter(complejo=complejo, estado = 'pendiente')
    context = {
        'turnos':turnos,
        'complejo':complejo
    }
    return render(request, 'ver_reservas_realizadas.html', context)

def Manejar_Turno_View(request, id_turno):
    turno = get_object_or_404(Turno, id= id_turno)
    complejo = turno.complejo
    confirmacion = request.POST.get('confirmacion')
    if confirmacion == 'aceptar':
        turno.estado = 'reservado'
        turno.save()
        messages.success(request, 'Turno confirmado exitosamente!')
        return redirect(f'/ver_reservas_realizadas/{complejo.id}/')
    elif confirmacion == 'buscando_gente':
        turno.estado = 'buscando_gente'
        turno.cantidad_jugadores_faltantes = int(request.POST.get('cantidad_personas'))
        turno.save()
        messages.success(request, 'Tu turno se ha publicado!')
        return redirect('/ver_mis_reservas/')
    else: 
        turno.estado = 'disponible' #Por ahora solo deja el turno en pendiente, pero lo ideal sería que lo deje en un estado en el que el complejo pueda decidir soobre el, como "disponible_oculto"
        turno.usuario= None
        turno.save()
        messages.success(request, 'Turno rechazado.')
        return redirect(f'/ver_reservas_realizadas/{complejo.id}/')

@login_required(login_url='login')
def Ver_Mis_Reservas_View(request):
    user = request.user
    reservas = Turno.objects.filter(usuario = user, estado = 'reservado')
    reservas_buscando_gente = Turno.objects.filter(usuario = user, estado= 'buscando_gente')
    context = {
        'reservas': reservas,
        'reservas_buscando_gente': reservas_buscando_gente 
    }
    return render(request,'ver_mis_reservas.html',context)

def Mostrar_Turnos_Proximos_View(request): #De momento hace que se muestren todos, habria que acotarle un poco el rango 
    hoy = timezone.now()
    turnos_libres = Turno.objects.filter(horario__gte=hoy, estado='disponible').order_by('horario')
    turnos_falta_gente = Turno.objects.filter(horario__gte=hoy, estado='buscando_gente').order_by('horario')
    turnos_libres = generar_turnos_por_dia(turnos_libres)
    turnos_falta_gente = generar_turnos_por_dia(turnos_falta_gente)
    context = {
        'turnos_libres': dict(turnos_libres),
        'turnos_falta_gente': dict(turnos_falta_gente)
    }
    return render(request, 'mostrar_turnos_proximos.html', context)