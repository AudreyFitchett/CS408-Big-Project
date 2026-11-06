from django import forms

#connects to the name field in the html forms, fyi
class UserForm(forms.Form):
    user = forms.CharField(label="user", max_length=200)
    pwd = forms.CharField(label="pwd", max_length=200)

class WorkoutForm(forms.Form):
    group = forms.CharField(label="group", max_length=200)
    numsets = forms.IntegerField(label="numsets")
    bonus = forms.CharField(label="group", max_length=200)

