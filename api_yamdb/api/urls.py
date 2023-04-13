from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet


router = DefaultRouter()
router.register('title/(?P<post_id>\d+)/rewiews', ReviewViewSet, basename='rewiews')


urlpatterns = [
    path('v1/', include(router.urls)),
]
