from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import re

def index(request):
    return render(request, 'handy/index.html')

def register(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    errors = []
    if len(request.POST["first_name"]) < 1:
        errors.append("You must enter a first name!")
    if len(request.POST["first_name"]) > 1 and not request.POST["first_name"].isalpha():
        errors.append("Your first name must not have numbers!")
    if len(request.POST["last_name"]) < 1:
        errors.append("You must enter a last name!")
    if  len(request.POST["first_name"]) > 1 and not request.POST["last_name"].isalpha():
        errors.append("Your last name must not have numbers!")
    if len(request.POST["email"]) < 1:
        errors.append("You must enter an email!")
    
    if len(request.POST["first_name"]) > 1 and not EMAIL_REGEX.match(request.POST["email"]):
        errors.append("Your email must be an email!")

    if len(request.POST["password"]) < 8:
        errors.append("You must enter a password that is at least 8 characters!")
    if not request.POST["password"] == request.POST["confirm_password"]:
        errors.append("Your password must must match password confirmation!")
    try:
        User.objects.get(email=request.POST["email"])
        messages.error(request, 'Your already registered')
    except:
        fname = request.POST["first_name"]
        lname = request.POST["last_name"]
        em = request.POST["email"]
        password = request.POST["password"]

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            correct_hashed_pw = hashed_pw.decode("utf-8")
            print(hashed_pw)
            print(correct_hashed_pw)
            new_user = User.objects.create(first_name = fname, last_name = lname, email = em, password = correct_hashed_pw)
            request.session['user_id'] = new_user.id
            print(new_user)
    return redirect("/")
    
def login(request):
    errors = []
    if len(request.POST["email"]) < 1:
        errors.append("You must enter an email!")
    if len(request.POST["password"]) < 8:
        errors.append("You must enter a password that is at least 8 characters!")

    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        try:
            user = User.objects.get(email=request.POST["email"])
        except:
            messages.error(request, 'Your email does not exists. Please register.')
            return redirect('/')

        check_pass = bcrypt.checkpw(request.POST["password"].encode(), user.password.encode())
        print(check_pass)
        if check_pass:
            request.session["user_id"] = user.id
        else:
            messages.error(request, 'Email/Password does not match.')

        return redirect('/dashboard')
    return redirect("/")

def dashboard(request):
    values = {
        "user" : User.objects.get(id = request.session["user_id"]),
        "jobs" : Job.objects.all(),
        "my_jobs" : MyJobs.objects.all(),
    }
    return render(request, 'handy/dashboard.html', values)

def log_off(request):
    request.session.clear()
    return redirect("/")

def addJob(request):
    return render(request, 'handy/add_job.html')

def back(request):
    return redirect("/dashboard")

def add_new_job(request):
    errors = []
    if len(request.POST["title"]) < 3:
        errors.append("Your title must be greater than three characters!")
    if len(request.POST["description"]) < 10:
        errors.append("Your description must be greater than ten characters!")
    if len(request.POST["location"]) < 1:
        errors.append("You must include a location!")

    user = User.objects.get(id = request.session["user_id"])
    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        Job.objects.create(title = request.POST["title"], description = request.POST["description"], location = request.POST["location"], user = user)
        return redirect("/dashboard")
    return redirect("/addJob")

def view(request, job_id):
    values = {
        "job" : Job.objects.get(id = job_id)
    }
    return render(request, 'handy/view_job.html', values)

def add_to_my_jobs(request, job_id):
    title = Job.objects.get(id = job_id).title
    description = Job.objects.get(id = job_id).description
    location = Job.objects.get(id = job_id).location
    # user = User.objects.get(id = request.session["user_id"])
    user = Job.objects.get(id = job_id).user

    MyJobs.objects.create(title = title, description = description, location = location, user = user)
    Job.objects.get(id = job_id).delete()
    return redirect("/dashboard")

def edit(request, job_id):
    values = {
        "job" : Job.objects.get(id = job_id)
    }
    return render(request, 'handy/edit_job.html', values)

def delete_job(request, job_id):
    Job.objects.get(id = job_id).delete()
    return redirect("/dashboard")

def delete_myjob(request, job_id):
    MyJobs.objects.get(id = job_id).delete()
    return redirect("/dashboard")

def update_job(request, job_id):
    errors = []
    if len(request.POST["title"]) < 3:
        errors.append("Your title must be greater than three characters!")
    if len(request.POST["description"]) < 10:
        errors.append("Your description must be greater than ten characters!")
    if len(request.POST["location"]) < 1:
        errors.append("You must include a location!")

    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        j = Job.objects.get(id = job_id)
        j.title = request.POST["title"]
        j.description = request.POST["description"]
        j.location = request.POST["location"]
        j.save()
        return redirect("/dashboard")
    return redirect("/edit/{}".format(job_id))