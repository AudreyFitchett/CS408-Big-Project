from django.test import TestCase
import pytest
from .models import *
import json
import random
from django.utils import timezone
import datetime

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
        [559, random.randint(0, 875), random.randint(0, 875), random.randint(0, 875), random.randint(0, 875)],
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
                            instructions = instructions, level = level, image1_path = image1_path, image2_path = image2_path) is not None

class IdkWhyImDoingClasses():

    def test_update_workout(self):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user=user)

        date = datetime.datetime(2026, 7, 15, 12, 0, 0)
        date = timezone.make_aware(date) 

        workout.date_completed = date
        workout.save()
        assert UserWorkouts.objects.filter(user=user, date_completed=date) is not None

    @pytest.mark.parametrize(
        "index",
        [random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)],
    )
    def test_add_user_exercise(self, index):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user=user)
        exercise = Exercise.objects.get(name="90/90 Hamstring")

        UserExercises.objects.create(workout, exercise, index, index, index)

        assert UserExercises.objects.filter(workout, exercise, index, index, index) is not None
    
    @pytest.mark.parametrize(
        "index",
        [random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)],
    )
    def test_update_user_exercise(self, index):
        user = User.objects.create(username="temp", password="1234")
        workout = UserWorkouts.objects.create(user=user)
        exercise = Exercise.objects.get(name="90/90 Hamstring")

        user_exercise = UserExercises.objects.create(workout, exercise, index, index, index)

        user_exercise.sets = index + 1
        user_exercise.save()

        assert UserExercises.objects.filter(workout, exercise, index, index, index) is None
     
    
    

    


       
