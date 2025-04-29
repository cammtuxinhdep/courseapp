"""
WSGI config for courseapisv1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
"""
  WSGI config for courseapisv1 project.
  It exposes the WSGI callable as a module-level variable named ``application``.
  """

import os

from django.core.wsgi import get_wsgi_application

# Đặt biến môi trường để xác định file settings của Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseapisv1.settings')

# Tạo ứng dụng WSGI
application = get_wsgi_application()
