from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import connection
from django.core.validators import RegexValidator
from accountManager.models import accountModel

# Create your models here.

RESO_STATUS_ = (
    ('Pending', 'Pending'),
    ('Solved', 'Solved'),
    ('Skip','Skip'),
    ('Closed','Closed')
)

PRIORITY_ = ( 
    ('Lowest','Lowest'),
    ('Low','Low'),
    ('Medium','Medium'),
    ('High','High'),
    ('Highest','Highest') 
)

STATUS_ = ( 
    ('New','New'),
    ('Reopen','Reopen'),
    ('Skip','Skip'),
    ('Solved','Solved'),
    ('Closed','Closed')
 )

class AddNewProject(models.Model):
    ProjectName = models.CharField(
        max_length=255, null=False, primary_key=True, verbose_name='Project_Name')

    def __str__(self):
        return self.ProjectName


class TaskAssignment(models.Model):
    ProjectName = models.ForeignKey(
        AddNewProject, on_delete=models.CASCADE)

    AssignedTo = models.ForeignKey(
        accountModel, on_delete=models.CASCADE,)


class BugSheetModel(models.Model):

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    sr_no = models.IntegerField             (null = True, blank = True)
    Defect_Id = models.CharField            (max_length=500,null = True, blank = True)
    Project_name = models.CharField         (max_length=500,null = True, blank = True)
    project_version = models.CharField      (max_length=500)
    Browser = models.CharField              (max_length=500, validators=[alphanumeric])
    Url_of_page = models.URLField           ()
    Status = models.CharField               (max_length=500,choices=STATUS_,null = True, blank = True)
    TimesReopened = models.IntegerField     (default=0,null = True, blank = True)
    Priority = models.CharField             (max_length=500,choices=PRIORITY_)
    Defect_desc = models.TextField          ()
    Steps_to_Reproduce = models.CharField   (max_length=500)
    Date_of_finding = models.DateTimeField  ()
    Tester_name = models.CharField          (max_length=500,null = True, blank = True)
    Developer_name = models.CharField       (max_length=500,null = True, blank = True)
    Resolution_Status = models.CharField    (max_length=500,choices=RESO_STATUS_,null = True, blank = True)
    Date_of_resolving = models.DateTimeField(null = True, blank = True)
    Developer_comments = models.TextField   (null = True, blank = True)
    Reopen_Reason = models.TextField        (null = True, blank = True)
    Attachment = models.ImageField          (upload_to='screenshots/%Y.%m.%d/', max_length=255,null = True, blank = True)

    #def save(self, *args, **kwargs):

        #theCursor = connection.cursor()
        #theCursor.execute('SELECT count(Project_name) FROM bugsdb.consoles_bugsheetmodel where Project_name = "'+ self.Project_name +'";')
        #for x in theCursor:
        #    self.sr_no = int(x[0])
        #    
        ##self.sr_no = BugSheetModel.objects.filter(Project_name=str(self.Project_name)).count()
        #
        #self.Defect_Id = str(self.Project_name) + '_' + str(self.sr_no)
        #super(BugSheetModel, self).save(*args, **kwargs)


    def __str__(self):
        return self.Defect_Id
class BugSheetModelextraimage(models.Model):
    Attachment = models.ImageField(upload_to='screenshots/%Y.%m.%d/', max_length=255,null = True, blank = True)
    Date_of_finding = models.DateTimeField  ()
    
class changelogs(models.Model):
    type_of_Change = models.CharField       (max_length=500)
    sr_no = models.IntegerField             (null = True, blank = True)
    Defect_Id = models.CharField            (max_length=500,null = True, blank = True)
    Project_name = models.CharField         (max_length=500,null = True, blank = True)
    project_version = models.CharField      (max_length=500)
    Browser = models.CharField              (max_length=500)
    Url_of_page = models.URLField           ()
    Status = models.CharField               (max_length=500,choices=STATUS_,null = True, blank = True)
    TimesReopened = models.IntegerField     (default=0,null = True, blank = True)
    Priority = models.CharField             (max_length=500,choices=PRIORITY_)
    Defect_desc = models.TextField          ()
    Steps_to_Reproduce = models.CharField   (max_length=500)
    Date_of_finding = models.DateTimeField  ()
    Tester_name = models.CharField          (max_length=500,null = True, blank = True)
    Developer_name = models.CharField       (max_length=500,null = True, blank = True)
    Resolution_Status = models.CharField    (max_length=500,choices=RESO_STATUS_,null = True, blank = True)
    Date_of_resolving = models.DateTimeField(null = True, blank = True)
    Developer_comments = models.TextField   (null = True, blank = True)
    Reopen_Reason = models.TextField        (null = True, blank = True)
    Attachment = models.ImageField          (upload_to='screenshots/%Y.%m.%d/', max_length=255,null = True, blank = True)
