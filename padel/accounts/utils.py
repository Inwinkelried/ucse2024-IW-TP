from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.models import User

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Confirma tu email de padel.com'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    activate_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activate_url = f"http://{current_site.domain}{activate_url}"
    message = render_to_string('registration/activation_email.html', {
        'user': user,
        'activate_url': activate_url,
    })
    send_mail(mail_subject, message, 'facundoschillino01@gmail.com', [user.email])
