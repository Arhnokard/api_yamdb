from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                    CommentViewSet, ReviewViewSet, UsersViewSet,
                    APIGetToken, APISignup)


router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(r'^titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews'),
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
),
router_v1.register('users', UsersViewSet)


urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
