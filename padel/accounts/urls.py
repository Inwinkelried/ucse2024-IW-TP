from django.urls import path

from .views import  JugadorRegisterView


urlpatterns = [
    path("signup/",JugadorRegisterView , name="signup"),
    
]