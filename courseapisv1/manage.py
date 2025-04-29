#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os  # Thư viện os giúp thao tác với hệ điều hành
import sys  # Thư viện sys giúp thao tác với hệ thống (chạy script, nhận tham số từ dòng lệnh)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseapisv1.settings')  # Cấu hình biến môi trường cho Django settings
    try:
        from django.core.management import execute_from_command_line  # Import công cụ quản lý của Django
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)  # Chạy các lệnh quản lý Django từ dòng lệnh

if __name__ == '__main__':
    main()  # Gọi hàm main nếu script này được chạy
