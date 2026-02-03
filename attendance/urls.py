from django.urls import path
from . import views

urlpatterns = [
    path('take/', views.take_attendance_view, name='take_attendance'),
]
