from django.contrib import admin

from project.models import Project, ProjectCollaborator, ProjectFile, Notes


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(ProjectCollaborator)
class ProjectCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'added_at')
    list_filter = ('user', 'project', 'added_at')
    search_fields = ('user', 'project')


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'uploaded_at')
    list_filter = ('name', 'project', 'uploaded_at')
    search_fields = ('name', 'project')

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_at', 'updated_at')
    list_filter = ('title', 'project', 'created_at')
    search_fields = ('title', 'project')


admin.site.site_header = 'Project Manager Admin'
admin.site.site_title = 'Administration'
admin.site.index_title = 'Project Manager'
