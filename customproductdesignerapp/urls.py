from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name=''),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('forget_link',views.forget_link,name='forget_link'),
    path('new_pass',views.new_pass,name='new_pass'),
    path('redirectt',views.redirectt,name='redirectt'),
     
    

]
