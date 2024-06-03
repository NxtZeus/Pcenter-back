from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', ListUsuarios.as_view()),
    path('usuarios/detalles/', DetailedUsuarios.as_view()),
    path('usuario/pedidos/', UsuarioPedidosView.as_view()),

    path('productos/', ListProductos.as_view()),
    path('productos/<int:pk>/', DetailedProductos.as_view()),
    path('search/', ProductoSearchView.as_view()),
    path('categorias/', list_categorias),
    path('añadir-producto/', añadir_producto),
    path('modificar-producto/<int:pk>/', modificar_producto),
    path('eliminar-producto/<int:pk>/', eliminar_producto),
    
    path('pedidos/', ListPedidos.as_view()),
    path('pedidos/<int:pk>/', DetailedPedidos.as_view()),
    path('crear-pedido/', crear_pedido),
    path('modificar-pedido/<int:pk>/', modificar_pedido),
    path('eliminar-pedido/<int:pk>/', eliminar_pedido),

    path('detalles-pedidos/', ListDetallesPedidos.as_view()),
    path('detalles-pedidos/<int:pk>/', DetailedDetallesPedidos.as_view()),
    path('pago/', pago),

    path('reembolsos/', ListReembolsos.as_view()),
    path('reembolsos/<int:pk>/', DetailedReembolsos.as_view()),

    path('carritos/', ListCarritos.as_view()),
    path('carritos/<int:pk>/', DetailedCarritos.as_view()),
    path('añadir-carrito/', AgregarAlCarrito.as_view()),
    path('ver-carrito/', VerCarrito.as_view()),
    path('eliminar-carrito/<int:producto_id>/', QuitarDeCarrito.as_view()),
    path('productos-carrito/', ListProductosCarrito.as_view()),
    path('productos-carrito/<int:pk>/', DetailedProductosCarritos.as_view()),
    path('actualizar-carrito/', ActualizarCantidadCarrito.as_view()),

    path('registro/', registro),
    path('login/', login),
    path('logout/', logout),
]