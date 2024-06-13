from django.urls import path
from .views import *

urlpatterns = [
    # Rutas para la gestión de usuarios
    path('usuarios/', ListUsuarios.as_view(), name='list-usuarios'),
    path('usuarios/detalles/', DetailedUsuarios.as_view(), name='detailed-usuarios'),
    path('usuario/pedidos/', UsuarioPedidosView.as_view(), name='usuario-pedidos'),

    # Rutas para la gestión de productos
    path('productos/', ListProductos.as_view(), name='list-productos'),
    path('productos/<int:pk>/', DetailedProductos.as_view(), name='detailed-productos'),
    path('pedidos/<int:pedidoId>/cancelar/', cancelarPedido, name='cancelar-pedido'),
    path('search/', ProductoSearchView.as_view(), name='producto-search'),
    path('categorias/', list_categorias, name='list-categorias'),
    path('añadir-producto/', añadir_producto, name='añadir-producto'),
    path('modificar-producto/<int:pk>/', modificar_producto, name='modificar-producto'),
    path('eliminar-producto/<int:pk>/', eliminar_producto, name='eliminar-producto'),
    
    # Rutas para la gestión de pedidos
    path('pedidos/', ListPedidos.as_view(), name='list-pedidos'),
    path('pedidos/<int:pk>/', DetailedPedidos.as_view(), name='detailed-pedidos'),
    path('crear-pedido/', crear_pedido, name='crear-pedido'),
    path('modificar-pedido/<int:pk>/', modificar_pedido, name='modificar-pedido'),
    path('eliminar-pedido/<int:pk>/', eliminar_pedido, name='eliminar-pedido'),

    # Rutas para la gestión de detalles de pedidos
    path('detalles-pedidos/', ListDetallesPedidos.as_view(), name='list-detalles-pedidos'),
    path('detalles-pedidos/<int:pk>/', DetailedDetallesPedidos.as_view(), name='detailed-detalles-pedidos'),
    path('pago/', pago, name='pago'),

    # Rutas para la gestión de carritos
    path('carritos/', ListCarritos.as_view(), name='list-carritos'),
    path('carritos/<int:pk>/', DetailedCarritos.as_view(), name='detailed-carritos'),
    path('añadir-carrito/', AgregarAlCarrito.as_view(), name='añadir-carrito'),
    path('ver-carrito/', VerCarrito.as_view(), name='ver-carrito'),
    path('eliminar-carrito/<int:producto_id>/', QuitarDeCarrito.as_view(), name='eliminar-carrito'),
    path('productos-carrito/', ListProductosCarrito.as_view(), name='list-productos-carrito'),
    path('productos-carrito/<int:pk>/', DetailedProductosCarritos.as_view(), name='detailed-productos-carritos'),
    path('actualizar-carrito/', ActualizarCantidadCarrito.as_view(), name='actualizar-carrito'),

    # Rutas para la autenticación de usuarios
    path('registro/', registro, name='registro'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
