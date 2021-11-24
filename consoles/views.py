from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db import connection
from consoles.models import TaskAssignment, AddNewProject
from consoles.models import BugSheetModel, changelogs
from consoles.forms import editBugForm, reopenBugForm, screenShotForm, solveBugForm, testerBugForm
from django.conf import settings
from django.templatetags.static import static
from django.utils import timezone
import xlwt


from .models import User
from notifications.signals import notify
# common
def showConsoles(request):
    if 'username' in request.session:
        theCursor = connection.cursor()
        theCursor.execute("SELECT DISTINCT ProjectName_id FROM consoles_taskassignment where assignedto_id='"+ str(request.session['username']) +"'")
        allProjectAssignedToUser = theCursor 
        lot= list(theCursor)
        lol = [list(x) for x in lot]
        totalproj = 0  
        for project in allProjectAssignedToUser:                
            total = BugSheetModel.objects.filter(Project_name=project[0]).count()
            solved = BugSheetModel.objects.filter(Project_name=project[0]).filter(Resolution_Status='Solved').count()
            pending = BugSheetModel.objects.filter(Project_name=project[0]).filter(Resolution_Status='Pending').count()

            lol[totalproj].append(solved)
            lol[totalproj].append(pending)
            lol[totalproj].append(total)

            totalproj += 1
        request.session['template'] = 't_tester'
        return render(request, 'consoles/t_showConsole.html', {'projects': lol})
    else:
        request.session['template'] = 'index'
        return render(request, 'accountManager/index.html')



def sheetDetail(request, pk, fv):
    fullview = int(fv)
    request.session['projectname'] = pk
    if 'usertype' in request.session:    
        sheetListQuery = BugSheetModel.objects.filter(Project_name=pk).order_by('-sr_no')
        request.session['template'] = 't_partialsheet'
        if fullview == 0 :
            return render(request, 'consoles/t_partialsheet.html', {'sheetRows': sheetListQuery,'proj_name': pk})
        elif fullview == 1 :
            return render(request, 'consoles/t_fullsheet.html', {'sheetRows': sheetListQuery,'proj_name': pk})

    else: 
        request.session['template'] = 't_login'
        return render(request, 'accountManager/t_login.html', {})


def sheetDetailOrderBY(request, pk, ob):
    if 'usertype' in request.session:
        sheetListQuery = BugSheetModel.objects.filter(Project_name=pk).order_by('-'+ob)
        request.session['template'] = 't_partialsheet'
        return render(request, 'consoles/t_partialsheet.html', {'sheetRows': sheetListQuery,'proj_name': pk})
    else: 
        request.session['template'] = 't_login'
        return render(request, 'accountManager/t_login.html', {})



def rowDetail(request, projname,bugModelPK):
    if 'usertype' in request.session:    
        rowQuery = BugSheetModel.objects.filter(id=bugModelPK)
        request.session['template'] = 't_rowDetails'
        return render(request, 'consoles/t_rowDetails.html', {'sheetRow': rowQuery,'proj_name': projname})
    else: 
        request.session['template'] = 't_login'
        return render(request, 'accountManager/t_login.html', {})



# Admin
def adminConsole(request):
    if request.session['usertype'] == 'admin':
        if 'usertype' in request.session:
            if request.session['usertype'] == 'admin':
                allProjects = AddNewProject.objects.only('ProjectName')
                request.session['template'] = 't_tester'
                return render(request, 'consoles/t_adminShowConsole.html', {'projects': allProjects})
        else:
            request.session['template'] = 'index'
            return render(request, 'accountManager/index.html')
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})


def showAllActivity(request):
    if request.session['usertype'] == 'admin':

        if 'usertype' in request.session:    
            sheetListQuery = changelogs.objects.all().order_by('-id')
            request.session['template'] = 't_logsheet'
            return render(request, 'consoles/t_logsheet.html', {'sheetRows': sheetListQuery})
        else: 
            request.session['template'] = 't_login'
            return render(request, 'accountManager/t_login.html', {})
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})

