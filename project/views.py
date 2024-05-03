from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Project


@login_required
def projects(request):
    all_projects = Project.objects.all()

    return render(request, 'project/projects.html', {'projects': all_projects})


@login_required()
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            project = Project.objects.create(name=name, description=description, created_by=request.user)
            project.save()

            return redirect('project:projects')

    return render(request, 'project/create_project.html')
