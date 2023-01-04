from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.run),
    path('regester', views.regester),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),


    path('wall', views.wall),
    path('post', views.post),
    path('comment', views.comment),
    path('dell', views.dell),
    path('dell_post', views.dell_post),
    

    
    
    
]
