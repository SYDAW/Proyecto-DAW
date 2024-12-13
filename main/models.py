from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from datetime import date, timedelta

# Modelo Usuario
class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Clientes"


# Modelo Autor
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="autores", null=True)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Autores"


# Modelo Genero
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Géneros"


# Modelo Libro
class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros', default=1)    
    generos = models.ManyToManyField(Genero, related_name='libros')
    descripcion = models.TextField()    
    disponibilidad = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="libros", null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Libros"


# Modelo LibroDigital
class LibroDigital(models.Model):
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE, related_name='digital')
    archivo = models.FileField(upload_to='libros_digitales/')
    precio = models.DecimalField(max_digits=12, decimal_places=2)


    def __str__(self):
        return self.libro.titulo

    class Meta:
        verbose_name_plural = "Libros Digitales"


# Modelo LibroFisico
class LibroFisico(models.Model):
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE, related_name='fisico')
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)


    def __str__(self):
        return self.libro.titulo

    class Meta:
        verbose_name_plural = "Libros Físicos"

# Modelo Direccion
class Direccion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='direcciones')
    calle = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.calle}, {self.ciudad}, {self.codigo_postal}, {self.pais}'

    class Meta:
        verbose_name_plural = "Direcciones"

# Modelo Tarjeta
class Tarjeta(models.Model):
    TIPO_CHOICES = [
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tarjeta')
    titular = models.CharField(max_length=100)
    numero = models.CharField(max_length=16, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    caducidad = models.DateField()

    def __str__(self):
        return f'{self.numero} - {self.usuario.username}'



# Modelo Reserva Libro Físico
class ReservaLibroFisico(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas_fisicas')
    libro = models.ForeignKey(LibroFisico, on_delete=models.CASCADE, related_name='reservas')
    tarjeta_reserva = models.ForeignKey(Tarjeta, on_delete=models.PROTECT, null=True, blank=True, related_name='reservas')
    fecha_reserva = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    fianza = models.DecimalField(max_digits=10, decimal_places=2) 
    fianza_devuelta = models.BooleanField(default=False) 
    estado_reserva = models.CharField(
        max_length=20,
        choices=[
            ('Activa', 'Activa'),
            ('Completada', 'Completada'),
            ('Sancionada', 'Sancionada'),
        ],
    )

    def devolver_libro(self, en_buenas_condiciones):
        """
        Maneja la devolución del libro.
        """
        if en_buenas_condiciones:
            self.fianza_devuelta = True  
        else:
            self.fianza_devuelta = False  
        self.estado_reserva = 'Completada'
        self.save()

    def verificar_vencimiento(self):
        """
        Verifica si han pasado 30 días sin devolución.
        """
        if not self.fecha_devolucion and (self.fecha_reserva + timedelta(days=30)) < date.today():
            self.estado_reserva = 'Sancionada'
            self.fianza_devuelta = False
            self.save()

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.libro.titulo} (Físico)"

    class Meta:
        verbose_name_plural = "Reservas libros fisicos"

# Reserva Libro Digital
class ReservaLibroDigital(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas_digitales')
    libro = models.ForeignKey(LibroDigital, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField()
    estado_reserva = models.CharField(
        max_length=20,
        choices=[
            ('Activa', 'Activa'),
            ('Expirada', 'Expirada'),
        ],
    )

    def verificar_acceso(self):
        """
        Verifica si la reserva ha expirado.
        """
        if self.fecha_expiracion < date.today():
            self.estado_reserva = 'Expirada'
            self.save()

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.libro.titulo} (Digital)"

    class Meta:
        verbose_name_plural = "Reservas libros digitales"


# Modelo Compra
class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='compras')
    fecha = models.DateField(auto_now_add=True)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2)
    direccion_envio = models.ForeignKey(Direccion, on_delete=models.PROTECT, related_name='compras')
    tarjeta_compra =  models.ForeignKey(Tarjeta, on_delete=models.PROTECT, related_name='compras')

    def __str__(self):
        return f'{self.usuario.username} - {self.fecha}'

    class Meta:
        verbose_name_plural = "Compras"


# Modelo detalle de compra
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Libro, on_delete=models.PROTECT) 
    formato = models.CharField(max_length=20, choices=[("Fisico", "Físico"), ("Digital", "Digital")])
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.titulo} - {self.cantidad} x {self.precio_unitario}€"


# Modelo Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username}'

    class Meta:
        verbose_name_plural = "Carritos"

# Modelo ItemCarrito
class ItemCarrito(models.Model):
    FORMATO_CHOICES = [
        ('Fisico', 'Físico'),
        ('Digital', 'Digital'),
    ]

    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.titulo} ({self.formato})'

    class Meta:
        verbose_name_plural = "Items del Carrito"



# Modelo Reseña
class Reseña(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reseñas')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='reseñas')
    comentario = models.TextField()
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.libro.titulo}'

    class Meta:
        unique_together = ('usuario', 'libro')
        verbose_name_plural = "Reseñas"


