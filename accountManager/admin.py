from django.contrib import admin
from django.contrib.auth.models import User
from .models import accountModel
from .models import masterPassword
# Register your models here.


class accountModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'UserType', 'bugCount', 'projectCount')


admin.site.register(accountModel, accountModelAdmin)
admin.site.register(masterPassword)
