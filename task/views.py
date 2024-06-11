from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from project.models import Project
from task.models import Task
from todolist.models import ToDoList


@login_required()
def add_task(request, project_id, todolist_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = ToDoList.objects.filter(project=project).get(pk=todolist_id)

    if request.method == 'POST':
        if request.user != project.owner and request.user not in project.collaborators.all():
            messages.error(request, "You do not have permission to access this project.")
            return redirect('project:project_detail', pk=project.id)

        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        created_by = request.user

        Task.objects.create(
            project=project, todolist=todolist, name=name, description=description,
            status=status, created_by=created_by
        )

        messages.success(request, 'Task added successfully')

        return redirect('todolist:todolist', project.id, todolist.id)

    return render(request, 'task/add_task.html', {'project': project, 'todolist': todolist})


@login_required()
def detail(request, project_id, todolist_id, pk):
    project = Project.objects.get(pk=project_id)
    todolist = ToDoList.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project, todolist=todolist).get(pk=pk)

    if request.user != project.owner and request.user not in project.collaborators.all():
        messages.error(request, "You do not have permission to access this project.")
        return redirect('project:project_detail', pk=project.id)

    return render(request, 'task/detail.html', {'project': project, 'todolist': todolist, 'task': task})


@login_required()
def edit(request, project_id, todolist_id, pk):
    project = Project.objects.get(pk=project_id)
    todolist = ToDoList.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project, todolist=todolist).get(pk=pk)

    if request.method == 'POST':
        if request.user != project.owner and request.user not in project.collaborators.all():
            messages.error(request, "You do not have permission to edit this task.")
            return redirect('project:project_detail', pk=project.id)

        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')

        if name:
            task.name = name

        task.description = description
        task.status = status
        task.save()

    return redirect('task:detail', project.id, todolist.id, task.id)


@login_required()
def delete(request, project_id, todolist_id, pk):
    project = Project.objects.get(pk=project_id)
    todolist = ToDoList.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project, todolist=todolist).get(pk=pk)

    if request.user != task.created_by:
        messages.error(request, "You do not have permission to delete this task.")
        return redirect('todolist:todolist', project.id, todolist.id)

    task.delete()
    messages.success(request, 'Task deleted successfully')

    return redirect('todolist:todolist', project.id, todolist.id)
