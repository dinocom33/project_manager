import uuid

from django.contrib.auth import get_user_model
from django.db import models
from project.models import Project
from todolist.models import ToDoList

User = get_user_model()


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=(
            ('open', 'Open'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
        )
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
