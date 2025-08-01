from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.view.as_view(get_active=True), name='acttive'),
    path('index', views.index.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('users', views.userlist.as_view(), name='userindex'),
    path('new', views.new.as_view(), name='new'),
    path('interface', views.interface.as_view(), name='interface_active'),
    path('interface/<int:pk>', views.interface.as_view(), name='interface'),
    path('view/<int:pk>', views.view.as_view(), name='view'),
    path('edit/<int:pk>', views.edit.as_view(), name='edit'),

    path('api/marbar/<int:marbar_id>', views.marbar, name='marbar_updates'),

    path('consumers', views.consumer_index.as_view(), name='consumer_index'),
    path('consumers/new', views.consumer_new.as_view(), name='consumer_new'),
]
