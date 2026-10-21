from django.shortcuts import render
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

def home(request):
    # Get the 'msg' parameter from the URL, default to 'Moo!'
    message = request.GET.get('msg', 'WORK IN PROGRESS.')
    
    # Generate the cowsay ASCII art
    cow_art = html.escape(cowsay.get_output_string('cow', message))
    context = {'cow_art': cow_art}
    
    # Return as plain text so the browser preserves the formatting
    return render(request, "lzwrkts/temp.html", context)

def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                real_user = User.objects.get(username = name)
                if(real_user.password == password):
                    return HttpResponseRedirect(reverse("lzwrkts:home"))
                else: 
                    return HttpResponse("Not Cool Beans: wrong password")
            except User.DoesNotExist: 
                return HttpResponse("Not Cool Beans: username dne")
        else:
            print(form.errors)
            return HttpResponse("Not Cool Beans: something ain't right")
    else:
        form = UserForm()
    return render(request, "lzwrkts/index.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid(): 
            try:
                form.save()
                return HttpResponse("cool beans")
            except User.DoesNotExist: 
                return HttpResponse("Not Cool Beans: username dne")
        else:
            print(form.errors)
            return HttpResponse("Not Cool Beans: something ain't right")
    else:
        form = UserForm()
    return render(request, "lzwrkts/index.html", {"form": form})

    # try: 
    #     user = request.GET["username"]
    #     pwd = request.GET["password"]
        


    # except(KeyError):
    #    return render(
    #         request,
    #         "polls/index.html",
    #         {
    #             "error_message": "Please enter a username/password",
    #         },
    #     )
    # else: 
    #     if(not user.exists()):
    #         return render(
    #             request,
    #             "lzwrkts/index.html",
    #             {
    #                 "error_message": "User does not exist",
    #             },
    #         )
    #     elif(user.first().password != pwd):
    #         return render(
    #             request,
    #             "lzwrkts/index.html",
    #             {
    #                 "error_message": "Incorrect password",
    #             },
    #         )
    #     else:
    #         return HttpResponse("Cool Beans")

def health_check(request):
    return HttpResponse("OK", status=200)