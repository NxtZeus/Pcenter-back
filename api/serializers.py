from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Producto, Pedido, DetallePedido, Reembolso, Reseña, Usuario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'correo_electronico', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'telefono', 'rol', 'is_active', 'is_staff']

class PedidoSerializer(serializers.ModelSerializer):
    cliente = UsuarioSerializer(read_only=True, many=True)
    
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetallePedido
        fields = '__all__'

class ReembolsoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)

    class Meta:
        model = Reembolso
        fields = '__all__'

class ReseñaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    cliente = UsuarioSerializer(read_only=True)

    class Meta:
        model = Reseña
        fields = '__all__'
