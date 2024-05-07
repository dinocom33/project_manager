from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Project


@login_required
def projects(request):
    all_projects = Project.objects.all().filter(created_by=request.user).order_by('-created_at')

    return render(request, 'project/projects.html', {'projects': all_projects})


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
