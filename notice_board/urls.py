from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'notice_board'
urlpatterns = [
    path('', NoticeLists.as_view(), name='allAds'),
    path('check_email/', EmailCheckView.as_view(), name='checkEmail'),
    path('<int:pk>/', AdDetail.as_view(), name='detailAd'),
    path('create_ad/', AdCreate.as_view(), name='createAd'),
    path('<int:pk>/edit/', AdUpdate.as_view(), name='adUpdate'),
    path('<int:pk>/delete/', AdDelete.as_view(), name='adDelete'),
    path('<int:pk>/send_reply/', ReplyCreate.as_view(), name='replySend'),
    path('replyes/', ReplyList.as_view(), name='allReplyes')
]