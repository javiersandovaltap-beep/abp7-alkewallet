from django.contrib import admin
from .models import Cuenta, Transaccion


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ['nombre_titular', 'email', 'tipo_cuenta', 'saldo', 'activa', 'fecha_creacion']
    list_filter = ['tipo_cuenta', 'activa']
    search_fields = ['nombre_titular', 'email']
    list_editable = ['activa']


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['cuenta', 'tipo', 'monto', 'descripcion', 'fecha']
    list_filter = ['tipo']
    search_fields = ['cuenta__nombre_titular', 'descripcion']
    raw_id_fields = ['cuenta']
