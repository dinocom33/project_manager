import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from project.models import Project
from .models import ToDoList


@login_required()
def todolist(request, project_id, pk):
    project = Project.objects.filter(pk=project_id).first()
    todolist = ToDoList.objects.filter(project=project).get(pk=pk)

    if request.user == project.owner or request.user in project.collaborators.all():
        return render(request, 'todolist/todolist.html', {'project': project, 'todolist': todolist})


@login_required
def add(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':

        if request.user != project.owner and request.user not in project.collaborators.all():
            messages.error(request, "You do not have permission to add a new To-Do List.")
            return redirect('project:project_detail', pk=project_id)

        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            ToDoList.objects.create(name=name, description=description, created_by=request.user,
                                    project_id=project_id)
            return redirect('project:project_detail', pk=project_id)

    return redirect('project:project_detail', pk=project_id)


@login_required()
def edit(request, project_id, pk):
    project = Project.objects.get(pk=project_id)
    todolist = ToDoList.objects.filter(project=project).get(pk=pk)

    if request.method == 'POST':
        if request.user != project.owner and request.user not in project.collaborators.all():
            messages.error(request, "You do not have permission to edit this To-Do List.")

            return redirect('project:project_detail', pk=project_id)

        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            todolist.name = name
            todolist.description = description
            todolist.save()
            return redirect('todolist:todolist', project_id=project_id, pk=pk)

    return render(request, 'todolist/edit.html', {'project': project, 'todolist': todolist})


@login_required()
def delete(request, project_id, pk):
    project = Project.objects.get(pk=project_id)
    todolist = ToDoList.objects.filter(project=project).get(pk=pk)

    if request.user != project.owner and request.user not in project.collaborators.all():
        messages.error(request, "You do not have permission to delete this To-Do List.")

        return redirect('project:project_detail', pk=project_id)

    if request.user == todolist.created_by or request.user == project.owner:
        todolist.delete()
        messages.success(request, 'ToDo list deleted successfully')

        return redirect('project:project_detail', pk=project_id)

    messages.error(request, "You do not have permission to delete this To-Do List.")

    return redirect('project:project_detail', pk=project_id)
