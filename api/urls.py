from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', UsuarioView.as_view()),
    path('pedidos/', PedidoView.as_view()),
    path('detalles/', DetallePedidoView.as_view()),
    path('reembolsos/', ReembolsoView.as_view()),
    path('reseñas/', ReseñaView.as_view()),
]