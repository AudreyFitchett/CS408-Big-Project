from django.db import models
from django.forms import ModelForm
from django.utils import timezone
import random
from django.db.models import Q

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
# class ExerciseGroup(models.Model):
#     #there's only three rn and their names are all distinct so I think it's fine
#     name = models.CharField(max_length=200)
    
class Muscles(models.Model):
    #why didn't I make this the primary key? 
    name = models.CharField(max_length=200)
    exercise_group = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    #I might want to change this at some point
    #exercise_group = models.ForeignKey(ExerciseGroup, on_delete=models.CASCADE, null=True)
    equipment = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    instructions = models.TextField(null=True)
    level = models.TextField(null=True)
    image1_path = models.CharField(max_length=200, null=True)
    image2_path = models.CharField(max_length=200, null=True)
    primary_muscle = models.ForeignKey(Muscles, on_delete=models.SET_NULL, null=True)
    #link = models.URLField()
    #the database I'm pulling the info from has a description for each, which I think is worth it, so
    #add that field here

    def __str__(self):
        return self.name

    def grab_exercises(group, numsets, bonus):
        workout = list()
        abs = 0

        type = Exercise.objects.filter(
            #things that people can feasible have at home only
            Q(equipment = "barbell") | Q(equipment = "dumbbell") | Q(equipment = "kettlebells"),
            level = "beginner",
            primary_muscle__in=Muscles.objects.filter(exercise_group = group),
            )
        #for now, we're going to hardcode it at beginner. Later, I can add level to the form
        #barbell, dumbbell, kettlebells
        #filter out by equipment
        choice = random.sample(range(0, type.count() - 1), 4)

        for i in range(numsets):
            workout.append(type[choice[i]])

        if(bonus == "surprise_me"):
            abs = random.randint(0,1)
        if(bonus == "yes" or abs == 1):
            type = Exercise.objects.filter(primary_muscle__in=Muscles.objects.filter(name = 'abdominals'))
            workout.append(type[4])

        return workout


class UserWorkouts(models.Model):
    date_completed = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class UserExercises(models.Model):
    workout_id = models.ForeignKey(UserWorkouts, on_delete=models.CASCADE)
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    #TODO: this will have to be set to null=True
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    reps = models.PositiveSmallIntegerField(null=True)
    sets = models.PositiveSmallIntegerField(null=True)
    #TODO: I definitley forgot to add the liked field 
    
    
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

