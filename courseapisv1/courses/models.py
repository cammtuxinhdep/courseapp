from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Mô hình người dùng kế thừa từ AbstractUser
class User(AbstractUser):
    avatar = CloudinaryField(null=True)  # Ảnh đại diện lưu trên Cloudinary

# Mô hình cơ sở, chứa các trường chung cho các mô hình khác
class BaseModel(models.Model):
    active = models.BooleanField(default=True)  # Xác định trạng thái kích hoạt
    created_date = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    updated_date = models.DateTimeField(auto_now=True)  # Ngày cập nhật

    class Meta:
        abstract = True  # Mô hình này sẽ không được tạo thành bảng riêng trong DB

# Mô hình danh mục khóa học
class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)  # Tên danh mục duy nhất

    def __str__(self):
        return self.name

# Mô hình khóa học
class Courses(BaseModel):
    subject = models.CharField(max_length=255)  # Tiêu đề khóa học
    description = models.TextField(null=True)  # Mô tả khóa học
    image = CloudinaryField()  # Hình ảnh khóa học
    category = models.ForeignKey(Category, on_delete=models.PROTECT)  # Khóa ngoại liên kết với Category

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-id']  # Sắp xếp khóa học theo ID giảm dần

# Mô hình bài học
class Lesson(BaseModel):
    subject = models.CharField(max_length=255)  # Tiêu đề bài học
    content = RichTextField()  # Nội dung bài học với CKEditor hỗ trợ soạn thảo văn bản
    image = CloudinaryField()  # Hình ảnh minh họa bài học
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)  # Bài học thuộc khóa học nào
    tags = models.ManyToManyField('Tag')  # Gắn thẻ cho bài học

    def __str__(self):
        return self.subject

# Mô hình thẻ (Tag) để gắn vào bài học
class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)  # Tên thẻ duy nhất

    def __str__(self):
        return self.name

# Mô hình tương tác (abstract) giữa người dùng và bài học
class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người dùng thực hiện tương tác
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Bài học được tương tác

    class Meta:
        abstract = True  # Không tạo bảng riêng trong DB

# Mô hình bình luận
class Comment(Interaction):
    content = models.CharField(max_length=255)  # Nội dung bình luận

    def __str__(self):
        return self.content

# Mô hình thích bài học (Like)
class Like(Interaction):
    class Meta:
        unique_together = ('lesson', 'user')  # Một người dùng chỉ có thể thích một bài học một lần