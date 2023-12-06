from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('project1/', views.project1, name="project1-dengue"),
    path('project2/', views.project2, name="project2-pizza"),
    path('project3/', views.project3, name="project3-family"),
]