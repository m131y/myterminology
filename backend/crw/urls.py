from django.urls import path
from . import views
from django.contrib.auth import login, logout
from .views import process_login,process_news,process_signup,result,process_logout,test
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('crw/', views.index, name="index"),
    #path('result/', views.result, name="result"),
    #path('signup/',views.signup, name="signup"),
    #path('userpage/',views.userpage, name='userpage'),
    
    path('', views.home, name='index'),
    path('usertest/', TemplateView.as_view(template_name='usertest.html'), name='usertest'),
    path('news/', TemplateView.as_view(template_name='news.html'), name='news'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', auth_views.LoginView.as_view(template_name='signup.html'), name='signup'),
    path('process-login/', process_login, name='process_login'),
    path('process-logout/', process_logout, name='process_logout'),
    path('process-news/', process_news, name='process_news'),
    path('process-signup/', process_signup, name='process_signup'),
    path('result/',result, name='result'),
    path('test/',test,name='test'),
]