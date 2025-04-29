from django.urls import path, include  # Thêm các hàm path và include từ django.urls để định nghĩa URL
from rest_framework.routers import DefaultRouter  # DefaultRouter giúp tự động tạo các URL cho ViewSets

from . import views  # Import các views từ file views.py

# Khởi tạo DefaultRouter để dễ dàng đăng ký các ViewSet
router = DefaultRouter()

# Đăng ký các viewsets với router, mỗi ViewSet sẽ có một URL path tương ứng
router.register('categories', views.CategoryViewSet, basename='category')  # Đăng ký URL cho CategoryViewSet
router.register('courses', views.CourseViewSet, basename='course')  # Đăng ký URL cho CourseViewSet
router.register('lessons', views.LessonViewSet, basename='lesson')  # Đăng ký URL cho LessonViewSet
router.register('users', views.UserViewSet, basename='user')  # Đăng ký URL cho UserViewSet

# Danh sách các URL, bao gồm tất cả các URL được tạo ra bởi router
urlpatterns = [
    path('', include(router.urls)),  # Bao gồm tất cả các URL từ router
]
