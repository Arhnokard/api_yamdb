from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Сокращенное название жанра',
                            unique=True, max_length=50)


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Сокращенное название категории',
                            unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выхода')
    rating = models.IntegerField('Рейтинг приозведения')
    description = models.TextField('Описание произведения',
                                   blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', on_delete=models.SET_NULL,
        blank=True, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='titles')


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    '''Модель отзывов на произведения'''
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='rewiews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='rewiews')
    score = models.IntegerField(
        validators=[MaxValueValidator(10, 'Оценка может быть от 1 до 10'),
                    MinValueValidator(1, 'Оценка  может быть от 1 до 10')]
    )
    pub_date = models.TimeField('Дата отзыва',auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author')
        ]

