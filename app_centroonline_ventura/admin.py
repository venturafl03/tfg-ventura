from django.contrib import admin

# app_centroonline_ventura/admin.py
from django.contrib import admin
from .models import (
    UsuarioPersonalizado,
    Vehiculo,
    TestDrive,
    Producto,
    Pedido,
    ProductoMarket,
    ProyectoConstruccion,
    Perfumeria,
    ProductoEstudio,
    Viaje,

)

# Registro de modelos en el admin

admin.site.register(UsuarioPersonalizado)
admin.site.register(Vehiculo)
admin.site.register(TestDrive)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ProductoMarket)
admin.site.register(ProyectoConstruccion)
admin.site.register(Perfumeria)
admin.site.register(ProductoEstudio)
admin.site.register(Viaje)






