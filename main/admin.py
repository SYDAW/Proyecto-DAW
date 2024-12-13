from django.contrib import admin
from .models import Usuario, Autor, Libro, LibroDigital, LibroFisico, Direccion, Compra, Carrito, ItemCarrito, Genero, Reseña, Tarjeta, DetalleCompra, ReservaLibroFisico, ReservaLibroDigital
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(LibroDigital)
admin.site.register(LibroFisico)
admin.site.register(Direccion)
admin.site.register(ReservaLibroFisico)
admin.site.register(ReservaLibroDigital)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Genero)
admin.site.register(Reseña)
admin.site.register(Tarjeta)