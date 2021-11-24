from django import forms
from consoles.models import BugSheetModel
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


PRIORITY_ = ( 
    ('Lowest','Lowest'),
    ('Low','Low'),
    ('Medium','Medium'),
    ('High','High'),
    ('Highest','Highest') 
)


class testerBugForm(forms.ModelForm):

    class Meta:
        model = BugSheetModel
        fields = [
            'project_version',
            'Browser',
            'Url_of_page',
            'Priority',
            'Defect_desc',
            'Steps_to_Reproduce',
        #    'Date_of_finding',
            'Attachment'
        ]
        widgets = {
            'project_version':forms.TextInput(attrs={"pattern":"[0-9]+([\.][0-9]{0,2})","title":"Only Float number's are Allowed","class": "new-class-name two",}),
            'Browser':forms.TextInput(attrs={"pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed",'id':'Browser',"class": "new-class-name two",}),
            'Defect_desc':forms.TextInput(attrs={"placeholder": "Your description",'id':"Defect_desc","pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed","class": "new-class-name two","rows": 7,'cols': 120}),
            'Steps_to_Reproduce':forms.TextInput(attrs={"placeholder": "Your description",'id':"Defect_desc","pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed","class": "new-class-name two","rows": 7,'cols': 120}),
#            'Date_of_finding':  DatePickerInput(format='%Y-%m-%d')
             'Attachment' : forms.FileInput(attrs={"class": "form-control bg-white",})
        }
    

class editBugForm(forms.ModelForm):

    class Meta:
        model = BugSheetModel
        fields = [
            'project_version',
            'Browser',
            'Url_of_page',
            'Priority',
            'Defect_desc',
            'Steps_to_Reproduce',
#            'Date_of_finding',
            'Attachment'
        ]

        widgets = {
            'project_version':forms.TextInput(attrs={"pattern":"[0-9]{1,4}+[.]+[0-9]{1,4}","title":"Only Float number's are Allowed","class": "new-class-name two",}),
            'Browser':forms.TextInput(attrs={"pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed","class": "new-class-name two",}),
            'Defect_desc':      forms.Textarea(attrs={"placeholder": "Your description","pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed","class": "new-class-name two","rows": 7,'cols': 120}),
#            'Date_of_finding':  DatePickerInput(format='%Y-%m-%d')
             'Attachment' : forms.FileInput(attrs={"class": "form-control bg-white",})
        }
    

class solveBugForm(forms.ModelForm):

    class Meta:
        model = BugSheetModel
        fields = [
#            'Date_of_resolving',
            'Developer_comments']
        widgets = {
            'Developer_comments':      forms.Textarea(attrs={"placeholder": "Your description","pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed","class": "new-class-name two","rows": 7,'cols': 120}),
#            'Date_of_resolving':  DatePickerInput(format='%Y-%m-%d')
        }



class reopenBugForm(forms.ModelForm):

    class Meta:
        model = BugSheetModel
        fields = [
            'Reopen_Reason'
        ]
        widgets = {
            'Reopen_Reason':      forms.Textarea(attrs={"placeholder": "Your description","pattern":"[a-zA-Z ]*","title":"Only Strings are Allowed","class": "new-class-name two","rows": 7,'cols': 120}),
#            'Date_of_resolving':  DatePickerInput(format='%Y-%m-%d')
        }


class screenShotForm(forms.ModelForm):

    class Meta:
        model = BugSheetModel
        fields = [
            'Attachment'
        ]
