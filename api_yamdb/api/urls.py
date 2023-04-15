from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet, CommentViewSet,
                    ReviewViewSet, UsersViewSet, APIGetToken, APISignup)


router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('title/(?P<post_id>\d+)/rewiews',
                   ReviewViewSet, basename='rewiews'),
router.register('titles/(?P<post_id>\d+)/rewiews/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments'),
router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
