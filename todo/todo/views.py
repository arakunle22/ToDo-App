from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from todo import models
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import TODOO  # Assuming your model is imported from the current app


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')

        # Create the user
        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.save()
        return redirect('/login')

    return render(request, 'signup.html')

def user_login(request):  # Renamed from `login` to `user_login`
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        # Authenticate user
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            auth_login(request, user)  # Use `auth_login` from `django.contrib.auth`
            return redirect('/todopage')
        else:
            return redirect('/login')

    return render(request, 'login.html')


@login_required(login_url='/loginn')
def todopage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            # Create a new task for the logged-in user
            obj = TODOO(title=title, user=request.user)
            obj.save()
        # Use the named URL 'todopage' instead of hardcoding
        return redirect('todopage')  # Redirect after adding the task to prevent resubmission

    # Retrieve the tasks for the current logged-in user, ordered by date (latest first)
    tasks = TODOO.objects.filter(user=request.user).order_by('-date')

    return render(request, 'todo.html', {'tasks': tasks})

@login_required(login_url='/loginn')
def edit_todo(request, srno):
    # Safely get the TODOO object or return 404 if it doesn't exist
    obj = get_object_or_404(models.TODOO, srno=srno)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:  # Ensure title is not None or empty
            obj.title = title
            obj.save()  # Save the updated object
            return redirect(reverse('todopage'))  # Redirect using named URL 'todopage'
    
    # Render the edit_todo template with the object to edit
    return render(request, 'edit_todo.html', {'obj': obj})

def delete_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('todopage')


def logout(request):
    auth_logout(request)  # Logs the user out
    return redirect('/login')  # Redirect to the login page after logout