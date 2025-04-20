from django.urls import path
from .views import health, recommend

urlpatterns = [
    path('health', health, name='health'),
    path('recommend', recommend, name='recommend'),
]

