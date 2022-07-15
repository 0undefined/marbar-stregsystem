from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index.as_view(), name='index'),
    path('new', views.new.as_view(), name='new'),
    path('interface', views.interface.as_view(), name='interface'),
]
