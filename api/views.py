from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from rest_framework.exceptions import NotFound

class ListUsuarios(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Usuario.objects.all()
        else:
            queryset = [user]
        return queryset

class DetailedUsuarios(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    def delete(self, request, *args, **kwargs):
        token = self.request.user
        token.delete()
        return super().delete(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # Hashear la contraseña si está presente en los datos de la solicitud
        if 'password' in request.data:
            user = self.request.user
            user.set_password(request.data['password'])
            user.save()
            request.data.pop('password')
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        # Hashear la contraseña si está presente en los datos de la solicitud
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            request.data.pop('password')
        return self.partial_update(request, *args, **kwargs)

class ListProductos(generics.ListCreateAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Pedido.objects.filter(usuario=user)

class DetailedProductos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
def añadir_producto(request):
    if request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_producto(request, pk):
    if request.method == 'DELETE':
        producto = get_object_or_404(Producto, id=pk)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def modificar_producto(request, pk):
    if request.method == 'PUT':
        producto = get_object_or_404(Producto, id=pk)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListPedidos(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetailedPedidos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

@api_view(['POST'])
def crear_pedido(request):
    serializer = PedidoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def modificar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    serializer = PedidoSerializer(pedido, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DetailedReseñas(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(['POST'])
def crear_reseña(request):
    serializer = ReseñaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def modificar_reseña(request, pk):
    reseña = get_object_or_404(Reseña, pk=pk)
    serializer = ReseñaSerializer(reseña, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, pk=reseña_id)
    
    # Verificar si el usuario es un administrador o el propietario de la reseña
    if request.user.is_staff or request.user == reseña.cliente:
        reseña.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "No tiene permiso para eliminar esta reseña."}, status=status.HTTP_403_FORBIDDEN)

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

class AgregarAlCarrito(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoCarritoSerializer

    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)
        producto = get_object_or_404(Producto, id=producto_id)

        # Verificar si el usuario tiene un carrito existente
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        # Asociar el carrito al usuario si es nuevo
        if created:
            carrito.usuario = request.user
            carrito.save()

        # Crear o actualizar el ProductoCarrito
        producto_carrito, created = ProductoCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            producto_carrito.cantidad += int(cantidad)
            producto_carrito.save()

        return Response(ProductoCarritoSerializer(producto_carrito).data, status=status.HTTP_201_CREATED)

class VerCarrito(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarritoSerializer

    def get_object(self):
        carrito, created = Carrito.objects.get_or_create(usuario=self.request.user)
        if not carrito.productocarrito_set.exists():
            raise NotFound("El carrito está vacío")
        return carrito

class QuitarDeCarrito(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        producto_id = self.kwargs.get('producto_id')  # Obtener el ID del producto de los parámetros de la URL

        producto = get_object_or_404(Producto, id=producto_id)

        carrito = get_object_or_404(Carrito, usuario=request.user)
        producto_carrito = get_object_or_404(ProductoCarrito, carrito=carrito, producto=producto)
        producto_carrito.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

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
    update_last_login(None, user)
    if not user.check_password(request.data['password']):
        return Response({'details': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)
    return Response({'pepito': token.key, 'user' : serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'details': 'Logged out'}, status=status.HTTP_200_OK)