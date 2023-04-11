from rest_framework.pagination import LimitOffsetPagination

from rest_framework import viewsets
from api.filters import TitleFilter
from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes =
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter
    