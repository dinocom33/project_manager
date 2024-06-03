from django.urls import path

from . import views

app_name = 'task'

urlpatterns = [
    path('add/', views.add_task, name='add'),
]