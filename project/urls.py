from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('add/', views.add_project, name='add'),
    path('<uuid:pk>/', views.project_detail, name='project_detail'),
    path('<uuid:pk>/edit/', views.edit_project, name='edit_project'),
    path('<uuid:pk>/delete_project/', views.delete_project, name='delete_project'),
    path('<uuid:project_id>/upload_file/', views.upload_file, name='upload_file'),
    path('<uuid:project_id>/<uuid:file_id>/delete_file/', views.delete_file, name='delete_file'),
    path('<uuid:project_id>/add_note/', views.add_note, name='add_note'),
    path('project/<uuid:project_id>/invite/', views.invite_collaborator, name='invite_collaborator'),
]
