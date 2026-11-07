from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
import html
import cowsay
from .models import *
from .forms import *
from django.utils import timezone
from datetime import date

def grab_user_hist(user_history, exercises, workout):
    user_ex = []
        
    for exercise in exercises:
        ex_history = user_history.filter(exercise_id = exercise)
        new_ex = UserExercises(workout_id = workout, exercise_id = exercise)
        if(ex_history.exists()):
            temp = UserExercises.objects.filter(workout_id__date_completed__gte=timezone.now() - datetime.timedelta(days=7))
            if(temp.exists()):
                temp.order_by('workout_id__date_completed')
                last_wrkt = temp[0]
                if(last_wrkt.reps < 12):
                    new_reps = last_wrkt.reps + 1
                    new_weight = last_wrkt.weight
                else:
                    new_reps = 8
                    new_weight = last_wrkt.weight + 5
                new_ex.weight = new_weight
                new_ex.reps = new_reps
                new_ex.sets = 3
        user_ex.append(new_ex)
    return user_ex
        

def index(request): 
    # Return as plain text so the browser preserves the formatting
    return render(request, "lzwrkts/index.html")

def home(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        return render(request, "lzwrkts/home.html", {"user_username":user_username})
    else:
        return render(request, "lzwrkts/index.html")

def new_workout(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):

        # Get the 'msg' parameter from the URL, default to 'Moo!'
        message = request.GET.get('msg', 'WORK IN PROGRESS.')

        e = Exercise.objects.get(name='3/4 Sit-Up')
        #test_image2 = Exercise.objects.get(name='3/4 Sit-Up').image2_path
        
        # Generate the cowsay ASCII art
        cow_art = html.escape(cowsay.get_output_string('cow', message))
        context = {'cow_art': cow_art,
                   'e': e,
                   'user_username': user_username,
                   }
        
        # Return as plain text so the browser preserves the formatting
        return render(request, "lzwrkts/new_workout.html", context)
    else:
        return render(request, "lzwrkts/index.html")

def suggested_workout(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        wrkt_ids = request.session.get('gen_wrkt_ids', [])
        exercises = [Exercise.objects.get(pk=pk) for pk in wrkt_ids]

        curr_wrkt = UserWorkouts(user_id = user)
        user_history = UserExercises.objects.filter(workout_id__user_id = user_username)

        if(user_history.exists()):
            #see when a workout of the same muscle group was done 
            #exercise id is the magic field
            user_ex = grab_user_hist(user_history, exercises, curr_wrkt)

            #see if any of current exercises match the user history
            #if they do, check the date they were completed
            #if it's a week ago or less, increase rep (up to 12 - if number of reps is 12, increase weight) 
            #if it's been longer than a week, keep it the same (for now, there's probably a more sciencey way to do it)
             
            #fuck, this is gonna be another form
            #create a new user exercise for each with the information gathered, then put it in the session so the form can access it
            print("beans")
        else:
            user_ex = []
            for exercise in exercises:
                new_ex = UserExercises(workout_id = curr_wrkt, exercise_id = exercise)
                user_ex.append(new_ex)

        # Get the 'msg' parameter from the URL, default to 'Moo!'
        message = request.GET.get('msg', 'WORK IN PROGRESS.')

        e = Exercise.objects.get(name='3/4 Sit-Up')
        #test_image2 = Exercise.objects.get(name='3/4 Sit-Up').image2_path
        
        # Generate the cowsay ASCII art
        cow_art = html.escape(cowsay.get_output_string('cow', message))
        context = {'cow_art': cow_art,
                   'e': e,
                   'user_username': user_username,
                   'wrkt_ids': wrkt_ids,
                   'exercises': exercises,
                   }
        return render(request, "lzwrkts/suggested_workout.html", context)
    else:
        return render(request, "lzwrkts/index.html")

def workout_generator(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if request.method == "POST":
            form = WorkoutForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data["group"]
                numsets = form.cleaned_data["numsets"]
                bonus = form.cleaned_data["bonus"]

                gen_wrkt = Exercise.grab_exercises(group, numsets, bonus)
                request.session['gen_wrkt_ids'] = [exercise.pk for exercise in gen_wrkt]
                return HttpResponseRedirect(reverse("lzwrkts:suggestedwrkt", args=(user.username,)))
            else:
                #idk what else to do here
                return render(request, "lzwrkts/new_workout.html", {"user_username": user_username})
    else:
        return render(request, "lzwrkts/new_workout.html", {"user_username": user_username})

def search_exercises(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        # Get the 'msg' parameter from the URL, default to 'Moo!'
        message = request.GET.get('msg', 'WORK IN PROGRESS.')
        
        # Generate the cowsay ASCII art
        cow_art = html.escape(cowsay.get_output_string('cow', message))
        context = {'cow_art': cow_art}
        
        # Return as plain text so the browser preserves the formatting
        return render(request, "lzwrkts/search_page.html", context)
    else:
        return render(request, "lzwrkts/index.html")
    
def workout_history(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        # Get the 'msg' parameter from the URL, default to 'Moo!'
        message = request.GET.get('msg', 'WORK IN PROGRESS.')
        
        # Generate the cowsay ASCII art
        cow_art = html.escape(cowsay.get_output_string('cow', message))
        context = {'cow_art': cow_art}
        
        # Return as plain text so the browser preserves the formatting
        return render(request, "lzwrkts/search_page.html", context)
    else:
        return render(request, "lzwrkts/index.html")


def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["user"]
            password = form.cleaned_data["pwd"]
            try:
                real_user = User.objects.get(username = name)
                if(real_user.password == password):
                    real_user.active_session = True
                    real_user.save(update_fields=['active_session'])
                    return HttpResponseRedirect(reverse("lzwrkts:home", args=(real_user.username,)))
                else: 
                    return render(
                        request,
                        "lzwrkts/index.html",
                        {
                            "form": form,
                            "error_message": "Incorrect Username/Password. Please try again",
                        },
                    )
            except User.DoesNotExist: 
                return render(
                    request,
                    "lzwrkts/index.html",
                    {
                        "form": form,
                        "error_message": "Incorrect Username/Password. Please try again",
                    },
                )
        else:
            return render(
                    request,
                    "lzwrkts/index.html",
                    {
                        "form": form,
                        "error_message": "Incorrect Username/Password. Please try again",
                    },
                )
    else:
        form = UserForm()
        return render(request, "lzwrkts/index.html", {"form": form})

def signup(request):
    if request.method == "POST":
        new_user = LoginForm(request.POST)
        if new_user.is_valid(): 
            new_user.save()
            return render(
                    request,
                    "lzwrkts/index.html",
                    {
                        "error_message": "Success! Please log in",
                    },
                )
        else:
            return render(
                    request,
                    "lzwrkts/index.html",
                    {
                        "new_user": new_user,
                        "error_message": new_user.errors,
                    },
                )
    else:
        new_user = UserForm()
        return render(request, "lzwrkts/index.html", {"form": new_user})
    




def health_check(request):
    return HttpResponse("OK", status=200)