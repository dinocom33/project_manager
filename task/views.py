from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from project.models import Project
from task.models import Task
from todolist.models import ToDoList


@login_required()
def add_task(request, project_id, todolist_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = ToDoList.objects.filter(created_by=request.user, project=project).get(pk=todolist_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        created_by = request.user

        Task.objects.create(
            project=project, todolist=todolist, name=name, description=description,
            status=status, created_by=created_by
        )

        return redirect('todolist:todolist', project.id, todolist.id)

    return render(request, 'task/add_task.html', {'project': project, 'todolist': todolist})
