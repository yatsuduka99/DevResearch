from django.urls import path
from app.schedule_check import views

app_name = 'schedule_check'
urlpatterns = [
    path('', views.index, name='index'),
]
