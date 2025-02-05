from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index),
    re_path(r'^.*chat/$', TemplateView.as_view(template_name='frontend/index.html'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
