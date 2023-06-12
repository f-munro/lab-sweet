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
    path('tests', views.getTests, name='tests'),
    path('tests/<str:pk>/', views.getTest, name='test'),
    path('jobs', views.getJobs, name='jobs'),
    path('jobs/<str:pk>/', views.getJob, name='job'),
    ]
