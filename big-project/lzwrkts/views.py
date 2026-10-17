from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import html
import cowsay

# Create your views here.
def index(request):
    # Get the 'msg' parameter from the URL, default to 'Moo!'
    message = request.GET.get('msg', 'OINK.')
    
    # Generate the cowsay ASCII art
    cow_art = html.escape(cowsay.get_output_string('cow', message))
    context = {'cow_art': cow_art}
    
    # Return as plain text so the browser preserves the formatting
    return render(request, "lzwrkts/temp.html", context)

def health_check(request):
    return HttpResponse("OK", status=200)