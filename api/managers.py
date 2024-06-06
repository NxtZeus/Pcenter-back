from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario, donde el email es el identificador único para la autenticación.
    """

    def create_user(self, username, email, password, codigo_postal, **extra_fields):
        """
        Crear y guardar un usuario con el nombre de usuario, email, contraseña y código postal proporcionados.
        """
        if not username:
            raise ValueError('El campo de nombre de usuario es obligatorio.')
        if not email:
            raise ValueError('El campo de correo electrónico es obligatorio.')

        email = self.normalize_email(email)
        user = self.model(
            username=username, 
            email=email,
            codigo_postal=codigo_postal,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Crear y guardar un SuperUsuario con el email y la contraseña proporcionados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
