from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^log_off$', views.log_off),
    url(r'^addJob$', views.addJob),
    url(r'^back$', views.back),
    url(r'^add_new_job$', views.add_new_job),
    url(r'^view/(?P<job_id>\d+)$', views.view),
    url(r'^add_to_my_jobs/(?P<job_id>\d+)$', views.add_to_my_jobs),
    url(r'^delete_job/(?P<job_id>\d+)$', views.delete_job),
    url(r'^delete_myjob/(?P<job_id>\d+)$', views.delete_myjob),
    url(r'^edit/(?P<job_id>\d+)$', views.edit),
    url(r'^update_job/(?P<job_id>\d+)$', views.update_job),
    
]