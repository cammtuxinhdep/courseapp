from rest_framework.pagination import PageNumberPagination

# Custom paginator cho Course
class CoursePagination(PageNumberPagination):
    page_size = 1  # Số lượng items mỗi trang