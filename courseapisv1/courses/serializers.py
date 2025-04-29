from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from courses.models import Category, Courses, Lesson, Tag, User, Comment


# Serializer cho Category, dùng để chuyển đổi dữ liệu từ và đến các đối tượng Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Sử dụng model Category
        fields = ['id', 'name']  # Chỉ serialize các trường 'id' và 'name'


# Lớp cơ sở cho các serializer có chứa trường 'image' để dễ dàng chuyển đổi dữ liệu ảnh
class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Gọi hàm to_representation của lớp cha (ModelSerializer)
        data = super().to_representation(instance)
        # Thêm đường dẫn ảnh vào data (nếu có)
        data['image'] = instance.image.url
        return data


# Serializer cho Course, kế thừa từ ItemSerializer
class CourseSerializer(ItemSerializer):
    class Meta:
        model = Courses  # Sử dụng model Courses
        fields = ['id', 'subject', 'image', 'created_date', 'category_id']  # Chọn các trường cần hiển thị


# Serializer cho Lesson, kế thừa từ ItemSerializer
class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson  # Sử dụng model Lesson
        fields = ['id', 'subject', 'image', 'created_date']  # Các trường cần serialize


# Serializer cho Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag  # Sử dụng model Tag
        fields = ['id', 'name']  # Serialize id và name


# Serializer cho chi tiết Lesson, kế thừa từ LessonSerializer, thêm thông tin về tags
class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many=True)  # Thêm thông tin các tags liên quan đến bài học
    liked = SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return lesson.like_set.filter(user=request.user, active=True).exists()

    class Meta:
        model = LessonSerializer.Meta.model  # Sử dụng model của LessonSerializer
        fields = LessonSerializer.Meta.fields + ['content', 'tags', 'liked']  # Thêm trường 'content' và 'tags'


# Serializer cho User, dùng để chuyển đổi dữ liệu từ và đến đối tượng User
class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Gọi hàm to_representation của lớp cha (ModelSerializer)
        data = super().to_representation(instance)
        # Thêm URL của avatar (nếu có)
        data['avatar'] = instance.avatar.url if instance.avatar else ''
        return data

    def create(self, validated_data):
        # Hàm tạo User mới từ validated_data, mã hóa password
        data = validated_data.copy()
        u = User(**data)  # Tạo đối tượng User
        u.set_password(u.password)  # Mã hóa password trước khi lưu
        u.save()  # Lưu vào cơ sở dữ liệu

    class Meta:
        model = User  # Sử dụng model User
        fields = ['first_name', 'last_name', 'username', 'password', 'avatar']  # Các trường cần serialize
        extra_kwargs = {
            'write_only': True  # Đặt password là 'write_only' để không trả về trong API responses
        }


# Serializer cho Comment, hiển thị nội dung bình luận cùng với thông tin user
class CommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance): # Thêm thông tin của user bình luận không ảnh hưởng deseri
        # Gọi hàm to_representation của lớp cha (ModelSerializer)
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data

    class Meta:
        model = Comment  # Sử dụng model Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user', 'lesson']  # Các trường cần serialize
        extra_kwargs = {
            'lesson': {
                'write_only': True
            }
        }