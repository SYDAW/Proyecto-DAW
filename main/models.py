from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

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


# Modelo Reserva
class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    libro = models.ForeignKey(LibroFisico, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField()
    estado_reserva = models.CharField(max_length=20, choices=[('Activa', 'Activa'), ('Completada', 'Completada'), ('Sancionada', 'Sancionada')])

    def __str__(self):
        return f'{self.usuario.username} - {self.libro.libro.titulo}'

    class Meta:
        verbose_name_plural = "Reservas"


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
        verbose_name_plural = "Reseñas"
