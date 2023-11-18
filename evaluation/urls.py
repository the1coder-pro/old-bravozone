from django.urls import path
from evaluation import views


app_name = "evaluation"

urlpatterns = [
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.task_create, name="task_create"),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('mytask', views.my_tasks, name='my_task_list')
]
