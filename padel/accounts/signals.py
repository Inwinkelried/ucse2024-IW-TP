from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Roles

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == 'accounts':  # Asegúrate de que solo se ejecute para tu app de 'accounts'
        Roles.objects.get_or_create(nombre=Roles.JUGADOR)
        Roles.objects.get_or_create(nombre=Roles.PROPIETARIO)
