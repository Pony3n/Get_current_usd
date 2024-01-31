from django.urls import path

from .views import get_current_usd


urlpatterns = [
    path('', get_current_usd, name="get_current_usd"),
]