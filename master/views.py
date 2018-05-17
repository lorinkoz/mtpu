from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, FormView, ListView, DeleteView

from . import models, forms
from users import forms as user_forms


class HomePage(FormView):
    form_class = forms.TenantForm
    success_url = reverse_lazy('home')
    template_name = 'master/home.html'
    
    def form_valid(self, form):
        subdomain = form.cleaned_data['subdomain']
        schema_name = 'tn_{}'.format(subdomain.replace('-', '_'))
        domain = '{}{}'.format(subdomain, settings.ALLOWED_HOSTS[0])
        if models.Tenant.objects.filter(schema_name=schema_name).exists() or\
            models.Domain.objects.filter(domain=domain).exists():
            form.add_error(None, 'Hmm, there is another subdomain very similar and we cannot let you take it.')
            return super().form_invalid(form)
        tenant = models.Tenant(schema_name=schema_name)
        tenant.save()
        tenant_domain = models.Domain(domain=domain, tenant=tenant)
        tenant_domain.save()
        return redirect('//{}'.format(domain))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'subdomain': settings.ALLOWED_HOSTS[0],
        })
        return context
    

class LogInPage(FormView):
    form_class = user_forms.LoginForm
    template_name = 'master/login.html'
    
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


class SignUpPage(FormView):
    form_class = user_forms.SignUpForm
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


class TenantList(LoginRequiredMixin, ListView):
    queryset = models.Tenant.objects.exclude(schema_name='public')
    template_name = 'master/tenant_list.html'