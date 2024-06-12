from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from account.models import User
from .forms import ProjectFileForm, InviteCollaboratorForm
from .models import Project, ProjectFile, Notes, ProjectCollaborator


@login_required
def projects(request):
    user = request.user
    owned_projects = Project.objects.filter(owner=user)
    collaborated_projects = Project.objects.filter(collaborators=user)
    all_projects = (owned_projects | collaborated_projects).distinct().order_by('-created_at')

    return render(request, 'project/projects.html', {'projects': all_projects})


@login_required()
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            project = Project.objects.create(name=name, description=description, owner=request.user)
            project.save()

            messages.success(request, 'Project created successfully')

            return redirect('project:projects')
        else:
            messages.error(request, 'Project name is required')

    return render(request, 'project/create_project.html')


@login_required()
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    collaborators = ProjectCollaborator.objects.filter(project=project)
    project_files = ProjectFile.objects.filter(project=project).order_by('-uploaded_at')

    if request.user == project.owner or request.user in project.collaborators.all():
        return render(request, 'project/project_detail.html',
                      {'project': project, 'collaborators': collaborators, 'project_files': project_files})
    else:
        messages.error(request, "You do not have permission to access this project.")
        return redirect('projects')


@login_required()
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            if request.user == project.owner:
                project.name = name
                project.description = description
                project.save()

                messages.success(request, 'Project updated successfully')

                return redirect('project:project_detail', pk=project.id)
            else:
                messages.error(request, 'You are not authorized to edit this project')
        else:
            messages.error(request, 'Project name is required')

    return redirect('project:project_detail', pk=project.id)


@login_required()
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner:
        messages.error(request, 'You are not authorized to delete this project')

        return redirect('project:projects')

    project.delete()
    messages.success(request, 'Project deleted successfully')

    return redirect('project:projects')


@login_required
def upload_file(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    form = ProjectFileForm(request.POST, request.FILES)

    if request.method == 'POST':
        if request.user == project.owner or request.user in project.collaborators.all():

            if form.is_valid():
                file = form.save(commit=False)
                file.project = project
                file.uploaded_by = request.user

                file.save()

                messages.success(request, 'File uploaded successfully')
        else:
            messages.error(request, 'You are not authorized to upload files to this project')

    return redirect('project:project_detail', pk=project.id)


@login_required
def delete_file(request, project_id, file_id):
    project = get_object_or_404(Project, pk=project_id)

    file = get_object_or_404(ProjectFile, pk=file_id)

    if request.user != file.uploaded_by and request.user != project.owner:
        messages.error(request, 'You are not authorized to delete this file')

        return redirect('project:project_detail', pk=project.id)

    file.attachment.delete()
    file.delete()

    messages.success(request, 'File deleted successfully')

    return redirect('project:project_detail', pk=project.id)


@login_required()
def add_note(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')

        if request.user != project.owner and request.user not in project.collaborators.all():
            messages.error(request, "You do not have permission to add notes to this project.")
            return redirect('project:project_detail', pk=project.id)

        if title:
            note = Notes.objects.create(title=title, body=body, project=project, created_by=request.user)
            note.save()

            messages.success(request, 'Note added successfully')

            return redirect('project:project_detail', pk=project.id)

    return redirect('project:project_detail', pk=project.id)


@login_required
def invite_collaborator(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user != project.owner:
        messages.error(request, "You do not have permission to invite collaborators to this project.")
        return redirect('project:project_detail', project_id=project.id)

    if request.method == 'POST':
        form = InviteCollaboratorForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role'] or 'Collaborator'
            try:
                user = User.objects.get(email=email)
                if ProjectCollaborator.objects.filter(user=user, project=project).exists():
                    messages.warning(request, "This user is already a collaborator on this project.")
                else:
                    ProjectCollaborator.objects.create(user=user, project=project, role=role)
                    messages.success(request, f"{user.email} has been successfully invited as a collaborator.")
                    return redirect('project:project_detail', pk=project.id)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('project:project_detail', pk=project.id)
    else:
        form = InviteCollaboratorForm()

    return redirect('project:project_detail', pk=project_id, form=form)
