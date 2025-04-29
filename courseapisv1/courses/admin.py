from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.html import mark_safe

from courses.models import Category, Courses, Lesson, Tag, Comment

# Form tùy chỉnh cho Lesson, sử dụng CKEditor để nhập nội dung
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'

# Quản lý hiển thị và chỉnh sửa model Courses trong trang Admin
class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date', 'category']  # Các cột hiển thị
    search_fields = ['subject']  # Cho phép tìm kiếm theo subject
    list_filter = ['id', 'created_date']  # Bộ lọc
    list_editable = ['subject']  # Cho phép chỉnh sửa trực tiếp subject
    readonly_fields = ['image_view']  # Chỉ đọc với image_view

    def image_view(self, course):
        """Hiển thị ảnh trong trang Admin"""
        return mark_safe(f"<img src='/static/{course.image.name}' width='120' />")

# Quản lý Lesson trong trang Admin
class MyLessonAdmin(admin.ModelAdmin):
    form = LessonForm

# Đăng ký các model vào trang Admin
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Courses, MyCourseAdmin)
admin.site.register(Lesson, MyLessonAdmin)