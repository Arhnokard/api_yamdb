import datetime as dt

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
        user = User.objects.create(**validated_data)
        if user.is_admin:
            user.is_staff = True
            user.save()
        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if instance.is_admin:
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
        if User.objects.filter(username=data['username']).exists():
            user = User.objects.get(username=data['username'])
            if user.email == data['email']:
                return data
            else:
                raise ValidationError(
                    f'{data["email"]} не соответствует '
                    f'зарегистрированому на акаунте {user.username}'
                )
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError(f'{data["email"]} уже зарегистрирован, '
                                  'укажите другой email')
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
