from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ModeloTests(TestCase):
    def setUp(self):
        # Crea instancias de modelos para las pruebas
        self.usuario = Usuario.objects.create_user(email='test@example.com', password='testpassword', codigo_postal=12345, username='testuser')
        self.producto = Producto.objects.create(nombre_producto='Test Product', categoria='ordenadores', marca='Test Brand', descripcion='Test Description', precio=99.99, stock=10)
        self.pedido = Pedido.objects.create(cliente=self.usuario, fecha_pedido='2024-06-13', direccion_envio='Test Address', direccion_facturacion='Test Address', metodo_pago='tarjeta_credito', precio_total=99.99, estado_pedido='pendiente')
        self.detalle_pedido = DetallePedido.objects.create(pedido=self.pedido, producto=self.producto, cantidad=1, precio_unidad=99.99)
        self.carrito = Carrito.objects.create(usuario=self.usuario)
        self.producto_carrito = ProductoCarrito.objects.create(carrito=self.carrito, producto=self.producto)

    def test_modelos_str(self):
        # Verifica que los métodos __str__ de los modelos devuelvan los valores esperados
        self.assertEqual(str(self.usuario), self.usuario.email)
        self.assertEqual(str(self.producto), self.producto.nombre_producto)
        self.assertEqual(str(self.pedido), f"Pedido de {self.pedido.cliente}")
        self.assertEqual(str(self.detalle_pedido), f"Detalle del pedido {self.detalle_pedido.pedido.id} (Producto: {self.detalle_pedido.producto.nombre_producto}) - Cantidad: {self.detalle_pedido.cantidad} - Precio: {self.detalle_pedido.precio_unidad}")
        self.assertEqual(str(self.carrito), self.carrito.usuario.username)
        self.assertEqual(str(self.producto_carrito), f"{self.producto_carrito.cantidad} x {self.producto_carrito.producto.nombre_producto} en el carrito de {self.producto_carrito.carrito.usuario.username}")

    def test_usuario_manager(self):
        # Prueba el funcionamiento del UsuarioManager personalizado
        usuario_normal = Usuario.objects.create_user(email='normal@example.com', password='testpassword', codigo_postal=12345, username='normaluser')
        self.assertFalse(usuario_normal.is_staff)
        self.assertFalse(usuario_normal.is_superuser)

    def test_pedido_total(self):
        # Calcula el precio total de un pedido y verifica que sea correcto
        self.pedido.precio_total = self.detalle_pedido.cantidad * self.detalle_pedido.precio_unidad
        self.pedido.save()
        self.assertEqual(self.pedido.precio_total, 99.99)


class APITests(APITestCase):
    def setUp(self):
        # Crea un usuario y obtén un token de autenticación para las pruebas
        self.user = Usuario.objects.create_user(email='testuser@example.com', password='testpassword', codigo_postal=12345, username='testuser')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Crea datos de prueba adicionales
        self.producto1 = Producto.objects.create(nombre_producto='Product 1', categoria='ordenadores', marca='Brand A', descripcion='Description 1', precio=50.00, stock=5)
        self.producto2 = Producto.objects.create(nombre_producto='Product 2', categoria='moviles', marca='Brand B', descripcion='Description 2', precio=80.00, stock=3)

    def test_list_usuarios(self):
        # Prueba la vista de listado de usuarios (solo accesible para superusuarios)
        url = reverse('list-usuarios')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Asumiendo que el usuario de prueba es superusuario

    def test_get_usuario_detail(self):
        # Prueba la vista de detalle de usuario
        url = reverse('detailed-usuarios')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_list_productos(self):
        # Prueba la vista de listado de productos
        url = reverse('list-productos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Debería haber 2 productos creados en setUp

    def test_producto_search(self):
        # Prueba la búsqueda de productos
        url = reverse('producto-search') + '?search=Product'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Debería encontrar 2 productos
