import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from project.models import Project
from .models import ToDoList


@login_required()
def todolist(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = ToDoList.objects.filter(created_by=request.user, project=project).get(pk=pk)

    return render(request, 'todolist/todolist.html', {'project': project, 'todolist': todolist})


@login_required
def add(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            ToDoList.objects.create(name=name, description=description, created_by=request.user,
                                    project_id=project_id)
            return redirect('project:project_detail', pk=project_id)

    return render(request, 'todolist/add.html', {'project': project})


def save_task_view(request):
    project = Project.objects.filter(created_by=request.user).get(pk=request.POST.get('project_id'))
    if request.method == 'POST':
        # Extract data from POST request
        data = json.loads(request.body)
        task_name = data.get('name')
        task_description = data.get('description', '')  # Assuming description is optional

        # Create the task
        task = ToDoList.objects.create(name=task_name, description=task_description, project_id=project.id)

        # Return success response
        return JsonResponse({'message': 'Task saved successfully!', 'task_id': task.id})

    # Return error response if request method is not POST
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required()
def edit(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = ToDoList.objects.filter(created_by=request.user, project=project).get(pk=pk)

    if request.method == 'POST':
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
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = ToDoList.objects.filter(created_by=request.user, project=project).get(pk=pk)

    todolist.delete()
    return redirect('project:project_detail', pk=project_id)
