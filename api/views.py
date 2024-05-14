from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

class ListUsuarios(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class DetailedUsuarios(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ListProductos(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class DetailedProductos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ListPedidos(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetailedPedidos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class ListDetallesPedidos(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class DetailedDetallesPedidos(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class ListReembolsos(generics.ListCreateAPIView):
    queryset = Reembolso.objects.all()
    serializer_class = ReembolsoSerializer

class DetailedReembolsos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reembolso.objects.all()
    serializer_class = ReembolsoSerializer

class ListReseñas(generics.ListCreateAPIView):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer

class DetailedReseñas(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer

class ListCarritos(generics.ListCreateAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class DetailedCarritos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class ListProductosCarrito(generics.ListCreateAPIView):
    queryset = ProductoCarrito.objects.all()
    serializer_class = ProductoCarritoSerializer

class DetailedProductosCarritos(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductoCarrito.objects.all()
    serializer_class = ProductoCarritoSerializer

@api_view(['POST'])
def registro(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = Usuario.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user' : serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(Usuario, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({'details': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)
    return Response({'pepito': token.key, 'user' : serializer.data}, status=status.HTTP_200_OK)