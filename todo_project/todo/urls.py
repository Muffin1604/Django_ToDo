from django.urls import path
from .views import register, login_view, logout_view
from .views import task_list, task_detail, create_task, update_task, delete_task

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('task/', task_list, name='task-list'),
    path('task/<int:pk>/', task_detail, name='task-detail'),
    path('task/new/', create_task, name='task-create'),
    path('task/<int:pk>/edit/', update_task, name='task-update'),
    path('task/<int:pk>/delete/', delete_task, name='task-delete'),
]
