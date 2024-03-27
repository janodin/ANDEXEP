from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('show_record', show_record, name='show_record'),
    ]
