from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):  #для токенов каждому юзеру
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('The given email must be set!') #проверка на наличие почты
        email = self.normalize_email(email=email) #проверка написания почты
        user = self.model(email=email, **kwargs) # *kwargs принимает доп параметры для юзера
        user.create_activation_code() #создание и отправка кода активации на почту
        user.set_password(password) #установка пароля
        user.save(using=self._db) #сохранение в базе данных
        return user

    def create_user(self, email, password, **kwargs): #добавление дополнительных параметров #создание юзеров
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs): #создание админа
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have status is_staff=True!')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have status is_staff=True!')
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField('email.address', unique=True)
    password = models.CharField(max_length=255)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/default_avatar.jpg')
    is_active = models.BooleanField(_("active"), default=False, help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."),
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    def create_activation_code(self): #
        import uuid #библиотека которая пишет активационный код длиной 255 символов
        code = str(uuid.uuid4()) #сам код в переменной code
        self.activation_code = code
