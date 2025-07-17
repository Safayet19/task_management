from django.http import HttpResponse
from django.shortcuts import render

from tasks.forms import TaskForm, TaskModelForm
from tasks.models import *
from datetime import date
from django.db.models import Q, Count


# Create your views here.
def manager_dashboard(request):
    
    #Total task count
    tasks = Task.objects.all()
    
    task_count = tasks.count()
    completed_task = Task.objects.filter(status = "COMPLETED").count()
    in_progress_task = Task.objects.filter(status = "IN_PROGRESS").count()
    pending_task = Task.objects.filter(status = "PENDING").count()
    
    context = {
        "tasks" : tasks,
        "task_count" : task_count,
        "completed_task" : completed_task,
        "in_progress_task" : in_progress_task,
        "pending_task" : pending_task 
    }
    
    return render(request, "dashboard/manager_dashboard.html", context)

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

def view_task(request):
   #filter data of pending task
   #pending_tasks = Task.objects.filter(status = "PENDING")
   
   #show task of due_date today
   #tasks = Task.objects.filter(due_date = date.today())
   
   """ Show The Task Whose Priority is not LOW"""
   #tasks = TaskDetail.objects.exclude(priority = 'L')
   
   """ Show The Task contain word paper .. ',' mane and. Q mane OR """
   #tasks = Task.objects.filter(Q(title__icontains = 'c') | Q(status = 'PENDING'))
   
   """ select related query (Foreign Key, OneToOneField)"""
   #tasks = Task.objects.all() # eta dile onkbar query chole.Optimized hoyna. 21bar query chole.. tai select related query use
   # tasks = Task.objects.select_related('taskdetail').all()
   
   """ Foreign key er upor select_related query """
   #asks = Task.objects.select_related('project').all()
   
   """ prefetch_related (reverse ForeignKey , manytomany )"""
   #tasks = Project.objects.prefetch_related('task_set').all()
   
   """Count how many TaskDetail records each Task has (annotate)"""
  #tasks = Task.objects.annotate(detail_count=Count('taskdetail'))
  
   """ Aggregation """
   tasks = Task.objects.aggregate(total=Count('id'))
   return render(request, "show_task.html", {'tasks' : tasks})
