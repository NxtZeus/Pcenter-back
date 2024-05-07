from django.shortcuts import render
from api.models import *
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UsuarioView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
class PedidoView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

class DetallePedidoView(APIView):
    def get(self, request):
        detalles = DetallePedido.objects.all()
        serializer = DetallePedidoSerializer(detalles, many=True)
        return Response(serializer.data)

class ReembolsoView(APIView):
    def get(self, request):
        reembolsos = Reembolso.objects.all()
        serializer = ReembolsoSerializer(reembolsos, many=True)
        return Response(serializer.data)

class ReseñaView(APIView):
    def get(self, request):
        reseñas = Reseña.objects.all()
        serializer = ReseñaSerializer(reseñas, many=True)
        return Response(serializer.data)