import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


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
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        if obj.reviews.count()==0:
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username', default=serializers.CurrentUserDefault())
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all(),
                                               write_only=True, required=False, default=1)

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(),
                                               write_only=True, required=False)

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        model = Comment
