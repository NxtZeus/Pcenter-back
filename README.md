# PCenter - Backend

Este es el backend del proyecto PCenter, una aplicación de comercio electrónico desarrollada con Django y Django REST Framework.

## 🚀 Características

- API RESTful completa
- Autenticación basada en tokens
- Gestión de usuarios y roles
- Sistema de pedidos y productos
- Gestión de carrito de compras
- CORS configurado para desarrollo y producción

## 🛠️ Tecnologías

- Python 3.11
- Django 5.0.4
- Django REST Framework 3.15.1
- PostgreSQL
- Gunicorn
- WhiteNoise
- django-cors-headers

## 📋 Requisitos Previos

- Python 3.11 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [carpeta-con-repositorio-clonado]
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
SECRET_KEY=tu_clave_secreta
DATABASE_URL=tu_url_de_base_de_datos
```

5. Aplicar migraciones:
```bash
python manage.py migrate
```

6. Crear un superusuario:
```bash
python manage.py createsuperuser
```

## 🚀 Ejecución

Para desarrollo local:
```bash
python manage.py runserver
```

Para producción:
```bash
gunicorn backend.wsgi
```

## 📚 Estructura del Proyecto

```
tfg-backend/
├── api/                    # Aplicación principal
│   ├── admin.py           # Configuración del admin
│   ├── models.py          # Modelos de datos
│   ├── serializers.py     # Serializadores
│   ├── views.py           # Vistas de la API
│   └── urls.py            # URLs de la API
├── backend/               # Configuración del proyecto
│   ├── settings.py        # Configuración
│   └── urls.py           # URLs principales
├── media/                 # Archivos multimedia
├── requirements.txt       # Dependencias
└── manage.py             # Script de gestión
```

## 🔐 Autenticación

La API utiliza autenticación basada en tokens. Para acceder a los endpoints protegidos, incluye el token en el header:

```
Authorization: Token <tu_token>
```

## 🌐 Endpoints Principales

- `/api/auth/` - Autenticación
- `/api/usuarios/` - Gestión de usuarios
- `/api/productos/` - Gestión de productos
- `/api/pedidos/` - Gestión de pedidos
- `/api/carrito/` - Gestión del carrito

## 🧪 Testing

Para ejecutar las pruebas:
```bash
python manage.py test
```
