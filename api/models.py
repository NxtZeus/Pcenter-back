from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ('cliente', 'Cliente'),
    ('administrador', 'Administrador'),
    # Add more roles as needed
)

METODOS_PAGO = (
    ('efectivo', 'Efectivo'),
    ('tarjeta_credito', 'Tarjeta de Crédito'),
    ('tarjeta_debito', 'Tarjeta de Débito'),
    # Add more payment methods as needed
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

class Usuario(AbstractUser):

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='custom_user_groups',  # Change here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Change here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    codigo_postal = models.IntegerField()
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=ROLES)

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    direccion_envio = models.CharField(max_length=255)
    direccion_facturacion = models.CharField(max_length=255)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)  # Cambiado de enum a CharField
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
