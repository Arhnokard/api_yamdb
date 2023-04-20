import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Genre, Category, Title, Review, User, Comment


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = GenreField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return None
        rating = obj.reviews.aggregate(Avg('score'))
        return round(rating['score__avg'], 1)

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError(
                'Проверьте год создания произведения!')
        return value

    def validate_genre(self, value):
        genres = Genre.objects.all()
        for item in value:
            if item not in genres:
                raise serializers.ValidationError(
                    'Такого жанра не существует!'
                )
        return value

    def validate_category(self, value):
        categories = Category.objects.all()
        if value not in categories:
            raise serializers.ValidationError(
                'Такой категории не существует!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),write_only=True, required=False
    )

    def validate(self, data):
            request = self.context['request']
            author = request.user
            title = get_object_or_404(Title, id=self.context['view'].kwargs.get('title_id'))
            if request.method == 'POST':
                if Review.objects.filter(title=title, author=author).exists():
                    raise ValidationError('Вы не можете добавить более'
                                        'одного отзыва на произведение')
            return data

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), write_only=True, required=False
    )

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        model = Comment
