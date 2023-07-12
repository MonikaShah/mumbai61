from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .models import student, LoginUsers, TaskStudent, tasks_zerowaste
from zerowaste.models import AuthUser
from .forms import TaskForm, RegisterForm
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
import json
from datetime import datetime
from django.db.models import Count


# Create your views here.

def home(request):
    usernames = tasks_zerowaste.objects.values_list('zerowaste_user__username', flat=True).distinct()
    return render(request, 'home/home.html', {'usernames': usernames})

def tasks_by_username(request, username):
    
    tasks = tasks_zerowaste.objects.filter(zerowaste_user__username=username).values()
    
    
    return JsonResponse(list(tasks), safe=False)


# def get_tasks(request):
#     tasks = TaskStudent.objects.all()
#     task_list = []
#     for task in tasks:
#         task_data = {
#             'id': task.id,
#             'task_name': task.task_name,
#             'task_start_date': task.task_start_date,
#             'task_status': task.task_status,
#             'task_completion_date': task.task_completion_date,
#             'username': task.username.username  # Access the username field of the related student object
#         }
#         task_list.append(task_data)
#     return JsonResponse(json.dumps(task_list), safe=False)


def update_status(request, task_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        task = get_object_or_404(tasks_zerowaste, id=task_id)

        # Update the task status
        task.task_status = new_status

        # Save the completion date if it exists in the form data
        completion_date = request.POST.get('completion_date')
        if completion_date:
            task.task_completion_date = completion_date

        # Save the updated task
        task.save()

        messages.success(request, 'Status updated successfully!')

        # Construct the JSON response
        response_data = {
            'status': task.task_status,
        }
        return JsonResponse(response_data)

    return HttpResponseBadRequest('Invalid request method')

    return redirect('home')

def delete_task(request, task_id):
    task = get_object_or_404(tasks_zerowaste, id=task_id)
    task.delete()
    return HttpResponse(status=200)


# @login_required(login_url='home')
def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User credentials are valid
            login(request, user)
            return redirect('home')  
        else:
            # User credentials are invalid
            error_message = "Invalid username or password"
            return render(request, 'home/login.html', {'error_message': error_message})
    return render(request,'home/login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def tasks(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_start_date = request.POST.get('task_start_date')
        username = request.POST.get('username')

        # Check if task_start_date is valid and convert it to date object
        if task_start_date:
            try:
                task_start_date = datetime.strptime(task_start_date, '%Y-%m-%d').date()
            except ValueError:
                task_start_date = None

        user = AuthUser.objects.get(username=username)

        tasks_zerowaste.objects.create(
            task_name=task_name,
            task_start_date=task_start_date,
            zerowaste_user=user,
            username=username,
            task_status='0%'
        )

        messages.success(request, 'Task Added Successfully')  # Add success message

        # Add any additional logic or redirection after saving the task

    usernames = AuthUser.objects.values_list('username', flat=True)
    return render(request, 'home/tasks.html', {'usernames': usernames})
def get_student_name():
    # Retrieve the student name from the student_data table, assuming you have a specific student in mind
    # Modify this logic based on how you want to retrieve the student name
    student_obj = student.objects.get(id=1)  # Example: Retrieving the student with id=1
    return student_obj.name

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if student.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'home/register.html')
        else:
            # Create a new student object
            new_student = student(name=name, username=username, password=password)
            
            # Save the student object to the database
            new_student.save()
        
        # Redirect to a success page or any other desired page
        return redirect('user_login')
    
    return render(request, 'home/register.html')

@login_required
def graph(request):
    usernames = tasks_zerowaste.objects.values_list('username', flat=True).distinct()
    selected_username = request.GET.get('username', '')
    return render(request, 'home/graph.html', {'usernames': usernames, 'selected_username': selected_username})

def get_tasks(request, username):
    selected_username = request.GET.get('username')
    tasks = tasks_zerowaste.objects.filter(zerowaste_user__username=username).order_by('id').values('task_name', 'task_status')
    
    return JsonResponse({'tasks': list(tasks)})

@login_required
def graph2(request):
    task_data = tasks_zerowaste.objects.values('task_name', 'task_status').annotate(task_count=Count('id'))

    # Prepare the data for the chart
    labels = [task['task_name'] for task in task_data]
    status_percentages = [float(task['task_status'].strip('%')) for task in task_data]

    # Fetch task names and usernames
    task_names = tasks_zerowaste.objects.values_list('task_name', flat=True).distinct()
    usernames = tasks_zerowaste.objects.values_list('username', flat=True).distinct()

    # Pass the data, task names, and usernames to the template
    context = {
        'labels': labels,
        'status_percentages': status_percentages,
        'task_names': task_names,
        'usernames': usernames,
    }
    return render(request, 'home/graph2.html', context)


