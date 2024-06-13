from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import *

class ImagenProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ImagenProducto, que maneja las imágenes de los productos.
    """
    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen']

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Producto. Incluye un nested serializer para las imágenes del producto.
    """
    imagenes = ImagenProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario, que maneja la información del usuario.
    """
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'direccion', 
            'ciudad', 'pais', 'codigo_postal', 'telefono', 'is_active', 'is_staff', 'is_superuser'
        ]

class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Pedido. Incluye un nested serializer para el cliente (usuario).
    """
    cliente = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo DetallePedido. Incluye nested serializers para el pedido y el producto.
    """
    pedido = PedidoSerializer(read_only=True)
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetallePedido
        fields = '__all__'

class ProductoCarritoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ProductoCarrito. Incluye un nested serializer para el producto.
    """
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ProductoCarrito
        fields = ['id', 'producto', 'cantidad']

class CarritoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Carrito. Incluye nested serializers para el cliente y los productos en el carrito.
    """
    cliente = UsuarioSerializer(read_only=True)
    productos_carrito = ProductoCarritoSerializer(many=True, read_only=True, source='productocarrito_set')

    class Meta:
        model = Carrito
        fields = '__all__'
