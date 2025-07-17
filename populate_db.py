import os
import django
import uuid
import random
from faker import Faker

# ✅ Set up Django environment before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

# ✅ Import models AFTER setting up Django
from tasks.models import Employee, Project, Task, TaskDetail

def populate_db():
    fake = Faker()

    # Create Projects
    projects = []
    for _ in range(5):
        project = Project.objects.create(
            name=fake.bs().capitalize(),
            description=fake.paragraph(),
            start_date=fake.date_this_year()
        )
        projects.append(project)
    print(f"✅ Created {len(projects)} projects.")

    # Create Employees
    employees = []
    for _ in range(10):
        employee = Employee.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        employees.append(employee)
    print(f"✅ Created {len(employees)} employees.")

    # Create Tasks and assign Employees
    tasks = []
    for _ in range(50):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.sentence(nb_words=6),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            is_completed=random.choice([True, False])
        )
        assigned_emps = random.sample(employees, random.randint(1, 3))
        task.assigned_to.set(assigned_emps)
        task.save()
        tasks.append(task)
    print(f"✅ Created {len(tasks)} tasks.")

    # Create TaskDetails with unique std_id
    for task in tasks:
        assigned_names = ", ".join([emp.name for emp in task.assigned_to.all()])
        TaskDetail.objects.create(
            std_id=str(uuid.uuid4()),
            task=task,
            assigned_to=assigned_names,
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )
    print("✅ Populated TaskDetails for all tasks.")
    print("🎉 Database populated successfully!")

# ✅ Run if this script is executed directly
if __name__ == "__main__":
    populate_db()
