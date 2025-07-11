from django.http import HttpResponse
from django.shortcuts import render

from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task


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

# def create_task(request):
#     employees = Employee.objects.all()
#     form = TaskForm(employees = employees)
    
#     #jkhn form submit hobe tkhn database a save korar jonno
#     if request.method == "POST":
#         form = TaskForm(request.POST, employees=employees)
#         if form.is_valid():
#             data = form.cleaned_data
#             title = data.get('title')
#             description = data.get('description')
#             due_date = data.get('due_date')
#             assigned_to = data.get('assigned_to')  # should be a list of employee IDs

#             # Create the task
#             task = Task.objects.create(
#                 title=title,
#                 description=description,
#                 due_date=due_date
#             )

#             # Assign employees to task (assuming many-to-many relationship)
#             for emp_id in assigned_to:
#                 employee = Employee.objects.get(id=emp_id)
#                 task.assigned_to.add(employee)
        
#     context = {
#         "form": form
#     }
#     return render(request, "task_form.html",context)


def create_task(request):
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'task_form.html', {"form": form, "message": "Task Added Successfully"})
    else:
        form = TaskModelForm()

    context = {"form": form}
    return render(request, "task_form.html", context)
