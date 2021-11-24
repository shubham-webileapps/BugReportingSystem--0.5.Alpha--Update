from django import forms
from django.contrib.auth.password_validation import validate_password
from accountManager.models import accountModel
from django.contrib.auth.models import User

userType = (
    ('developer', 'developer'),
    ('tester', 'tester'),
)


class UserForm(forms.ModelForm):
    # username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control','pattern':'[A-Za-z0-9]*','title':'username shuold be a combination of numbers and alphabets'}))
    password = forms.CharField(widget=forms.PasswordInput(),validators=[validate_password])
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control','name':'email','pattern':'[A-Za-z0-9._%+-]+@[A-Za-z.]+\.[A-Za-z]{1,63}$','title':'Write a Orignal Email'}))
    class Meta():
        model = User
        # fields = ('username', 'password', 'email')
        fields = ('email','password')

class UserForm1(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control','pattern':'[A-Za-z0-9]*','title':'username shuold be a combination of numbers and alphabets'}))
    password = forms.CharField(widget=forms.PasswordInput(),validators=[validate_password])
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'abc@xyz.com', 'class': 'form-control','name':'email','pattern':'[A-Za-z0-9._%+-]+@[A-Za-z.]+\.[A-Za-z]{1,63}$','title':'Write a Orignal Email'}))
    class Meta():
        model = User
        fields = ('username', 'password', 'email')
        # fields = ('email','password')


class UserMoreDetailsForm(forms.ModelForm):
    '''istester = forms.BooleanField(required=False,initial=False,label='Are you a Tester? ')'''
    UserType = forms.ChoiceField(choices=userType, required=True)
    masterpassword = forms.CharField(
        required=True, widget=forms.PasswordInput())

    class Meta():
        model = accountModel
        fields = ('UserType', 'masterpassword')


class UserLoginForm(forms.Form):

    # Username = forms.CharField()
    Email = forms.EmailField()
    Password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    MasterPassword = forms.CharField(max_length=32, widget=forms.PasswordInput)

class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField()
    
class ResetPasswordCodeForm(forms.Form):
    codeRecieved = forms.CharField(
        required=True, widget=forms.PasswordInput())

class newPassword(forms.Form):
    password = forms.CharField(
        required=True, widget=forms.PasswordInput())