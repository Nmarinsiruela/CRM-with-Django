from django.contrib.auth.models import User
from django.forms import ModelForm
class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'is_staff')

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'is_staff')