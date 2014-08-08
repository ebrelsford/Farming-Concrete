from django.contrib.auth.models import User
from django.forms import (EmailField, Form, HiddenInput, ModelChoiceField,
                          ModelForm)

from farmingconcrete.models import Garden


class UserForm(ModelForm):
    # Require email
    email = EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


class InviteForm(Form):
    email = EmailField()
    garden = ModelChoiceField(
        queryset=Garden.objects.all(),
        widget=HiddenInput(),
    )
