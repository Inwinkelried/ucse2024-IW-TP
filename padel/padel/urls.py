"""
URL configuration for padel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views as homeview
from accounts import views
from django.views.generic import TemplateView
#Imports para manejo de estaticos.
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.LoginPersonalizado.as_view(), name='login'), 
    path('protected/', homeview.protected_page, name='protected_page'),
    path("", TemplateView.as_view(template_name="home.html"), name="home"), 
    path('registrar_complejo/',views.ComplejoRegisterView, name="registrar_complejo"), 
    path('vista_complejos/',TemplateView.as_view(template_name="vista_complejos.html"), name="vista_complejos" ),
    path('mis_complejos/', views.Visualizar_mis_complejos_view, name="mis_complejos"),
    path('complejo/<int:id_complejo>/editar',views.Editar_complejo_view , name="editar_complejo"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('registration_complete', TemplateView.as_view(template_name="registration/registration_complete.html"), name="registration_complete"),
    path('ver_complejos/', views.ComplejosListView, name="ver_complejos"),
    path('ver_complejos/<int:id>/', views.DetalleComplejoView, name='detalle_complejo'),
    path('mostrar_turnos/<int:id_complejo>/', views.Mostrar_Turnos_View ,name='mostrar_turnos'),
    path('cargar_turno/<int:id_complejo>/', views.Registrar_Turno_View, name='cargar_turno'),
    path('reservar_turno/<int:id_complejo>/<int:id_turno>/', views.Reservar_Turno_View, name='reservar_turno'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

