from django.urls import path
from .views import AiRequestView, DoctorModelViewSet, AiRequestAppointmentView



urlpatterns = [
    path('blec_ai', AiRequestView.as_view(), name="blec_ai_view"),
    path('doctors', DoctorModelViewSet.as_view({'get': 'list'}), name="doctors_view"),
    path('appointments', AiRequestAppointmentView.as_view(), name="appointment_view"),
]