def logsDetail(request, did):
    if request.session['usertype'] == 'admin':
        if 'usertype' in request.session:    
            logListQuery = changelogs.objects.filter(Defect_Id=did)
            request.session['template'] = 't_logsheet'
            return render(request, 'consoles/t_logsheet.html', {'sheetRows': logListQuery, 'did' : did})
        else: 
            request.session['template'] = 't_login'
            return render(request, 'accountManager/t_login.html', {})
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})



def logrowDetail(request, projname,bugModelPK):
    if 'usertype' in request.session:    
        rowQuery = changelogs.objects.filter(id=bugModelPK)
        request.session['template'] = 't_rowDetails'
        return render(request, 'consoles/t_rowDetails.html', {'sheetRow': rowQuery,'proj_name': projname})
    else: 
        request.session['template'] = 't_login'
        return render(request, 'accountManager/t_login.html', {})


# Tester
def newBugYey(request):
    if request.session['usertype'] == 'tester':
        formObj = testerBugForm()
        formObj1=screenShotForm()
        bugsaved = False
        if request.method == "POST" and bugsaved == False:
            formObj = testerBugForm(request.POST, request.FILES)
            formObj1=screenShotForm(request.POST, request.FILES)

            if formObj.is_valid() and formObj1.is_valid():
                newFormData = formObj.save(commit=False)
                # newFormData1 = formObj1.save(commit=False)

                #theCursor = connection.cursor()
                #theCursor.execute('SELECT count(Project_name) FROM bugsdb.consoles_bugsheetmodel where Project_name = "'+ request.session['projectname'] +'";')
                #for x in theCursor:
                #    newFormData.sr_no = int(x[0])
                #    newFormData.Defect_Id = str(request.session['projectname']) + '_' + str(int(x[0]))
                projectBugCount = BugSheetModel.objects.filter(Project_name=request.session['projectname']).count()
                newFormData.sr_no = int(projectBugCount) + 1
                newFormData.Defect_Id = str(request.session['projectname']) + '_' + str(int(projectBugCount) + 1)
                newFormData.Date_of_finding = timezone.localtime(timezone.now())
                newFormData.Project_name = request.session['projectname']
                newFormData.Status = 'New'
                newFormData.TimesReopened = 0
                newFormData.Tester_name = request.session['username']
                newFormData.Resolution_Status = 'Pending'
                newFormData.save()
                # newFormData1.save()

                changelogsentry = changelogs(
                    type_of_Change = 'Added Bug',
                    sr_no = newFormData.sr_no,
                    Defect_Id = newFormData.Defect_Id,
                    Project_name = newFormData.Project_name,
                    project_version = newFormData.project_version,
                    Browser = newFormData.Browser,
                    Url_of_page = newFormData.Url_of_page,
                    Status = newFormData.Status,
                    TimesReopened = newFormData.TimesReopened,
                    Priority = newFormData.Priority,
                    Defect_desc = newFormData.Defect_desc,
                    Steps_to_Reproduce = newFormData.Steps_to_Reproduce,
                    Date_of_finding = newFormData.Date_of_finding,
                    Tester_name = newFormData.Tester_name,
                    Developer_name = "None",
                    Resolution_Status = newFormData.Resolution_Status,
                    Date_of_resolving = None,
                    Developer_comments = None,
                    Reopen_Reason = None,
                    Attachment = newFormData.Attachment,
                    
                    )
                changelogsentry.save()

                bugsaved = True
            else :
                # print(formObj.errors)
                pass
        if bugsaved == False :
            request.session['template'] = 't_addNewBug'
            return render(request, 'consoles/t_addNewBug.html', {'theform':formObj})
        else:
            return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})

