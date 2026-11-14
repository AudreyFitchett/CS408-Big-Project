from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
import html
import cowsay
from .models import *
from .forms import *
from django.utils import timezone
import datetime
from django.forms import formset_factory
from .forms import ExerciseForm
from itertools import pairwise

def grab_user_hist(user_history, exercises):
    user_ex = []
        
    for exercise in exercises:
        ex_history = user_history.filter(exercise_id = exercise)
        new_ex = UserExercises(exercise_id = exercise)
        if(ex_history.exists()):
            temp = ex_history.filter(workout_id__date_completed__gte=timezone.now() - datetime.timedelta(days=7))
            if(temp.exists()):
                temp.order_by('workout_id__date_completed')
                last_wrkt = temp[0]
                if(last_wrkt.reps < 12):
                    new_reps = last_wrkt.reps + 1
                    new_weight = last_wrkt.weight
                    new_sets = last_wrkt.sets
                else:
                    new_reps = 8
                    new_weight = last_wrkt.weight + 5
                    new_sets = 3
                new_ex.weight = new_weight
                new_ex.reps = new_reps
                new_ex.sets = new_sets
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
        #FOR DEMO PUPROSES ONLY
        #exercises = [Exercise.objects.get(name='Alternating Kettlebell Row'), Exercise.objects.get(name='Alternating Renegade Row'), Exercise.objects.get(name = 'Barbell Ab Rollout - On Knees'),]
        user_history = UserExercises.objects.filter(workout_id__user_id = user_username)

        if(user_history.exists()):
            user_ex = grab_user_hist(user_history, exercises)
        else:
            user_ex = []
            for exercise in exercises:
                new_ex = UserExercises(exercise_id = exercise)
                user_ex.append(new_ex)
        future_exercises = {}
        for exercise in user_ex:
            ex_id_str = str(exercise.exercise_id.pk)
            future_exercises[ex_id_str] = {
                'exercise_id': exercise.exercise_id.pk,
                'weight': float(exercise.weight) if exercise.weight is not None else 0.0,
                'reps': exercise.reps,
                'sets': exercise.sets,
                'liked': exercise.liked,
            }
        request.session['future_exercises'] = future_exercises

        ExerciseFormSet = formset_factory(ExerciseForm, extra=0) # extra=0 prevents blank forms at the end

        initial_data = [
            {'exercise_pk': ex.exercise_id.pk, 'sets': ex.sets, 'weight': ex.weight, 'reps': ex.reps} 
            for ex in user_ex
        ]

        formset = ExerciseFormSet(initial=initial_data)
        exercise_forms = list(zip(exercises, formset))

        context = {
                   'user_username': user_username,
                   'wrkt_ids': wrkt_ids,
                   'formset': formset,
                   'exercises': exercises,
                   'exercise_forms': exercise_forms,
                   }
        return render(request, "lzwrkts/suggested_workout.html", context)
    else:
        return render(request, "lzwrkts/index.html")

