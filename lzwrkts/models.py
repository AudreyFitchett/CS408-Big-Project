from django.db import models
from django.forms import ModelForm
from django.utils import timezone

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
    
# Exercises
# Workouts 
# Muscles 
# Exercise group
# User Workouts

#reminder, default id when an explicit one isn't set
class ExerciseGroup(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    #I might want to change this at some point
    exercise_group = models.ForeignKey(ExerciseGroup, on_delete=models.CASCADE)
    link = models.URLField()
    #the database I'm pulling the info from has a description for each, which I think is worth it, so
    #add that field here

class Muscles(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    exercise_group = models.ForeignKey(ExerciseGroup, on_delete=models.CASCADE)

class UserWorkouts(models.Model):
    date_completed = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class UserExercises(models.Model):
    workout_id = models.ForeignKey(UserWorkouts, on_delete=models.CASCADE)
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    reps = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    
    
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

