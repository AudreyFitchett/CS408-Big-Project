from django import forms

#connects to the name field in the html forms, fyi
class UserForm(forms.Form):
    user = forms.CharField(label="user", max_length=200)
    pwd = forms.CharField(label="pwd", max_length=200)

class WorkoutForm(forms.Form):
    group = forms.CharField(label="group", max_length=200)
    numsets = forms.IntegerField(label="numsets")
    bonus = forms.CharField(label="group", max_length=200)

class ExerciseForm(forms.Form):
    exercise_pk = forms.IntegerField(widget=forms.HiddenInput())
    weight = forms.DecimalField(label="weight", max_digits=4, decimal_places=1, required=False)
    reps = forms.IntegerField(label="reps", required=False)
    sets = forms.IntegerField(label="sets", required=False)
    liked = forms.BooleanField(label="liked", required=False)

class SearchForm(forms.Form):
    search_term = forms.CharField(label="group", max_length=200, required=False)
    filter = forms.MultipleChoiceField(
        choices={
            'push': 'push', 
            'pull': 'pull', 
            'legs': 'legs', 
            'liked': 'liked',},
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

