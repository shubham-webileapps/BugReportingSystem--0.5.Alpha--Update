from django.contrib import admin
from .models import AddNewProject
from .models import TaskAssignment
from .models import BugSheetModel
from .models import changelogs
from .models import BugSheetModelextraimage
'''
'''
# Register your models here.


class BugSheetModelAdmin(admin.ModelAdmin):
    list_display = ('sr_no',
                    'Defect_Id',
                    'Resolution_Status',
                    'Project_name',
                    'project_version',
                    'Browser',
                    'Status',
                    'TimesReopened',
                    'Priority',
                    'Defect_desc',
                    'Steps_to_Reproduce',
                    'Attachment',
                    'Date_of_finding',
                    'Tester_name',
                    'Developer_name',
                    'Date_of_resolving',
                    'Developer_comments',
                    'Reopen_Reason',
                    'Url_of_page',)

class changelogsAdmin(admin.ModelAdmin):
    list_display = ('sr_no',
                    'type_of_Change',
                    'Defect_Id',
                    'Resolution_Status',
                    'Project_name',
                    'project_version',
                    'Browser',
                    'Status',
                    'TimesReopened',
                    'Priority',
                    'Defect_desc',
                    'Steps_to_Reproduce',
                    'Attachment',
                    'Date_of_finding',
                    'Tester_name',
                    'Developer_name',
                    'Date_of_resolving',
                    'Developer_comments',
                    'Reopen_Reason',
                    'Url_of_page',)


class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('AssignedTo', 'ProjectName')


admin.site.register(AddNewProject)
# admin.site.register(BugSheetModelextraimage)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(BugSheetModel, BugSheetModelAdmin)
admin.site.register(changelogs, changelogsAdmin)
'''
'''
