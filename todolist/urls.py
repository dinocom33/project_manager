from django.urls import path

from . import views

app_name = 'todolist'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('<uuid:pk>/', views.todolist, name='todolist'),
    path('<uuid:pk>/edit/', views.edit, name='edit'),
    path('<uuid:pk>/delete/', views.delete, name='delete'),
    path('projects/<uuid:project_id>/add/', views.save_task_view, name='save_task'),
]
