"""
ASGI config for courseapisv1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
"""
ASGI config for courseapisv1 project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application

# Đặt biến môi trường để xác định file settings của Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseapisv1.settings')

# Tạo ứng dụng ASGI
application = get_asgi_application()
