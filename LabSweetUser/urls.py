from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('submitsample', views.submit_sample, name='submitsample'),
    path('samples', views.get_samples, name='samples'),
    path('samples/<str:pk>/', views.get_sample, name='sample'),
    path('jobs', views.get_jobs, name='jobs'),
    path('jobs/<str:job_number>/', views.get_job, name='job'),
    path('worklists', views.get_worklists, name='worklists'),
    path('generate/<str:attribute>', views.generate_worklist, name='generate_worklist'),
    path('outstanding', views.outstanding_work_view, name='outstanding'),
    path('download_worklist/<str:worklist_number>', views.download_worklist, name='download_worklist'),
    path('staff', views.staff_view, name='staff'),
    path('upload_results', views.upload_results, name='upload_results'),
    ]
