from .models import Customer
from django.forms import ModelForm
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['created_by_user', 'last_modified_by_user']