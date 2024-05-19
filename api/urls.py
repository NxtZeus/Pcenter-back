from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('usuarios/', ListUsuarios.as_view()),
    path('usuarios/detalles/', DetailedUsuarios.as_view()),
    path('productos/', ListProductos.as_view()),
    path('productos/<int:pk>/', DetailedProductos.as_view()),
    path('pedidos/', ListPedidos.as_view()),
    path('pedidos/<int:pk>/', DetailedPedidos.as_view()),
    path('detalles_pedidos/', ListDetallesPedidos.as_view()),
    path('detalles_pedidos/<int:pk>/', DetailedDetallesPedidos.as_view()),
    path('reembolsos/', ListReembolsos.as_view()),
    path('reembolsos/<int:pk>/', DetailedReembolsos.as_view()),
    path('reseñas/', ListReseñas.as_view()),
    path('reseñas/<int:pk>/', DetailedReseñas.as_view()),
    path('carritos/', ListCarritos.as_view()),
    path('carritos/<int:pk>/', DetailedCarritos.as_view()),
    path('productos_carrito/', ListProductosCarrito.as_view()),
    path('productos_carrito/<int:pk>/', DetailedProductosCarritos.as_view()),
    path('register/', registro),
    path('login/', login),
    path('api-token-auth/', obtain_auth_token),
    path('add_to_cart/', AgregarAlCarrito.as_view()),
    path('view_cart/', VerCarrito.as_view()),
    path('remove_from_cart/<int:producto_id>/', QuitarDeCarrito.as_view()),
    path('añadir_producto/', añadir_producto),
    path('modificar_producto/<int:pk>/', modificar_producto),
    path('eliminar_producto/<int:pk>/', eliminar_producto),
]