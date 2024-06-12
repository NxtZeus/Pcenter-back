from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin
from .managers import UsuarioManager

# Métodos de pago disponibles
METODOS_PAGO = (
    ('tarjeta_credito', 'Tarjeta de Crédito'),
)

# Estados posibles para un pedido
ESTADOS_PEDIDO = (
    ('pendiente', 'Pendiente'),
    ('procesado', 'Procesado'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
    ('cancelado', 'Cancelado'),
)

# Categorías de productos
CATEGORIAS_PRODUCTO = (
    ('ordenadores', 'Ordenadores'),
    ('portatiles', 'Portátiles'),
    ('moviles', 'Moviles'),
    ('perifericos', 'Periféricos'),
    ('componentes', 'Componentes'),
    ('accesorios', 'Accesorios'),
)

class Producto(models.Model):
    """
    Modelo para los productos disponibles en la tienda.
    """
    nombre_producto = models.CharField(max_length=255)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_PRODUCTO)
    marca = models.CharField(max_length=255)
    descripcion = models.TextField()
    especificaciones = models.TextField(default='')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre_producto

class ImagenProducto(models.Model):
    """
    Modelo para las imágenes de los productos.
    """
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre_producto}"

class Usuario(AbstractUser, PermissionsMixin):
    """
    Modelo para los usuarios de la aplicación, extendiendo el modelo AbstractUser.
    """
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    codigo_postal = models.IntegerField()
    telefono = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'codigo_postal']

    objects = UsuarioManager()

class Pedido(models.Model):
    """
    Modelo para los pedidos realizados por los usuarios.
    """
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    direccion_envio = models.CharField(max_length=255)
    direccion_facturacion = models.CharField(max_length=255)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pedido = models.CharField(max_length=100, choices=ESTADOS_PEDIDO)

    def __str__(self):
        return f"Pedido de {self.cliente}"

class DetallePedido(models.Model):
    """
    Modelo para los detalles de un pedido específico.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)

class Carrito(models.Model):
    """
    Modelo para los carritos de compra de los usuarios.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username

class ProductoCarrito(models.Model):
    """
    Modelo para los productos dentro de un carrito de compra.
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
