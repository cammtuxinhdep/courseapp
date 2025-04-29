# File urls.py - Định nghĩa các đường dẫn URL cho ứng dụng Django
from django.contrib import admin
from django.urls import include, re_path, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Cấu hình Swagger API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1',
        description="APIs for CourseApp",
        contact=openapi.Contact(email="2251052132tu@ou.edu.vn"),
        license=openapi.License(name="Võ Minh Cẩm Tú@2025"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Danh sách đường dẫn URL
urlpatterns = [
    path('', include('courses.urls')),  # Bao gồm các URL của ứng dụng courses
    path('admin/', admin.site.urls),  # URL cho trang admin
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),  # URL cho CKEditor
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]