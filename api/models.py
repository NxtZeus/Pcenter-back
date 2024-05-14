from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin
from .managers import UsuarioManager

ROLES = (
    ('cliente', 'Cliente'),
    ('administrador', 'Administrador'),
)

METODOS_PAGO = (
    ('efectivo', 'Efectivo'),
    ('tarjeta_credito', 'Tarjeta de Crédito'),
)

ESTADOS_PEDIDO = (
    ('pendiente', 'Pendiente'),
    ('procesando', 'Procesando'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
    ('cancelado', 'Cancelado'),
)
# Categorias para productos, ordenadores(sobremesa y portatiles), mobiles, perifericos( ratones, teclados, auriculares, monitor, ), componentes de pc, accesorios, software
CATEGORIAS_PRODUCTO = (
    ('ordenadores', 'Ordenadores'),
    ('mobiles', 'Mobiles'),
    ('perifericos', 'Perifericos'),
    ('componentes', 'Componentes'),
    ('accesorios', 'Accesorios'),
    ('software', 'Software'),
)
    

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=255)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_PRODUCTO)
    marca = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True)

class Usuario(AbstractUser, PermissionsMixin):

     
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    codigo_postal = models.IntegerField()
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=50, choices=ROLES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'codigo_postal']

    objects = UsuarioManager()
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    direccion_envio = models.CharField(max_length=255)
    direccion_facturacion = models.CharField(max_length=255)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pedido = models.CharField(max_length=100, choices=ESTADOS_PEDIDO)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)

class Reembolso(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_reembolso = models.DateField()
    precio_reembolso = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255)

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    comentario = models.TextField()
    fecha_reseña = models.DateField()

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

class ProductoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)