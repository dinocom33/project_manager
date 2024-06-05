from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('add/', views.add_project, name='add'),
    path('<uuid:pk>/', views.project_detail, name='project_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<uuid:pk>/edit/', views.edit_project, name='edit_project'),
    path('<uuid:pk>/delete/', views.delete_project, name='delete_project'),
    path('<uuid:pk>/upload_file/', views.upload_file, name='upload_file'),
]
