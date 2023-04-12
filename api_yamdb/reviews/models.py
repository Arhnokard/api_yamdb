from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
