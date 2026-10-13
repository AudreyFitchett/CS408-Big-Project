from django.shortcuts import render
from django.http import HttpResponse
import cowsay

# Create your views here.
def index(request):
    message = request.GET.get('msg', 'Oink.')
    
    cow_art = cowsay.get_output_string('cow', message)
    
    return HttpResponse(cow_art, content_type="text/plain; charset=utf-8")