# Tester
def editNewBug(request, bugpk, un):
    if request.session['usertype'] == 'tester':
    
        edited = False
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        if request.method == "POST":
            formObj = testerBugForm(request.POST, instance=bugDataToEdit)
            if formObj.is_valid():
                bugDataToEdit.save()

                changelogsentry = changelogs(
                    type_of_Change = 'Bug Edited',
                    sr_no = bugDataToEdit.sr_no,
                    Defect_Id = bugDataToEdit.Defect_Id,
                    Project_name = bugDataToEdit.Project_name,
                    project_version = bugDataToEdit.project_version,
                    Browser = bugDataToEdit.Browser,
                    Url_of_page = bugDataToEdit.Url_of_page,
                    Status = bugDataToEdit.Status,
                    TimesReopened = bugDataToEdit.TimesReopened,
                    Priority = bugDataToEdit.Priority,
                    Defect_desc = bugDataToEdit.Defect_desc,
                    Steps_to_Reproduce = bugDataToEdit.Steps_to_Reproduce,
                    Date_of_finding = bugDataToEdit.Date_of_finding,
                    Tester_name = bugDataToEdit.Tester_name,
                    Developer_name = bugDataToEdit.Developer_name,
                    Resolution_Status = bugDataToEdit.Resolution_Status,
                    Date_of_resolving = bugDataToEdit.Date_of_resolving,
                    Developer_comments = bugDataToEdit.Developer_comments,
                    Reopen_Reason = bugDataToEdit.Reopen_Reason,
                    Attachment = bugDataToEdit.Attachment,
                    )
                changelogsentry.save()

                edited = True
        else:
            formObj = testerBugForm(instance=bugDataToEdit)
        if edited == False :
            request.session['template'] = 't_editNewBug'
            return render(request, 'consoles/t_editNewBug.html', {'theform':formObj,'un':un})
        else:
            return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})

# Tester
def reopenNewBug(request, bugpk, un):
    if request.session['usertype'] == 'tester':
        edited = False
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        if request.method == "POST":
            formObj = reopenBugForm(request.POST, instance=bugDataToEdit)
            if formObj.is_valid():
                bugDataToEdit = formObj.save(commit=False)
                bugDataToEdit.Status = 'Reopen'
                bugDataToEdit.TimesReopened = int(bugDataToEdit.TimesReopened) + 1 
                bugDataToEdit.Resolution_Status = 'Pending'
                bugDataToEdit.save()

                changelogsentry = changelogs(
                    type_of_Change = 'Bug Reopened',
                    sr_no = bugDataToEdit.sr_no,
                    Defect_Id = bugDataToEdit.Defect_Id,
                    Project_name = bugDataToEdit.Project_name,
                    project_version = bugDataToEdit.project_version,
                    Browser = bugDataToEdit.Browser,
                    Url_of_page = bugDataToEdit.Url_of_page,
                    Status = bugDataToEdit.Status,
                    TimesReopened = bugDataToEdit.TimesReopened,
                    Priority = bugDataToEdit.Priority,
                    Defect_desc = bugDataToEdit.Defect_desc,
                    Steps_to_Reproduce = bugDataToEdit.Steps_to_Reproduce,
                    Date_of_finding = bugDataToEdit.Date_of_finding,
                    Tester_name = bugDataToEdit.Tester_name,
                    Developer_name = bugDataToEdit.Developer_name,
                    Resolution_Status = bugDataToEdit.Resolution_Status,
                    Date_of_resolving = bugDataToEdit.Date_of_resolving,
                    Developer_comments = bugDataToEdit.Developer_comments,
                    Reopen_Reason = bugDataToEdit.Reopen_Reason,
                    Attachment = bugDataToEdit.Attachment,
                    )
                changelogsentry.save()

                edited = True
        else:
            formObj = reopenBugForm(instance=bugDataToEdit)
        if edited == False :
            request.session['template'] = 't_reopenBug'
            return render(request, 'consoles/t_reopenBug.html', {'theform':formObj,'un':un})
        else:
            return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})


def SkipBug(request, bugpk, un):
    if request.session['usertype'] == 'tester':
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        bugDataToEdit.Status = 'Skip'
        bugDataToEdit.Resolution_Status = 'Skip'
        bugDataToEdit.save()
        return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})



def CloseBug(request, bugpk, un):
    if request.session['usertype'] == 'tester':
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        bugDataToEdit.Status = 'Closed'
        bugDataToEdit.Resolution_Status = 'Closed'
        bugDataToEdit.save()
        return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")

    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})

