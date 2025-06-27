from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
        return HttpResponse("Welcome to the task management System")

def contact(request):
    return HttpResponse("This is Contact Page")

def show_task(request):
    return HttpResponse("This is our task page")
    
