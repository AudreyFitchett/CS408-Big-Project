from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="user", max_length=200)
    password = forms.CharField(label="pwd", max_length=200)