from django.db import models
from django.forms import ModelForm

#Django automatically creates a primary key field that autoincrements
#passwords currently not hashed
class User(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200)
    active_session = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    # I might change this so that it just checks for the user, then I can check the password later
    def is_real(username):
        for user in User.objects.all():
            if user.username == username:
                return user
        return User()
    
class Workout(models.Model):
    name = models.CharField(max_length=200)
    
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

