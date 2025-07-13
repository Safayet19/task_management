from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test, create_task,view_task

urlpatterns = [
  path('manager_dashboard/',manager_dashboard),
  path('user_dashboard/',user_dashboard),
  path('test/',test),
  path('task_form/', create_task),
  path('view-task/', view_task)
]