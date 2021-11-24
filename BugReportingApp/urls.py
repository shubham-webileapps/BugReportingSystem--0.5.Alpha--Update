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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from accountManager import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accountManager/', include('accountManager.urls')),
    path('consoles/', include('consoles.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    
    
    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accountManager/t_changePassword.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accountManager/password-reset/password_reset.html',
             subject_template_name='accountManager/password-reset/password_reset_subject.txt',
             email_template_name='accountManager/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accountManager/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accountManager/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accountManager/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
