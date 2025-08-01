from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404

from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import *
from datetime import date
from django.db.models import Q, Count


# Create your views here.
def manager_dashboard(request):
    
    type = request.GET.get('type','all')
    
    #Total task count
    # tasks = Task.objects.select_related('taskdetail').prefetch_related('assigned_to').all()
    
    # """Too Much Time Complexity"""
    """
    task_count = tasks.count()
    completed_task = Task.objects.filter(status = "COMPLETED").count()
    in_progress_task = Task.objects.filter(status = "IN_PROGRESS").count()
    pending_task = Task.objects.filter(status = "PENDING").count()
    
     context = {
        'task_count': task_count,
        'completed_task': completed_task,
        'in_progress_task': in_progress_task,
        'pending_task': pending_task,
    }
    """
    
    #Filtering Specific
    base_query = Task.objects.select_related('taskdetail').prefetch_related('assigned_to')
    
    if type == 'completed': 
        tasks = base_query.filter(status = 'COMPLETED')
    elif type == 'in_progress': 
        tasks = base_query.filter(status = 'IN_PROGRESS')
    elif type == 'pending': 
        tasks = base_query.filter(status = 'PENDING')
    else : 
        tasks = base_query.all()
    
     
    # Use a single aggregate call for all status counts
    status_counts = Task.objects.aggregate(
    task_count=Count('id'),
    completed_task=Count('id', filter=Q(status="COMPLETED")),
    in_progress_task=Count('id', filter=Q(status="IN_PROGRESS")),
    pending_task=Count('id', filter=Q(status="PENDING")),
)

    context = {
        "tasks": tasks,
        **status_counts  # Unpack the dictionary so you get keys: task_count, completed_task, etc.
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
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"Task Created Successfully")
            return redirect('create-task')
        
    context = {"task_form": task_form, "task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    try:
        task_detail = TaskDetail.objects.get(task=task)
    except TaskDetail.DoesNotExist:
        task_detail = None

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task_detail)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task updated successfully!")
            return redirect('manager-dashboard')  # or wherever you want to redirect
    else:
        task_form = TaskModelForm(instance=task)
        task_detail_form = TaskDetailModelForm(instance=task_detail)
    
    context = {
        "task_form": task_form,
        "task_detail_form": task_detail_form,
        "task": task,
    }
    return render(request, "task_form.html", context)



def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('manager-dashboard') 


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
