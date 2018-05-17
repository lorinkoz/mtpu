from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('login/', views.LogInPage.as_view(), name='login'),
    path('logout/', views.LogOutPage.as_view(), name='logout'),
    # re_path('signup/(outsider|primary|support)/', views.SignUpPage.as_view(), name='signup'),
]
