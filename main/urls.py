from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('leaderboard/', views.leader_bord, name='leader_bord'),

]