def save_workout(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    
    if(user.active_session == True):
        if request.method == "POST":
            finished_workout = UserWorkouts.objects.create(user_id = user)
            future_exercises = request.session.get('future_exercises', {})
            ExerciseFormSet = formset_factory(ExerciseForm, extra=len(future_exercises))
            finished_exercises = []
            names = []

            
            formset = ExerciseFormSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    #submitted_pk = str(form.cleaned_data.get('exercise_pk'))
                    # if submitted_pk in future_exercises:
                    # session_ex = future_exercises[submitted_pk]
                    new = UserExercises.objects.create(
                        workout_id = finished_workout,
                        exercise_id=Exercise.objects.get(pk=form.cleaned_data.get('exercise_pk')),
                        weight = form.cleaned_data.get('weight'),
                        reps = form.cleaned_data.get('reps'),
                        sets = form.cleaned_data.get('sets'),
                        liked = form.cleaned_data.get('liked'),
                        )
                    finished_exercises.append(new)
                    names.append(Exercise.objects.get(pk=form.cleaned_data.get('exercise_pk')).name)
                context = {
                   'user_username': user_username,
                   'formset': formset,
                   'exercises': finished_exercises,
                   'names': names
                   }
                return render(request, "lzwrkts/finish_workout.html", context)           
            else:
                return HttpResponseRedirect(reverse("lzwrkts:suggestedwrkt", args=(user.username,)))
    return HttpResponseRedirect(reverse("lzwrkts:suggestedwrkt", args=(user.username,)))

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
        ex_list = Exercise.objects.filter(
                (Q(equipment__in=["barbell", "dumbbell", "kettlebells"]) & 
                Q(primary_muscle__in=Muscles.objects.filter(exercise_group__in=["push", "pull", "legs"]))) | 
                Q(primary_muscle__in=Muscles.objects.filter(name = "abdominals")),
                level = "beginner"
                ).exclude(category="stretching").order_by('name')
        temp = UserExercises.objects.filter(workout_id__user_id=user).order_by('-workout_id__date_completed', '-workout_id__pk')
        u_ex = []
        seen_exercises = set()

        for item in temp:
            if item.exercise_id_id not in seen_exercises:
                u_ex.append(item)
                seen_exercises.add(item.exercise_id_id)

        context = {"ex_list": ex_list,
                        "u_list": u_ex,
                        'user_username': user_username,
                        }
        if request.method == "POST":
            form = SearchForm(request.POST)
            if form.is_valid():
                search = form.cleaned_data["search_term"]
                ex_filter = form.cleaned_data["filter"]
                if search != '':
                    ex_list = ex_list.filter(
                        Q(primary_muscle__in=Muscles.objects.filter(exercise_group__contains=search)) | Q(name__contains=search)
                    )
                if ex_filter != '':
                    for e in ex_filter:
                        if e == 'liked':
                            ex_list = ex_list.filter(userexercises__isnull=False).filter(userexercises__liked=True)
                        else:
                            ex_list= ex_list.filter(primary_muscle__in=Muscles.objects.filter(exercise_group=e))
                context = {"ex_list": ex_list,
                            "u_list": u_ex,
                            'user_username': user_username,
                            }
            #else:
                #TODO: update with a 'we didn't find anything' message

        return render(request, "lzwrkts/search_page.html", context)
    else:
        return render(request, "lzwrkts/index.html")

def workout_history(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        w_list = UserExercises.objects.filter(workout_id__user_id = user).order_by('workout_id__date_completed')
        u_wrkt = UserExercises.objects.filter(workout_id__user_id = user).order_by('workout_id__date_completed')
        context = {"ex_list": w_list,
                        "u_list": u_wrkt,
                        'user_username': user_username,
                        }
        if request.method == "POST":
            form = SearchForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data["start_date"]
                end = form.cleaned_data["end_date"]
                w_filter = form.cleaned_data["filter"]
                if start is not None:
                    w_list = w_list.filter(workout_id__date_completed__gte=start)
                if end is not None:
                    w_list = w_list.filter(workout_id__date_completed__lte=end)
                if w_filter != '':
                    for w in w_filter:
                        if w == 'liked':
                            w_list = w_list.filter(liked=True)
                        else:
                            w_list= w_list.filter(exercise_id__primary_muscle__in=Muscles.objects.filter(exercise_group=w)).exclude(exercise_id__primary_muscle__name='abdominals')
                context = {"ex_list": w_list,
                            "u_list": u_wrkt,
                            'user_username': user_username,
                            }
            #else:
                #TODO: update with a 'we didn't find anything' message

        return render(request, "lzwrkts/workout_history.html", context)
    else:
        return render(request, "lzwrkts/index.html")


def detail(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        # Get the 'msg' parameter from the URL, default to 'Moo!'
        message = request.GET.get('msg', 'WORK IN PROGRESS.')
        
        # Generate the cowsay ASCII art
        cow_art = html.escape(cowsay.get_output_string('cow', message))
        context = {'cow_art': cow_art}
        
        # Return as plain text so the browser preserves the formatting
        return render(request, "lzwrkts/detail.html", context)
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