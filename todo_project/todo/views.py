from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm,TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

#Function to register the user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('task-list')
    else:
        form = UserRegisterForm()
    return render(request, 'todo/register.html', {'form': form})

#function for login page view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task-list')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})

#function for logout page
def logout_view(request):
    logout(request)
    return redirect('login')

# list of the tasks for a particular logged in user
@login_required
def task_list(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(user=request.user).filter(title__icontains=query)
    else:
        tasks = Task.objects.filter(user=request.user)

    pending_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)
    return render(request, 'todo/task_list.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks
    })
#functions for the CRUD opertaion
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'todo/task_detail.html', {'task': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task-list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})
