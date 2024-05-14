from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):

    def create_user(self, username, email, password, direccion, ciudad, pais, codigo_postal, telefono, rol, **extra_fields):
        if not username:
            raise ValueError('El campo de nombre de usuario es obligatorio.')
        if not email:
            raise ValueError('El campo de correo electrónico es obligatorio.')

        email = self.normalize_email(email)
        user = self.model(
            username=username, 
            email=email,
            direccion=direccion,
            ciudad=ciudad,
            pais=pais,
            codigo_postal=codigo_postal,
            telefono=telefono,
            rol=rol,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, codigo_postal, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(username, email, password, codigo_postal **extra_fields)
