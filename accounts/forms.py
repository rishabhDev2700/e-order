from django.contrib.auth.forms import UserCreationForm as CreationForm

from accounts.models import User


class UserCreationForm(CreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