def dropdowntester(request, bugpk, un):
    if request.session['usertype'] == 'tester':
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        if request.GET.get('Status')=='Closed':
            bugDataToEdit.Status = 'Closed'
            bugDataToEdit.Resolution_Status = 'Closed'
            bugDataToEdit.save()
        elif request.GET.get('Status')=='Skip':
            bugDataToEdit.Status = 'Skip'
            bugDataToEdit.Resolution_Status = 'Skip'
            bugDataToEdit.save()
        elif request.GET.get('Status')=='Reopen':
            edited = False
            bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
            if request.method == "POST":
                formObj = reopenBugForm(request.POST, instance=bugDataToEdit)
                if formObj.is_valid():
                    bugDataToEdit = formObj.save(commit=False)
                    bugDataToEdit.Status = 'Reopen'
                    bugDataToEdit.TimesReopened = int(bugDataToEdit.TimesReopened) + 1 
                    bugDataToEdit.Resolution_Status = 'Pending'
                    bugDataToEdit.save()

                    changelogsentry = changelogs(
                        type_of_Change = 'Bug Reopened',
                        sr_no = bugDataToEdit.sr_no,
                        Defect_Id = bugDataToEdit.Defect_Id,
                        Project_name = bugDataToEdit.Project_name,
                        project_version = bugDataToEdit.project_version,
                        Browser = bugDataToEdit.Browser,
                        Url_of_page = bugDataToEdit.Url_of_page,
                        Status = bugDataToEdit.Status,
                        TimesReopened = bugDataToEdit.TimesReopened,
                        Priority = bugDataToEdit.Priority,
                        Defect_desc = bugDataToEdit.Defect_desc,
                        Steps_to_Reproduce = bugDataToEdit.Steps_to_Reproduce,
                        Date_of_finding = bugDataToEdit.Date_of_finding,
                        Tester_name = bugDataToEdit.Tester_name,
                        Developer_name = bugDataToEdit.Developer_name,
                        Resolution_Status = bugDataToEdit.Resolution_Status,
                        Date_of_resolving = bugDataToEdit.Date_of_resolving,
                        Developer_comments = bugDataToEdit.Developer_comments,
                        Reopen_Reason = bugDataToEdit.Reopen_Reason,
                        Attachment = bugDataToEdit.Attachment,
                        )
                    changelogsentry.save()

                    edited = True
            else:
                formObj = reopenBugForm(instance=bugDataToEdit)
            if edited == False :
                request.session['template'] = 't_reopenBug'
                return render(request, 'consoles/t_reopenBug.html', {'theform':formObj,'un':un})
            else:
                return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
        
        return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")

    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})
# Developer
def solveBug(request, bugpk):
    if request.session['usertype'] == 'developer':
        edited = False
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        if request.method == "POST":
            formObj = solveBugForm(request.POST, instance=bugDataToEdit)
            if formObj.is_valid():
                bugDataToEdit = formObj.save(commit=False)
                bugDataToEdit.Date_of_resolving = timezone.localtime(timezone.now())
                bugDataToEdit.Status = 'Solved'
                bugDataToEdit.Developer_name = request.session['username']
                bugDataToEdit.Resolution_Status = 'Solved'
                bugDataToEdit.save()

                changelogsentry = changelogs(
                    type_of_Change = 'Bug Solved',
                    sr_no = bugDataToEdit.sr_no,
                    Defect_Id = bugDataToEdit.Defect_Id,
                    Project_name = bugDataToEdit.Project_name,
                    project_version = bugDataToEdit.project_version,
                    Browser = bugDataToEdit.Browser,
                    Url_of_page = bugDataToEdit.Url_of_page,
                    Status = bugDataToEdit.Status,
                    TimesReopened = bugDataToEdit.TimesReopened,
                    Priority = bugDataToEdit.Priority,
                    Defect_desc = bugDataToEdit.Defect_desc,
                    Steps_to_Reproduce = bugDataToEdit.Steps_to_Reproduce,
                    Date_of_finding = bugDataToEdit.Date_of_finding,
                    Tester_name = bugDataToEdit.Tester_name,
                    Developer_name = bugDataToEdit.Developer_name,
                    Resolution_Status = bugDataToEdit.Resolution_Status,
                    Date_of_resolving = bugDataToEdit.Date_of_resolving,
                    Developer_comments = bugDataToEdit.Developer_comments,
                    #Reopen_Reason = None,
                    Attachment = bugDataToEdit.Attachment,
                    )
                changelogsentry.save()

                edited = True
        else:
            formObj = solveBugForm(instance=bugDataToEdit)
        if edited == False :
            request.session['template'] = 't_setAsSolved'
            return render(request, 'consoles/t_setAsSolved.html', {'theform':formObj})
        else:
            return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Not allowed as developer."})

