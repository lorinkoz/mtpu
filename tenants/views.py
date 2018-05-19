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
        return self.request.GET.get('next', reverse('status'))

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
    form_class = user_forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'tenants/signup.html'
    
    def form_valid(self, form):
        from random import Random
        r = Random()
        mode = self.kwargs['mode']
        if mode == 'primary':
            user = models.PrimaryStaffUser(
                login=form.cleaned_data['login'],
                display_name=form.cleaned_data['display_name'],
                rank=r.choice(range(1, 10)),
            )
            user.save()
            user.team.set(models.SupportStaffUser.objects.order_by('?')[:3])
        elif mode == 'support':
            user = models.SupportStaffUser(
                login=form.cleaned_data['login'],
                display_name=form.cleaned_data['display_name'],
                role=r.choice([1, 2, 3, 4]),
            )
        else:
            user = models.RegisteredUser(
                login=form.cleaned_data['login'],
                display_name=form.cleaned_data['display_name'],
            )
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs.update({'mode': self.kwargs['mode']})
        return super().get_context_data(**kwargs)


class StatusPage(LoginRequiredMixin, TemplateView):
    template_name = 'tenants/status.html'
    
    def get_context_data(self, **kwargs):
        kwargs.update({'type': self.request.user._meta.verbose_name})
        if isinstance(self.request.user, models.StaffUser):
            kwargs.update({'registered': models.RegisteredUser.objects.all()})
        if isinstance(self.request.user, models.PrimaryStaffUser):
            kwargs.update({'staff': models.StaffUser.objects.all()})
        return super().get_context_data(**kwargs)