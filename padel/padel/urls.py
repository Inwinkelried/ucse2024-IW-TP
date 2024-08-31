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
    path('login/', views.LoginPersonalizado.as_view(), name='login'), #URL DE LOGIN
    path('protected/', homeview.protected_page, name='protected_page'),
    path("", TemplateView.as_view(template_name="home.html"), name="home"), #URL DE HOME
    path('registrar_complejo/',views.ComplejoRegisterView, name="registrar_complejo"), ### URL DE LA VISTA DE REGISTRO DEL COMPLEJO
    path('vista_complejos/', views.ListaComplejosView, name='vista_complejos'), ###URL QUE DERIVA A LA VISTA DE LOS COMPLEJOSS UNA VEZ LOGUEADOS   
    path('complejo/<int:complejo_id>/', views.DetalleComplejoView, name='detalle_complejo'),
    path('mis_complejos/', views.Visualizar_mis_complejos_view, name="visualizar_mis_complejos"),
    path('complejo/<int:id_complejo>/editar',views.Editar_complejo_view , name="editar_complejo"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('registration_complete', TemplateView.as_view(template_name="registration/registration_complete.html"), name="registration_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
