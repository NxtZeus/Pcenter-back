from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from rest_framework.exceptions import NotFound
from django.contrib.auth import authenticate
from django.db.models import Sum
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

class ListUsuarios(generics.ListCreateAPIView):
    """
    Lista y crea usuarios. Los usuarios solo pueden ver su propia información, a menos que sean superusuarios.
    """
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
    """
    Recupera, actualiza y elimina un usuario específico.
    """
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'password' in request.data and request.data['password']:
            user.set_password(request.data['password'])
            user.save()

        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class UsuarioPedidosView(generics.ListAPIView):
    """
    Lista los pedidos del usuario autenticado.
    """
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user)

class ListProductos(generics.ListCreateAPIView):
    """
    Lista y crea productos. Permite cargar imágenes asociadas al producto.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        data = request.data
        imagenes = request.FILES.getlist('imagenes')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        producto = serializer.save()

        for imagen in imagenes:
            ImagenProducto.objects.create(producto=producto, imagen=imagen)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "request": self.request
        })
        return context

class DetailedProductos(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, actualiza y elimina un producto específico.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class ProductoSearchView(generics.ListAPIView):
    """
    Permite la búsqueda de productos por nombre, descripción, categoría y marca.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre_producto', 'descripcion', 'categoria', 'marca']

@api_view(['GET'])
def list_categorias(request):
    """
    Lista todas las categorías de productos distintas.
    """
    categorias = Producto.objects.values_list('categoria', flat=True).distinct()
    return Response(categorias)

