from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from courses import serializers, paginators
from courses.models import Category, Courses, Lesson, User, Like


# ViewSet cho Category, dùng để hiển thị danh sách các Category
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)  # Lọc các Category có active=True
    serializer_class = serializers.CategorySerializer  # Sử dụng CategorySerializer để chuyển đổi dữ liệu


# ViewSet cho Course, cung cấp API để hiển thị danh sách Course và thêm chức năng tìm kiếm
class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Courses.objects.filter(active=True)  # Lọc các Course có active=True
    serializer_class = serializers.CourseSerializer  # Sử dụng CourseSerializer để chuyển đổi dữ liệu
    pagination_class = paginators.CoursePagination  # Sử dụng phân trang cho kết quả

    def get_queryset(self):
        queryset = self.queryset

        # Xử lý tìm kiếm theo tên khóa học
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(subject__icontains=q)

        # Lọc khóa học theo category_id nếu có tham số category_id
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    # Thêm hành động tùy chỉnh 'lessons' cho từng khóa học
    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        # Lấy danh sách các bài học của khóa học
        lessons = self.get_object().lesson_set.filter(active=True)
        # Trả về dữ liệu các bài học đã serialize
        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


# ViewSet cho Lesson, cho phép lấy chi tiết từng Lesson và các comment liên quan
class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    # Lấy danh sách các bài học đang hoạt động (active=True) và prefetch các tag liên quan để giảm truy vấn DB
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)

    # Sử dụng LessonDetailsSerializer để serialize dữ liệu chi tiết bài học
    serializer_class = serializers.LessonDetailsSerializer

    def get_permissions(self):
        # Nếu gọi action 'get_comments', 'like' bằng phương thức POST → yêu cầu phải đăng nhập
        if self.action in ['get_comments', 'like']  and self.request.method.__eq__("POST"):
            return [permissions.IsAuthenticated()]  # Trả về quyền IsAuthenticated
        return [permissions.AllowAny()]  # Các trường hợp còn lại thì ai cũng có thể truy cập (không yêu cầu login)

    # Action tùy chỉnh cho endpoint /lessons/{id}/comments với 2 method: GET và POST
    @action(methods=['get', 'post'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            # Tạo một Comment mới từ dữ liệu client gửi lên
            u = serializers.CommentSerializer(data={
                'content': request.data.get('content'),  # Nội dung comment
                'user': request.user.pk,  # ID user hiện tại (đã đăng nhập)
                'lesson': pk  # ID bài học (lấy từ URL)
            })

            # Kiểm tra dữ liệu hợp lệ, nếu sai thì raise exception 400
            u.is_valid(raise_exception=True)

            # Lưu comment mới vào DB
            c = u.save()

            # Trả về comment vừa tạo, kèm status HTTP 201 CREATED
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        else:
            # Nếu là GET → trả về danh sách comment của bài học có pk tương ứng
            comments = self.get_object().comment_set.select_related('user').filter(active=True)

            # Serialize danh sách comment và trả về với status HTTP 200 OK
            return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    # Tạo action tùy chỉnh với phương thức POST tại endpoint: /lessons/{id}/like
    @action(methods=['post'], detail=True, url_path='like')
    def like(self, request, pk):
        # Tìm hoặc tạo mới đối tượng Like dựa trên user hiện tại và lesson_id (pk)
        # Nếu đã tồn tại thì trả về đối tượng đó, nếu chưa thì tạo mới
        li, created = Like.objects.get_or_create(user=request.user, lesson_id=pk)

        # Nếu đối tượng Like đã tồn tại (không phải tạo mới)
        if not created:
            # Đảo trạng thái like: nếu đã like thì bỏ like, nếu chưa thì like
            li.active = not li.active

        # Lưu lại thay đổi vào DB
        li.save()

        # Trả về thông tin chi tiết của bài học (bao gồm số like cập nhật nếu serializer xử lý phần đó)
        # Vì mình tự viết hàm xử lí nên phải thêm context để truyền về đối tượng
        return Response(serializers.LessonDetailsSerializer(self.get_object(), context={'request':request}).data)

# ViewSet cho User, cho phép tạo mới user
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)  # Lọc các User có active=True
    serializer_class = serializers.UserSerializer  # Sử dụng UserSerializer để xử lý dữ liệu
    parser_classes = [MultiPartParser]  # Sử dụng khi cần xử lý file upload

    @action(
        methods=['get', 'patch'],
        url_path='current-user',  # Định nghĩa endpoint API là `/current-user/`
        detail=False,  # Không yêu cầu ID user, chỉ lấy user hiện tại
        permission_classes=[permissions.IsAuthenticated]  # Chỉ cho phép user đã đăng nhập sử dụng
    )
    def get_current_user(self, request):
        """
        API lấy thông tin của user hiện tại đang đăng nhập.
        Nếu request là PATCH → cập nhật thông tin user.
        Ngược lại → trả về thông tin user hiện tại ở dạng JSON thông qua UserSerializer.
        """

        if request.method.__eq__("PATCH"):  # Kiểm tra nếu method là PATCH (yêu cầu cập nhật)
            u = request.user  # Lấy đối tượng user hiện tại đang đăng nhập, bảo mật

            for key in request.data:  # Duyệt qua từng trường dữ liệu được gửi lên
                if key in ['first_name', 'last_name']:
                    setattr(u, key, request.data[key])  # Cập nhật tên hoặc họ
                elif key.__eq__('password'):
                    u.set_password(request.data[key])  # Đặt lại mật khẩu (phải dùng set_password để mã hóa)

            u.save()  # Lưu thay đổi vào database
            return Response(serializers.UserSerializer(u).data)  # Trả về dữ liệu user sau khi cập nhật
        else:
            return Response(serializers.UserSerializer(request.user).data)  # Trả về dữ liệu user nếu không phải PATCH
