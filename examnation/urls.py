from django.urls import path
from . import views
from .views import register_view
from .views import test_view
from .views import result_view
from .views import add_question_view

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('test/<str:course_name>/', views.test_view, name='take_test'),
    path('result/', views.result_view, name='result'),
    path("add-question/", views.add_question_view, name="admin_add_question"),

    ]