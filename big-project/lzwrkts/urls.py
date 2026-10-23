from django.urls import path

from . import views

app_name = "lzwrkts"
urlpatterns = [
    path("", views.index, name="index"),
    path('api/health', views.health_check),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("<str:user_username>/home/", views.home, name="home"),
    path("<str:user_username>/new_workout/", views.new_workout, name="newwrkt"),
    path("<str:user_username>/search/", views.search_exercises, name="search"),
    path("<str:user_username>/workout_history/", views.workout_history, name="history"),
]