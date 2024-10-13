from django.urls import path
from . import views

urlpatterns = [
    path('words/', views.words, name="word"),
]