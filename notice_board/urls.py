from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'notice_board'
urlpatterns = [
    path('', NoticeLists.as_view(), name='allAds'),
]