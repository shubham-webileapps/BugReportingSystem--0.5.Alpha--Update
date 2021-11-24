from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accountManager.forms import *
from accountManager.forms import UserForm1
from accountManager.models import accountModel, masterPassword, passwordResetModel
from consoles.models import BugSheetModel, AddNewProject, TaskAssignment
from django.contrib.auth.models import User
from consoles.views import showConsoles
import random
import uuid 
# from django.db import connection
from django.core.serializers import serialize
import json

def index(request):

    # print(request.user)

    r = lambda: random.randint(0,255)
    # print('#%02X%02X%02X' % (r(),r(),r()))
    request.session['solved1'] = json.loads(serialize('json',BugSheetModel.objects.filter(Resolution_Status='Solved')))
    request.session['pending1'] = json.loads(serialize('json',BugSheetModel.objects.filter(Resolution_Status='Pending')))
    # print((serialize('json',BugSheetModel.objects.filter(Resolution_Status='Solved'))))
    request.session['bugstotal'] = BugSheetModel.objects.count()
    request.session['bugssolved'] = BugSheetModel.objects.filter(Resolution_Status='Solved').count()
    request.session['bugspending'] = BugSheetModel.objects.filter(Resolution_Status='Pending').count()
    request.session['totalprojects'] = AddNewProject.objects.count()
    request.session['totaldevelopers'] = accountModel.objects.filter(UserType='developer').count()
    request.session['totaltesters'] = accountModel.objects.filter(UserType='tester').count()
    projlist = list(AddNewProject.objects.all())
    ratiodata = []
    for i in range (0, request.session['totalprojects']):
        x = []

        x.append(str(projlist[i]))
        
        r = lambda: random.randint(0,255)
        x.append(str('#%02X%02X%02X' % (r(),r(),r()))) 
        
        x.append(int(BugSheetModel.objects.filter(Project_name = str(projlist[i])).count()))
        #x.append(float(int(BugSheetModel.objects.filter(Project_name = str(projlist[i])).count())/int(request.session['bugstotal'])*100))

        ratiodata.append(x)
    
    if 'usertype' in request.session:
        if request.session['usertype'] == 'tester':
            getHisBugCount = BugSheetModel.objects.filter(Tester_name = request.session['username']).count()
            getHisProject = TaskAssignment.objects.filter(AssignedTo = request.session['username']).count()
        elif request.session['usertype'] == 'developer':
            getHisBugCount = BugSheetModel.objects.filter(Developer_name = request.session['username']).count()
            getHisProject = TaskAssignment.objects.filter(AssignedTo = request.session['username']).count()
        elif request.session['usertype'] == 'admin':
            getHisBugCount = 0
            getHisProject = 0
            pass
        
        accountModel.objects.filter(username = request.session['username']).update(bugCount = int(getHisBugCount))
        accountModel.objects.filter(username = request.session['username']).update(projectCount = int(getHisProject))
        request.session['userbugcount'] = int(getHisBugCount)
        request.session['userprojectcount'] = int(getHisProject)
        if request.session['usertype'] == 'admin':

            developerList = accountModel.objects.filter(UserType='developer')
            testerList = accountModel.objects.filter(UserType='tester')
            request.session['template'] = 'index'
            return render(request, 'accountManager/index.html',{'ratiodata':ratiodata,'dlist': developerList,'tlist':testerList})
        else:
            request.session['template'] = 'index'
            return render(request, 'accountManager/index.html',{'ratiodata':ratiodata})
    else:
            request.session['template'] = 'index'
            return render(request, 'accountManager/index.html',{'ratiodata':ratiodata})

def aboutme(request):
    request.session['template'] = 't_aboutme'
    return render(request, 'accountManager/t_aboutme.html',)

@login_required
def user_logout(request):
    logout(request)
    request.session.flush()
    request.session['template'] = 'index'
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False 
    if request.method == 'POST': # register button clicked on the t_register.html 
        user_form = UserForm(data=request.POST) # Form grabbed
        profile_form = UserMoreDetailsForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            masterPasswordCount = masterPassword.objects.filter(
                masterPass=profile_form.cleaned_data['masterpassword']).count()
            if masterPasswordCount != 0:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                email = request.POST.get('email')
                from random import randint
                User.objects.filter(email=email).update(username=email.split('@')[0]+str(randint(100, 999)))
                profile = profile_form.save(commit=False)
                u=User.objects.get(email=email)
                # user1=UserForm1()
                # user1=UserForm1(request.GET or None, instance=u)
                profile.user = u
                profile.save()
                registered = True
            else:
                request.session['template'] = 't_error'
                return render(request, 't_error.html', {'error':"Wrong MasterPassword! Contact Admin."})
        else:
            pass
            # print(user_form.errors, profile_form.errors)
    else:   # Clicked on Register link, grab forms and render t_register.html 
        user_form = UserForm()
        profile_form = UserMoreDetailsForm()
    request.session['template'] = 't_register'
    return render(request, 'accountManager/t_register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    formObj = UserLoginForm()
    if 'username' in request.session:
        return showConsoles(request)
    elif request.method == 'POST':
        formObj = UserLoginForm(request.POST)
        # username = request.POST.get('Username')
        email = request.POST.get('Email')
        u=json.loads(serialize('json',User.objects.filter(email=email)))[0]
        username=u['fields']['username']
        # username=username.username
        password = request.POST.get('Password')
        themasterpassword = request.POST.get('MasterPassword')

        # print (username + password + themasterpassword+email)

        masterPasswordCount = masterPassword.objects.filter(
            masterPass=themasterpassword).count()
        # checking the masterpassword is there or not
        if masterPasswordCount != 0:
            user = authenticate(username=username, password=password)
            if user:
                
                if user.is_active:
                    login(request, user)
                    userPrimaryKey = User.objects.only(
                        'id').get(username=username).id
                    if user.is_superuser == True:
                        whatUserType = "admin"
                    else:
                        whatUserType = accountModel.objects.only('UserType').get(user=userPrimaryKey).UserType
                    request.session['username'] = username
                    request.session['usertype'] = whatUserType
                    request.session['userPK'] = userPrimaryKey
                    return index(request)
                else:
                    request.session['template'] = 't_error'
                    return render(request, 't_error.html', {'error':"Your account was inactive."})
            else:
                request.session['template'] = 't_error'
                return render(request, 't_error.html', {'error':"Invalid login details given"})
        else:
            request.session['template'] = 't_error'
            return render(request, 't_error.html', {'error':"Wrong MasterPassword! Contact Admin."})
    else:
        request.session['template'] = 't_login'
        return render(request, 'accountManager/t_login.html', {'theform':formObj})

