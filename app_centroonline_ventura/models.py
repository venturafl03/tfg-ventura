# app_centroonline_ventura/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class UsuarioPersonalizado(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('CLIENTE', 'Cliente'),
        ('EMPLEADO', 'Empleado'),
        ('ADMIN', 'Administrador'),
    ]
    
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='CLIENTE')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_tipo_usuario_display()}"

# Modelos para Ventura Motors (Concesionario)

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    pais_origen = models.CharField(max_length=50)
    año_fundacion = models.IntegerField()
    logo = models.ImageField(upload_to='marcas/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    TIPO_VEHICULO_CHOICES = [
        ('SEDAN', 'Sedán'),
        ('SUV', 'SUV'),
        ('PICKUP', 'Pickup'),
        ('DEPORTIVO', 'Deportivo'),
        ('ELECTRICO', 'Eléctrico'),
        ('HIBRIDO', 'Híbrido'),
    ]
    
    TRANSMISION_CHOICES = [
        ('AUTOMATICO', 'Automático'),
        ('MANUAL', 'Manual'),
        ('CVT', 'CVT'),
    ]
    
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_VEHICULO_CHOICES)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    kilometraje = models.IntegerField()
    color = models.CharField(max_length=30)
    transmision = models.CharField(max_length=10, choices=TRANSMISION_CHOICES)
    motor = models.CharField(max_length=50)
    potencia = models.IntegerField(help_text="Caballos de fuerza")
    descripcion = models.TextField()
    imagen_principal = models.ImageField(upload_to='vehiculos/')
    disponible = models.BooleanField(default=True)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    destacado = models.BooleanField(default=False)
    reservado = models.BooleanField(default=False)
    reservado_por = models.ForeignKey(UsuarioPersonalizado, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_reserva = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        verbose_name_plural = "Vehículos"
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.año}"


class Reserva(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comentarios = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Reserva de {self.nombre} para {self.vehiculo}'
    
    class Meta:
        verbose_name = 'Reserva de vehículo'
        verbose_name_plural = 'Reservas de vehículos'
        ordering = ['-fecha_creacion']
class ImagenVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='vehiculos/galeria/')
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']


class TestDrive(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_test = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Test Drive - {self.vehiculo} - {self.usuario}"


# Modelos para la Baguetería Ventura

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=30, blank=True, help_text="Clase de Font Awesome para el icono")

    class Meta:
        verbose_name_plural = "Categorías de Productos(bagueteria)"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    TIPO_PAN_CHOICES = [
        ('TRADICIONAL', 'Tradicional'),
        ('INTEGRAL', 'Integral'),
        ('SIN_GLUTEN', 'Sin Gluten'),
    ]
    
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tipo_pan = models.CharField(max_length=15, choices=TIPO_PAN_CHOICES, blank=True, null=True)
    imagen = models.ImageField(upload_to='bagueteria/')
    disponible = models.BooleanField(default=True)
    ingredientes = models.TextField(blank=True)
    tiempo_preparacion = models.IntegerField(help_text="Tiempo en minutos", blank=True, null=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Producto(bagueteria)"

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PREPARACION', 'En preparación'),
        ('LISTO', 'Listo para recoger'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Pedido(bagueteria)"

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.pedido.total = sum(d.subtotal for d in self.pedido.detalles.all())
        self.pedido.save()

    def __str__(self):
        return f"{self.cantidad}x {self.producto}"
    
    class Meta:
        verbose_name_plural = "Detalle de pedido (bagueteria)"


# Modelos para Ventura Market

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class ProductoMarket(models.Model):
    CATEGORIA_CHOICES = [
        ('ALIMENTOS', 'Alimentos'),
        ('BEBIDAS', 'Bebidas'),
        ('LIMPIEZA', 'Limpieza'),
        ('OTROS', 'Otros'),
    ]
    
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='market/', blank=True, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return self.nombre


# Modelo para Home Build (si aplica)

class ProyectoConstruccion(models.Model):
    ESTADO_CHOICES = [
        ('PLANIFICACION', 'En planificación'),
        ('CONSTRUCCION', 'En construcción'),
        ('FINALIZADO', 'Finalizado'),
        ('ENTREGADO', 'Entregado'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_estimada_fin = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PLANIFICACION')
    imagen_principal = models.ImageField(upload_to='construccion/')
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.nombre


class ImagenProyecto(models.Model):
    proyecto = models.ForeignKey(ProyectoConstruccion, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='construccion/galeria/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']



#perfumeria 
class Perfumeria(models.Model):
    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('U', 'Unisex')
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    imagen = models.ImageField(upload_to='perfumerias/')
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre 

# libros 
# centroonline/models.py

from django.db import models

# Modelo simplificado para productos de la tienda
class ProductoEstudio(models.Model):
    GENERO_LIBRO = (
        ('ficcion', 'Ficción'),
        ('no_ficcion', 'No Ficción'),
        ('educativo', 'Educativo'),
        ('ciencia', 'Ciencia'),
        ('historia', 'Historia'),
        ('fantasia', 'Fantasía'),
        ('romance', 'Romance'),
        ('arte', 'Arte'),
        ('misterio', 'Misterio'),
        ('infantil', 'Infantil'),
    )
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, choices=GENERO_LIBRO)
    imagen = models.ImageField(upload_to='productos_estudio/')
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Libreria"

# viajes 
class Viaje(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    destino = models.CharField(max_length=255)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
