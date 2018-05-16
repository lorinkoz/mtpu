from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, FormView, ListView, DeleteView

from . import models
from users import forms


class HomePage(TemplateView):
    template_name = 'master/home.html'


class LogInPage(FormView):
    form_class = forms.LoginForm
    template_name = 'master/login.html'
    
    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogOutPage(View):
    
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        next = request.POST.get('next', reverse('home'))
        return redirect(next)


class SignUpPage(FormView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'master/signup.html'
    
    def form_valid(self, form):
        mu = models.MasterUser(
            login=form.cleaned_data['login'],
            display_name=form.cleaned_data['display_name'],
        )
        mu.set_password(form.cleaned_data['password1'])
        mu.save()
        return super().form_valid(form)


class TenantList(ListView):
    model = models.Tenant
    template_name = 'master/tenant_list.html'