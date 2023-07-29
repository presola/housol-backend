from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .viewset import *
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'token/auth/', obtain_jwt_token),
    path(r'token/refresh/', refresh_jwt_token),
    re_path(r'^register/', UserCreateViewSet.as_view(), name='user'),
    re_path(r'^list/', UserListViewSet.as_view(), name='user'),
    re_path(r'^detail/', UserDetailViewSet.as_view(), name='user_get'),
]
