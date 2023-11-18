from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from account.models import User
from .models import Task
from .forms import TaskForm

@login_required
def task_create(request):
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('evaluation:task_list')
    else:
        employees = User.objects.filter(is_superuser=False, is_staff=False)

        if request.method == 'GET' and 'assigned_to' in request.GET:
            assigned_to = request.GET['assigned_to']
            if assigned_to is not None and assigned_to != '':
                form = TaskForm(initial={'assigned_to': request.GET['assigned_to']})
            else:
                form = TaskForm()
        else:
            form = TaskForm()
    return render(request, 'evaluation/task_create.html', {'form': form, 'employees': employees})


def task_list(request):
    all_tasks = None
    if request.user.is_superuser:
        all_tasks = Task.objects.all()
    # else:
    #     all_tasks = Task.objects.filter(assigned_to=request.user.id)
    return render(request, 'evaluation/task_list.html', {'all_tasks': all_tasks})


def my_tasks(request):
    all_tasks = Task.objects.filter(assigned_to=request.user.id)
    return render(request, 'evaluation/mytask.html', {'all_tasks': all_tasks})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.update_status() 
    print(f"user: {request.user}, task_assigned_to: {task.assigned_to}")
    return render(request, 'evaluation/task_detail.html', {'task': task})


def update_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
            
        return redirect('evaluation:task_detail', task_id=task_id)

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    task.delete()
    return redirect('evaluation:task_list')