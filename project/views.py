from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from todolist.models import ToDoList
from .forms import ProjectFileForm
from .models import Project, ProjectFile


@login_required
def projects(request):
    all_projects = Project.objects.all().filter(created_by=request.user).order_by('-created_at')

    return render(request, 'project/projects.html', {'projects': all_projects})


@login_required()
def project_detail(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'project/project_detail.html', {'project': project})


@login_required()
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            project = Project.objects.create(name=name, description=description, created_by=request.user)
            project.save()

            messages.success(request, 'Project created successfully')

            return redirect('project:projects')
        else:
            messages.error(request, 'Project name is required')

    return render(request, 'project/create_project.html')


@login_required()
def edit_project(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            project.name = name
            project.description = description
            project.save()

            messages.success(request, 'Project updated successfully')

            return redirect('project:project_detail', pk=project.id)

    return redirect('project:project_detail', pk=project.id)


@login_required()
def delete_project(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    project.delete()

    messages.success(request, 'Project deleted successfully')

    return redirect('project:projects')


@login_required
def dashboard(request):
    todolists = ToDoList.objects.all()

    if request.method == 'POST':
        # Handle form submission (if any)
        if 'name' in request.POST:
            # Create a new task
            task_name = request.POST.get('name')
            task_description = request.POST.get('description', '')  # Assuming description is optional
            task_status = request.POST.get('status', 'todo')  # Default status to 'todo' if not provided
            ToDoList.objects.create(name=task_name, description=task_description, status=task_status)
            return redirect('project:dashboard')

    # Pass tasks to the template
    context = {'todolists': todolists}

    return render(request, 'project/dashboard.html', context)


@login_required
def upload_file(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.project = project
            file.uploaded_by = request.user
            file.save()

            return redirect('project:project_detail', pk=project.id)
    else:
        form = ProjectFileForm()

    return render(request, 'project/upload_file.html', {'project': project, 'form': form})


@login_required
def delete_file(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    projectfile = project.files.get(pk=pk)

    projectfile.delete()

    return redirect('project:project_detail', pk=project.id)