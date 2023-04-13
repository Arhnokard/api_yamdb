from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategoryViewSet, TitleViewSet, ReviewViewSet


router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('title/(?P<post_id>\d+)/rewiews', ReviewViewSet, basename='rewiews')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
