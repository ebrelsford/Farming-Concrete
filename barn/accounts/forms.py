from django.contrib.auth.models import User
from django.forms import EmailField, ModelForm


class UserForm(ModelForm):
    # Require email
    email = EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
