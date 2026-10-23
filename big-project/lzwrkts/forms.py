from django import forms


class UserForm(forms.Form):
    user = forms.CharField(label="user", max_length=200)
    pwd = forms.CharField(label="pwd", max_length=200)