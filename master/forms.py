from django import forms


class TenantForm(forms.Form):
    
    subdomain = forms.SlugField(required=True)