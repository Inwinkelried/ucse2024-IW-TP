from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Roles

admin.site.register(Usuario,UserAdmin)
# Register your models here.
@admin.register(Roles)
class AdminNoticia(admin.ModelAdmin):
    list_display = ('id','nombre')
    