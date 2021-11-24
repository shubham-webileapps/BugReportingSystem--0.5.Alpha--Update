from django.db import models
from django.contrib.auth.models import User, models
User._meta.get_field('email').__dict__['_unique'] = True


# Create your models here.


userType = (
    ('developer', 'developer'),
    ('tester', 'tester'),
)


class accountModel(models.Model):
    # extending the django user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # if dev then false, if tester then true, helps in distinguishing
    UserType = models.CharField(max_length=500, choices=userType)
    username = models.CharField(max_length=255, primary_key=True)
    # for dev, it is the count of bugs solved, for tester it is number of bugs found
    bugCount = models.IntegerField(default=0)
    projectCount = models.IntegerField(default=0)

    
    def save(self, *args, **kwargs):
        self.username = str(self.user)
        super(accountModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class masterPassword(models.Model):
    masterPass = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.masterPass

class passwordResetModel(models.Model):
    email = models.CharField(max_length=500)
    guid = models.CharField(max_length=500)


