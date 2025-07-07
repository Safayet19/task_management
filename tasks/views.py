from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "names" : ["Safayet", "Mirza", "OKOL"],
        "age" : 23
    }
    return render(request,'test.html',context)