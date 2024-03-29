from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class UserManager(models.Manager):
    def create(self, **kwargs):
        user = User(**kwargs)
        if kwargs.get('role') == 'admin':
            user.is_staff = True
        user.save()
        return user

    def update(self, instance, **kwargs):
        if 'username' in kwargs:
            instance.username = kwargs['username']
        if 'email' in kwargs:
            instance.email = kwargs['email']
        if 'role' in kwargs:
            instance.role = kwargs['role']
            if kwargs.get('role') == 'admin':
                instance.is_staff = True
            else:
                instance.is_staff = False
        if 'bio' in kwargs:
            instance.bio = kwargs['bio']
        if 'first_name' in kwargs:
            instance.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            instance.last_name = kwargs['last_name']
        instance.save()
        return instance


class CreateUserManager(UserManager):
    def create_user(self, username, email, **extra_fields):
        if extra_fields['role'] == 'admin':
            extra_fields.setdefault('is_staff', True)
        user = self.model(username=username,
                          email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,
                         password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        user = self.model(username=username,
                          email=email, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        default='XXXX'
    )

    objects = CreateUserManager()

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Сокращенное название жанра',
                            unique=True, max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Сокращенное название категории',
                            unique=True, max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выхода')
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                   blank=True, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(10, 'Оценка может быть от 1 до 10'),
                    MinValueValidator(1, 'Оценка  может быть от 1 до 10')]
    )
    pub_date = models.TimeField('Дата отзыва', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.TimeField('Дата комментария', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
