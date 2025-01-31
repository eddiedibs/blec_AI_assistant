from django.urls import path
from .views import AiRequestView, DoctorModelViewSet, AiRequestAppointmentView, get_csrf_token



urlpatterns = [
    path('blec_ai', AiRequestView.as_view(), name="blec_ai_view"),
    path('doctors', DoctorModelViewSet.as_view({'get': 'list'}), name="doctors_view"),
    path('appointments', AiRequestAppointmentView.as_view(), name="appointment_view"),
    path('csrf', get_csrf_token, name='get_csrf_token'),

]