# Developer
def editSolution(request, bugpk, un):
    if request.session['usertype'] == 'developer':
        edited = False
        bugDataToEdit = get_object_or_404(BugSheetModel, pk=bugpk)
        if request.method == "POST":
            formObj = solveBugForm(request.POST, instance=bugDataToEdit)
            if formObj.is_valid():
                bugDataToEdit.save()

                changelogsentry = changelogs(
                    type_of_Change = 'Solution Edited',
                    sr_no = bugDataToEdit.sr_no,
                    Defect_Id = bugDataToEdit.Defect_Id,
                    Project_name = bugDataToEdit.Project_name,
                    project_version = bugDataToEdit.project_version,
                    Browser = bugDataToEdit.Browser,
                    Url_of_page = bugDataToEdit.Url_of_page,
                    Status = bugDataToEdit.Status,
                    TimesReopened = bugDataToEdit.TimesReopened,
                    Priority = bugDataToEdit.Priority,
                    Defect_desc = bugDataToEdit.Defect_desc,
                    Steps_to_Reproduce = bugDataToEdit.Steps_to_Reproduce,
                    Date_of_finding = bugDataToEdit.Date_of_finding,
                    Tester_name = bugDataToEdit.Tester_name,
                    Developer_name = bugDataToEdit.Developer_name,
                    Resolution_Status = bugDataToEdit.Resolution_Status,
                    Date_of_resolving = bugDataToEdit.Date_of_resolving,
                    Developer_comments = bugDataToEdit.Developer_comments,
                    Reopen_Reason = bugDataToEdit.Reopen_Reason,
                    Attachment = bugDataToEdit.Attachment,
                    )
                changelogsentry.save()

                edited = True
        else:
            formObj = solveBugForm(instance=bugDataToEdit)
        if edited == False :
            request.session['template'] = 't_editSolution'
            return render(request, 'consoles/t_editSolution.html', {'theform':formObj,'un':un})
        else:
            return HttpResponseRedirect("/consoles/sheetdetail/"+ request.session['projectname'] +"/0/")
    else:
        request.session['template'] = 't_error'
        return render(request, 't_error.html', {'error':"Sorry you can't access this page."})

# Export Excel
def export_xls(request):
    fn = request.session['projectname'] + ' - BRS'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="'+ fn +'.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(fn)

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Resolution_Status',
        'sr_no',
        'Project_name',
        'Browser',
        'Defect_Id',
        'Url_of_page',
        'Defect_desc',
        'Steps_to_Reproduce',
        'Priority',
        'Status',
        'TimesReopened',
        'Date_of_finding',
        'Tester_name',
        'Reopen_Reason',
        'Developer_name',
        'Date_of_resolving',
        'Developer_comments',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = BugSheetModel.objects.all().filter(Project_name=request.session['projectname']).values_list(
        'Resolution_Status',
        'sr_no',
        'Project_name',
        'Browser',
        'Defect_Id',
        'Url_of_page',
        'Defect_desc',
        'Steps_to_Reproduce',
        'Priority',
        'Status',
        'TimesReopened',
        'Date_of_finding',
        'Tester_name',
        'Reopen_Reason',
        'Developer_name',
        'Date_of_resolving',
        'Developer_comments',
    )
    for row in rows:    
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response



def message(request):
    # try:
        if request.method == 'POST':
            sender = User.objects.get(username=request.user)
            receiver = User.objects.get(id=request.POST.get('user_id'))
            notify.send(sender, recipient=receiver, verb='Message', description=request.POST.get('message'))
            return redirect('consoles:index1')
        else:
            return HttpResponse("Invalid request")
    # except Exception as e:
    #     print(e)
    #     return HttpResponse("Please login from admin site for sending messages")
def index1(request):
    try:
        users = User.objects.all()
        print(request.user)
        user = User.objects.get(username=request.user)
        return render(request, 'consoles/index1.html', {'users': users, 'user': user})
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages.")


