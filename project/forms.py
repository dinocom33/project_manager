from django import forms
from django.forms import ModelForm
from .models import Project, ProjectFile, ProjectCollaborator


class ProjectFileForm(ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['name', 'attachment']


class InviteCollaboratorForm(ModelForm):
    email = forms.EmailField()
    # role = forms.CharField(max_length=255, required=False)

    class Meta:
        model = ProjectCollaborator
        fields = ['email', 'role']
