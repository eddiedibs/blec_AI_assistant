from django.urls import path
from .views import *



urlpatterns = [
    path('blec_ai', AiRequestView.as_view(), name="blec_ai_view"),
]
