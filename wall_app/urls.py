from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('process_message', views.process_message),
    path('process_comment', views.process_comment),
    path('log_out', views.log_out),
    path('delete_message/<message_id>', views.delete_message),
]