from .models import Customer
from django.forms import ModelForm
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['referenced_user']