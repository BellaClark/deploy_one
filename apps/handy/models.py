from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Job(models.Model):
    user = models.ForeignKey(User, related_name = "users_job", on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    location = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class MyJobs(models.Model):
    user = models.ForeignKey(User, related_name = "users_myjob", on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    location = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
