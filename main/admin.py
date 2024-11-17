from django.contrib import admin
from .models import Usuario, Autor, Libro, LibroDigital, LibroFisico, Direccion, Reserva, Compra, Carrito, ItemCarrito, Genero, Reseña, Tarjeta, DetalleCompra
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(LibroDigital)
admin.site.register(LibroFisico)
admin.site.register(Direccion)
admin.site.register(Reserva)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Genero)
admin.site.register(Reseña)
admin.site.register(Tarjeta)