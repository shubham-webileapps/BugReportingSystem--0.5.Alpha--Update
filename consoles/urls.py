"""BugReportingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import path, include
from consoles import views
import notifications.urls

# SET THE NAMESPACE!
app_name = 'consoles'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url('BugSheet/', views.showConsoles, name='BugSheet'),
    
    path('sheetdetail/<str:pk>/<str:fv>/', views.sheetDetail, name='sheet_detail'),
    path('allactivity/', views.showAllActivity, name='all_activity'),
    path('logsdetail/<str:did>/', views.logsDetail, name='logs_detail'),
    path('sheetdetailorderd/<str:ob>/<str:pk>/', views.sheetDetailOrderBY, name='sheet_detail_orderby'),
    path('rowdetail/<str:projname>/<str:bugModelPK>/', views.rowDetail, name='row_detail'),
    path('logrowdetail/<str:projname>/<str:bugModelPK>/', views.logrowDetail, name='log_row_detail'),
    path('addNewBug/', views.newBugYey, name='NewBug'),
    path('editNewBug/<str:un>/<str:bugpk>', views.editNewBug, name='EditBug'),
    path('reopenBug/<str:un>/<str:bugpk>', views.reopenNewBug, name='ReopenBug'),
    path('SkipBug/<str:un>/<str:bugpk>', views.SkipBug, name='SkipBug'),
    path('CloseBug/<str:un>/<str:bugpk>', views.CloseBug, name='CloseBug'),
    path('dropdowntester/<str:un>/<str:bugpk>', views.dropdowntester, name='dropdowntester'),
    
    path('setAsSolved/<str:bugpk>', views.solveBug, name='SolveBug'),
    path('editSolution/<str:un>/<str:bugpk>', views.editSolution, name='EditSolution'),

    path('exportXLS/', views.export_xls, name='exportXLS'),
    path('adminConsole', views.adminConsole, name='adminConsole'),
    path('index1', views.index1, name='index1'),
    path('message', views.message, name='message'),
    url('^notifications/', include(notifications.urls, namespace='notifications')),
]
