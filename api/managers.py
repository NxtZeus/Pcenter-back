from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):

    def create_user(self, username, email, password, codigo_postal, **extra_fields):
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
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super usuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Super usuario debe tener is_superuser=True.'))
            

        return self.create_user(username, email, password, **extra_fields)
