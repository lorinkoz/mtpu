from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('tenants/', views.TenantList.as_view(), name='tenants'),
    
    path('login/', views.LogInPage.as_view(), name='login'),
    path('logout/', views.LogOutPage.as_view(), name='logout'),
    path('signup/', views.SignUpPage.as_view(), name='signup'),
]
