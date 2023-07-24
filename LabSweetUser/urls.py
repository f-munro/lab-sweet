from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('submitsample', views.submit_sample, name='submitsample'),
    path('samples', views.getSamples, name='samples'),
    path('samples/<str:pk>/', views.getSample, name='sample'),
    path('jobs', views.getJobs, name='jobs'),
    path('jobs/<str:job_number>/', views.getJob, name='job'),
    ]
