from django.urls import path
from .views import AiRequestView, DoctorModelViewSet#, ChatFormModelViewSet



urlpatterns = [
    path('blec_ai', AiRequestView.as_view(), name="blec_ai_view"),
    path('doctors', DoctorModelViewSet.as_view({'get': 'list'}), name="doctors_view"),
    # path('doctors', DoctorModelViewSet.as_view({'get': 'list'}), name="doctors_view"),
]
