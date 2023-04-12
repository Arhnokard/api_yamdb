from rest_framework import serializers
import datetime as dt
from django.db.models import Avg

from reviews.models import Genre, Category, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('__all__')
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))
        if not rating:
            return 0
        return round(rating, 1)

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError(
                'Проверьте год создания произведения!')
        return value

    def validate_genre(self, value):
        genres = Genre.objects.all()
        if value not in genres:
            raise serializers.ValidationError(
                'Такого жанра не существует!')
        return value

    def validate_category(self, value):
        categories = Category.objects.all()
        if value not in categories:
            raise serializers.ValidationError(
                'Такой категории не существует!')
        return value