@api_view(['POST'])
def añadir_producto(request):
    """
    Añade un nuevo producto a la base de datos.
    """
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_producto(request, pk):
    """
    Elimina un producto específico de la base de datos.
    """
    producto = get_object_or_404(Producto, id=pk)
    producto.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def modificar_producto(request, pk):
    """
    Modifica un producto específico de la base de datos.
    """
    producto = get_object_or_404(Producto, id=pk)
    serializer = ProductoSerializer(producto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListPedidos(generics.ListCreateAPIView):
    """
    Lista y crea pedidos.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetailedPedidos(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, actualiza y elimina un pedido específico.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

@api_view(['POST'])
def crear_pedido(request):
    """
    Crea un nuevo pedido.
    """
    serializer = PedidoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def modificar_pedido(request, pk):
    """
    Modifica un pedido específico.
    """
    pedido = get_object_or_404(Pedido, pk=pk)
    serializer = PedidoSerializer(pedido, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancelarPedido(request, pedidoId):
    """
    Cancela un pedido específico y restaura el stock de los productos asociados.
    """
    try:
        pedido = Pedido.objects.get(pk=pedidoId)
        
        # Verifica si el usuario autenticado es el propietario del pedido
        if pedido.cliente != request.user:
            return Response({"detail": "No tienes permiso para cancelar este pedido"}, status=status.HTTP_403_FORBIDDEN)

        if pedido.estado_pedido in ['cancelado', 'enviado']:
            return Response({'error': f'El pedido no se puede cancelar porque está en estado {pedido.estado_pedido}.'}, status=status.HTTP_400_BAD_REQUEST)

        pedido.estado_pedido = 'cancelado'
        pedido.save()

        # Restaurar el stock de los productos
        detalles_pedido = DetallePedido.objects.filter(pedido=pedido)
        for detalle in detalles_pedido:
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()

        return Response({'mensaje': 'Pedido cancelado y stock restaurado correctamente.'}, status=status.HTTP_200_OK)
    except Pedido.DoesNotExist:
        return Response({'error': 'No se encontró el pedido.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def eliminar_pedido(request, pk):
    """
    Elimina un pedido específico.
    """
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pago(request):
    """
    Procesa el pago de los productos en el carrito del usuario autenticado y crea un pedido.
    """
    usuario = request.user
    carrito = get_object_or_404(Carrito, usuario=usuario)
    
    if not carrito.productocarrito_set.exists():
        return Response({'detail': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)
    
    total_precio = sum(item.producto.precio * item.cantidad for item in carrito.productocarrito_set.all())
    
    metodo_pago = request.data.get('metodo_pago', 'tarjeta_credito')
    if metodo_pago not in dict(METODOS_PAGO):
        return Response({'detail': 'Método de pago no válido'}, status=status.HTTP_400_BAD_REQUEST)
    
    pedido = Pedido.objects.create(
        cliente=usuario,
        fecha_pedido=timezone.now().date(),
        direccion_envio=usuario.direccion,
        direccion_facturacion=usuario.direccion,
        metodo_pago=metodo_pago,
        precio_total=total_precio,
        estado_pedido='pendiente'
    )
    
    for item in carrito.productocarrito_set.all():
        if item.producto.stock < item.cantidad:
            return Response({'detail': 'Producto sin stock suficiente'}, status=status.HTTP_400_BAD_REQUEST)
        
        item.producto.stock -= item.cantidad
        item.producto.save()
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unidad=item.producto.precio
        )
    
    carrito.productocarrito_set.all().delete()

    return Response({'detail': 'Pedido creado con éxito'}, status=status.HTTP_201_CREATED)

class ListDetallesPedidos(generics.ListCreateAPIView):
    """
    Lista y crea detalles de pedidos.
    """
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class DetailedDetallesPedidos(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, actualiza y elimina un detalle de pedido específico.
    """
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class ListCarritos(generics.ListCreateAPIView):
    """
    Lista y crea carritos.
    """
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class DetailedCarritos(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, actualiza y elimina un carrito específico.
    """
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class ListProductosCarrito(generics.ListCreateAPIView):
    """
    Lista y crea productos en el carrito.
    """
    queryset = ProductoCarrito.objects.all()
    serializer_class = ProductoCarritoSerializer

class DetailedProductosCarritos(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, actualiza y elimina un producto específico del carrito.
    """
    queryset = ProductoCarrito.objects.all()
    serializer_class = ProductoCarritoSerializer

class AgregarAlCarrito(generics.CreateAPIView):
    """
    Agrega productos al carrito del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoCarritoSerializer

    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)
        producto = get_object_or_404(Producto, id=producto_id)

        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        if created:
            carrito.usuario = request.user
            carrito.save()

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
    """
    Muestra el carrito del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CarritoSerializer

    def retrieve(self, request, *args, **kwargs):
        carrito = self.get_object()

        serializer = self.get_serializer(carrito)
        data = serializer.data

        return Response(data)

    def get_object(self):
        carrito, created = Carrito.objects.get_or_create(usuario=self.request.user)
        if not carrito.productocarrito_set.exists():
            raise NotFound("El carrito está vacío")
        return carrito

class ActualizarCantidadCarrito(generics.UpdateAPIView):
    """
    Actualiza la cantidad de un producto en el carrito del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductoCarritoSerializer

    def patch(self, request, *args, **kwargs):
        producto_id = request.data.get('producto_id')
        nueva_cantidad = request.data.get('cantidad')
        if nueva_cantidad is None or nueva_cantidad <= 0:
            return Response({"detail": "Cantidad inválida"}, status=status.HTTP_400_BAD_REQUEST)

        producto = get_object_or_404(Producto, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        producto_carrito = get_object_or_404(ProductoCarrito, carrito=carrito, producto=producto)
        
        if nueva_cantidad > producto.stock:
            return Response({"detail": 'Producto no disponible en stock'}, status=status.HTTP_400_BAD_REQUEST)

        producto_carrito.cantidad = nueva_cantidad
        producto_carrito.save()

        return Response(ProductoCarritoSerializer(producto_carrito).data)

class QuitarDeCarrito(generics.DestroyAPIView):
    """
    Elimina un producto del carrito del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        producto_id = self.kwargs.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        producto_carrito = get_object_or_404(ProductoCarrito, carrito=carrito, producto=producto)
        producto_carrito.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def registro(request):
    """
    Registra un nuevo usuario.
    """
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
@permission_classes([AllowAny])
def login(request):
    """
    Autentica a un usuario y devuelve un token de acceso.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        serializer = UsuarioSerializer(user)
        serializer_data = serializer.data
        serializer_data['token'] = token.key

        return Response(serializer_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    """
    Cierra la sesión del usuario autenticado eliminando su token de acceso.
    """
    if request.user.is_authenticated:
        try:
            request.user.auth_token.delete()
            return Response({'result': 'Sesión cerrada'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'result': 'Token no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'result': 'No autenticado'}, status=status.HTTP_401_UNAUTHORIZED)