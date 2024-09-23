from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Roles, ComplejoDePadel, HorariosComplejos



class UsuarioAdmin(BaseUserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = (
        'username', 'email', 'telefono', 'estado', 'rol', 'first_name', 
        'last_name', 'is_staff', 'is_superuser', 'last_login', 'date_joined'
    )
    # Campos para filtrar la lista de usuarios
    list_filter = ('estado', 'rol', 'is_staff', 'is_superuser')
    # Campos que aparecen en el detalle del usuario en el admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'rol', 'estado')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Campos que aparecen al añadir un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'telefono', 'password1', 'password2', 'rol', 'estado')}
        ),
    )
    # Campos a usar en la búsqueda del panel de administración
    search_fields = ('username', 'email', 'telefono', 'first_name', 'last_name')

    # Ordenar por defecto por el nombre de usuario
    ordering = ('username',)
admin.site.register(Usuario,UsuarioAdmin)
# Register your models here.

@admin.register(HorariosComplejos)
class AdminHorarios(admin.ModelAdmin):
    lista_display = all

@admin.register(Roles)
class AdminNoticia(admin.ModelAdmin):
    list_display = ('id','nombre')

@admin.register(ComplejoDePadel)
class AdminComplejos(admin.ModelAdmin):
    lista_display=all
