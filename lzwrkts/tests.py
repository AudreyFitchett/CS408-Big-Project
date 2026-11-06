from django.test import TestCase
import pytest
from .models import *
import json
import random
from django.utils import timezone
import datetime
from django.db.models import Q

# Create your tests here.
pytestmark = pytest.mark.django_db

#just wanna make sure everything is loaded in properly
#these should really never change
class TestDBInit:
    def test_muscles_exists(self):
        assert Muscles.objects.exists() and Muscles.objects.count() == 17
    def test_exercise_exists(self):
        assert Exercise.objects.exists() and Exercise.objects.count() == 876

    @pytest.mark.parametrize(
        "index",
        [random.randint(0, 16), random.randint(0, 16), random.randint(0, 16), random.randint(0, 16), random.randint(0, 16)],
    )
    def test_muscles_init(self, index):
        with open('exercises.json', 'r') as file:
            data = json.load(file)
            name = data[index]['primaryMuscles'][0]
            group = None

            if(name == 'hamstrings' or name == 'glutes' or name ==  'calves' or name == 'quadriceps'): 
                # group = Group.objects.get(name='legs')
                group = 'legs'
            elif(data[index].get('force') == 'pull' or data[index].get('force') == 'push'):
                #group = Group.objects.get(name=item['force'])
                group = data[index].get('force')

        assert Muscles.objects.filter(name = name, exercise_group = group).exists() is not None
    
    @pytest.mark.parametrize(
        "index",
        [559, random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)],
    )
    def test_exercises_init(self, index):
        with open('exercises.json', 'r') as file:
            data = json.load(file)
            name = data[index]['name']
            category = data[index]['category']
            equipment = data[index]['equipment']
            primary_muscle = Muscles.objects.get(name=data[index]['primaryMuscles'][0])
            level = data[index]['level']
            image1_path = data[index]['images'][0]
            image2_path = data[index]['images'][1]

            instructions = data[index].get('instructions', [])
            if isinstance(instructions, list):
                instructions = " ".join(instructions)
            else:
                instructions = str(instructions)
            
        assert Exercise.objects.filter(name = name, category = category, equipment = equipment, primary_muscle = primary_muscle, 
                            instructions = instructions, level = level, image1_path = image1_path, image2_path = image2_path).exists() is True

class TestDBUploading():

    def test_update_workout(self):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user_id=user)

        date = datetime.datetime(2026, 7, 15, 12, 0, 0)
        date = timezone.make_aware(date) 

        workout.date_completed = date
        workout.save()
        assert UserWorkouts.objects.filter(user_id=user.pk, date_completed=date) is not None

    @pytest.mark.parametrize(
        "index",
        [random.randint(0, 50)],#, random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)],
    )
    def test_add_user_exercise(self, index):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user_id=user)
        exercise = Exercise.objects.get(name="90/90 Hamstring")

        UserExercises.objects.create(workout_id = workout, exercise_id = exercise, weight = index, reps = index, sets=index)

        assert UserExercises.objects.filter(workout_id = workout, exercise_id = exercise, weight = index, reps = index, sets=index).exists() is True

    @pytest.mark.parametrize(
        "index",
        [random.randint(0, 50)], #, random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)],
    )
    def test_update_user_exercise(self, index):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user_id=user)
        exercise = Exercise.objects.get(name="90/90 Hamstring")

        user_exercise = UserExercises.objects.create(workout_id = workout, exercise_id = exercise, weight = index, reps = index, sets=index)


        user_exercise.sets = 1
        user_exercise.save()

        assert UserExercises.objects.filter(workout_id = workout, exercise_id = exercise, weight = index, reps = index, sets=index).exists() is False

class TestOtherStuffIg:
    
    def test_grab_exercises(self):
        group = "pull"
        numsets = 4
        bonus = "yes"
        workout = list()
        #filter out by group
        type = Exercise.objects.filter(
            #things that people can feasible have at home only
            Q(equipment = "barbell") | Q(equipment = "dumbbell") | Q(equipment = "kettlebells"),
            level = "beginner",
            primary_muscle__in=Muscles.objects.filter(exercise_group = group),
            )
        #for now, we're going to hardcode it at beginner. Later, I can add level to the form
        #barbell, dumbbell, kettlebells
        #filter out by equipment
        #filter out by category? 
        choice = [2, 17, 8, type.count() - 1]
        abs = 0
        

        for i in range(numsets):
            workout.append(type[choice[i]])
        
        if(bonus == "surprise me"):
            abs = random.randint(0,1)
        if(bonus == "yes" or abs == 1):
            type = Exercise.objects.filter(primary_muscle__in=Muscles.objects.filter(name = 'abdominals'))
            workout.append(type[4])
            assert len(workout) == 5 and Muscles.objects.get(name = workout[4].primary_muscle).name == 'abdominals'
        else:
            assert len(workout) == 4 and Muscles.objects.get(name = workout[0].primary_muscle).exercise_group == "pull"
    
    def test_grab_user_hist(self):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user_id=user)
        exercises = [Exercise.objects.all()[0], Exercise.objects.all()[17], Exercise.objects.all()[52]]
        user_history = UserExercises.objects.filter(workout_id__user_id = user.username)
        new_reps
        new_weight


        #okay, what am I doing?
        if(user_history.Exists()):
            for exercise in exercises:
                ex_history = user_history.filter(exercise_id = exercise)
                if(ex_history.Exists()):
                    temp = UserWorkouts.objects.filter(pk=ex_history.workout_id).filter(date_completed = datetime.date.today() - 7)
                    if(temp.Exists()):
                        temp.order_by('date_completed')
                        last_wrkt = temp[0]
                        if(last_wrkt.numreps < 12):
                            new_reps = last_wrkt.numreps + 1
                        else:
                            new_reps = 8
                            new_weight = last_wrkt.weight + 2.5
            #see when a workout of the same muscle group was done 
            #see if any of current exercises match the user history
            #if they do, check the date they were completed
            #if it's a week ago or less, increase rep (up to 12 - if number of reps is 12, increase weight) 
            #if it's been longer than a week, keep it the same (for now, there's probably a more sciencey way to do it)
             
            #fuck, this is gonna be another form
            #create a new user exercise for each with the information gathered, then put it in the session so the form can access it
        assert True
    
    

    


       
