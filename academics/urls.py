from django.urls import path
from . import views

urlpatterns = [
    path('subjects/add/', views.add_subject_view, name='add_subject'),
    path('subjects/assign/', views.assign_classes_view, name='assign_classes'),
    path('marks/entry/', views.enter_marks_view, name='enter_marks'),
]
