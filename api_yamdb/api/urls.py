from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet


router = DefaultRouter()
router.register('titles/(?P<post_id>\d+)/rewiews',
                ReviewViewSet, basename='rewiews')
router.register('titles/(?P<post_id>\d+)/rewiews/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]
