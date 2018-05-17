from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, FormView, ListView, DeleteView

from . import models
from users import forms as user_forms


class HomePage(TemplateView):
    template_name = 'tenants/home.html'
    

class LogInPage(FormView):
    form_class = user_forms.LoginForm
    template_name = 'tenants/login.html'
    
    def get_success_url(self):
        return self.request.GET.get('next', reverse('tenants'))

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogOutPage(View):
    
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        next = request.POST.get('next', reverse('home'))
        return redirect(next)
