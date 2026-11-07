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
    path("<str:user_username>/workout_generator/", views.workout_generator, name="wrktgen"),
    path("<str:user_username>/suggested_workout/", views.suggested_workout, name="suggestedwrkt"),
    path("<str:user_username>/finish_workout/", views.save_workout, name="finishedwrkt"),
    path("<str:user_username>/detail/", views.detail, name="detail"),
]