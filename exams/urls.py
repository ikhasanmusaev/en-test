from django.urls import path

from . import views

urlpatterns = [
    path('tests', views.test_list, name='test-list'),
    path('listening-list', views.listening_list, name='listening-list'),
    path('listening/<int:pk>', views.listening_detail, name='listening-detail'),
    path('test/<int:pk>', views.test_detail, name='test-detail'),
]
