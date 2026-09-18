from django.urls import path
from . import views

urlpatterns = [
    path('tasks/',views.TaskApiListCreateView.as_view(),name='list-create'),
    path('tasks/<int:pk>/',views.TaskApiDetailView.as_view(),name='task-detail')
]