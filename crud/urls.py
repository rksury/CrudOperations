from os import name

from django.urls import path
from . import views

urlpatterns = [
    path('crud/', views.UserView, name='crud operations'),
    # path('create/', views.post),
    # path('read/', views.get),
    # path('update/', views.put),
    # path('delete/', views.delete)

]