from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dash', views.dash),
    
    # PROCESS
    path('loginUser', views.loginUser),
    path('regUser', views.regUser),

    # SEARCH
    path('search/forFirstName', views.findByFirstName)


]