from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    
    STATUS_COICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    # ------Many to One Relationship-------------
    project = models.ForeignKey("Project",
                                on_delete=models.CASCADE,
                                default=1)
    
    # ------Many to Many Relationship-------------
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_COICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDUIM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDUIM, 'Medium'),
        (LOW, 'Low')
    )
    std_id = models.CharField(max_length=200,primary_key=True)
    # Making Relation
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Details form Task = {self.task.title}"

# -----ORM = Object Relational Mapping----
# Task.objects.get(id = 1) but in sql select * from task where id = 1

# ------Many to One Relationship-------------

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True, null= True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name
    
    