import datetime as dt

from django.db.models import Avg
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core import validators

from reviews.models import Genre, Category, Title, Review, User, Comment
from reviews.validators import validate_username


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def create(self, validated_data):
        staff = False
        if 'role' in self.initial_data:
            if 'admin' == validated_data['role']:
                staff = True
        user = User.objects.create(is_staff=staff, **validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.username)
        instance.first_name = validated_data.get('first_name',
                                                 instance.username)
        instance.last_name = validated_data.get('last_name',
                                                instance.username)
        instance.bio = validated_data.get('bio', instance.username)
        instance.role = validated_data.get('role', instance.username)
        if 'admin' == instance.role:
            instance.is_staff = True
        else:
            instance.is_staff = False
        instance.save()
        return instance


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


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(validate_username, validators.MaxLengthValidator(150),)
    )
    email = serializers.EmailField(
        validators=(validators.MaxLengthValidator(254),)
    )

    def validate(self, data):
        users = User.objects.all()
        for user in users:
            if data['username'] == user.username:
                if data['email'] == user.email:
                    return data
                raise ValidationError('Указан неверный email')
            if data['email'] == user.email:
                raise ValidationError('email занят')
        return data

    class Meta:
        model = User
        fields = ('email', 'username')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=(validators.MaxLengthValidator(50),
                    validators.RegexValidator(r'^[-a-zA-Z0-9_]+$'),
                    UniqueValidator(queryset=Genre.objects.all()))
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=(validators.MaxLengthValidator(50),
                    validators.RegexValidator(r'^[-a-zA-Z0-9_]+$'),
                    UniqueValidator(queryset=Category.objects.all()))
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if not (-1500 < value <= year):
            raise serializers.ValidationError(
                'Проверьте год создания произведения!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(), write_only=True, required=False
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id')
        )
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
