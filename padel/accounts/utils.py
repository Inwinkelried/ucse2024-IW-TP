from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.models import User

from django.core.mail import EmailMessage

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Confirma tu email de padel.com'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    
    # Imprimir uid y token para depuración
    print(f"UID: {uid}, Token: {token}")
    
    activate_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activate_url = f"http://{current_site.domain}{activate_url}"
    
    print(f"Activation URL: {activate_url}")
    
    message = render_to_string('registration/activation_email.html', {
        'user': user,
        'activate_url': activate_url,
    })
    
    email = EmailMessage(mail_subject, message, 'facundoschillino01@gmail.com', [user.email])
    email.content_subtype = "html"
    email.send()

def enviar_email_confirmacion_turno(user, request, id_complejo):
    current_site = get_current_site(request)
    mail_subject = 'Tienes una nueva reserva!'
    
    notification_url = reverse('ver_reservas_realizadas', kwargs={
        'id_complejo': id_complejo})  
    notification_url = f"http://{current_site.domain}{notification_url}"
    
    message = render_to_string('email/enviar_email_confirmacion_turno.html', {
        'user': user,
        'notification_url': notification_url,
        'mensaje': 'Un usuario desea usar uno de tus turnos! Por favor, ingresa para confirmar o rechazar el turno.'
    })
    email = EmailMessage(mail_subject, message, 'facundoschillino01@gmail.com', [user.email])
    email.content_subtype = "html"
    email.send()

def enviar_email_solcitar_unirse_turno(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Alguien quiere unirse a tu turno'

    notification_url = reverse('ver_mis_reservas', kwargs={})  
    notification_url = f"http://{current_site.domain}{notification_url}"
    
    message = render_to_string('email/enviar_mail_aviso_unirse.html',{
        'user': user,
        'notification_url': notification_url,
        'mensaje': 'Un usuario desea unirse a uno de tus turnos! Por favor, ingresa para confirmar o rechazar la invitacion.'
    })
    email = EmailMessage(mail_subject, message, 'facundoschillino01@gmail.com', [user.email])
    email.content_subtype = "html"
    email.send()

def enviar_mail_aviso_reserva(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Tienes novedades sobre tu turno!'
    notification_url = reverse('ver_mis_reservas', kwargs={})  
    notification_url = f"http://{current_site.domain}{notification_url}"
    
    message = render_to_string('email/enviar_mail_aviso_unirse.html',{
        'user': user,
        'notification_url': notification_url,
        'mensaje': 'Tienes nueva información sobre un turno! Ingresa para confirmar.'
    })
    email = EmailMessage(mail_subject, message, 'facundoschillino01@gmail.com', [user.email])
    email.content_subtype = "html"
    email.send()

    

