from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
import html
import cowsay
from .models import User, LoginForm
from .forms import UserForm

# Create your views here.
def index(request): 
    # Return as plain text so the browser preserves the formatting
    return render(request, "lzwrkts/index.html")

def home(request, user_username):
    user = get_object_or_404(User, pk=user_username)
    if(user.active_session == True):
        # Get the 'msg' parameter from the URL, default to 'Moo!'
        message = request.GET.get('msg', 'WORK IN PROGRESS.')
        
        # Generate the cowsay ASCII art
        cow_art = html.escape(cowsay.get_output_string('cow', message))
        context = {'cow_art': cow_art}
        
        # Return as plain text so the browser preserves the formatting
        return render(request, "lzwrkts/temp.html", context)
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