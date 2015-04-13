from django.contrib.auth.models import User
from django.forms import (EmailField, Form, HiddenInput,  ModelChoiceField,
                          ModelForm, ValidationError)

from farmingconcrete.models import Garden
from generic.forms import GroupedModelMultipleChoiceField
from .models import GardenMembership


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


class GroupedGardenMembershipMultipleChoiceField(GroupedModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return str(obj.user_profile.user)


class AddGardenGroupAdminForm(Form):
    users = GroupedGardenMembershipMultipleChoiceField(
        group_by_field='garden',
        queryset=GardenMembership.objects.all(),
    )

    def __init__(self, group=None, *args, **kwargs):
        super(AddGardenGroupAdminForm, self).__init__(*args, **kwargs)
        self.group = group
        self.fields['users'].queryset = self.get_valid_users(group) \
                .order_by('garden__name')

    def clean_users(self):
        """
        Validate that all users are in fact members of a garden in the group.
        """
        users = self.cleaned_data['users']
        invalid_users = [u for u in users if u not in self.get_valid_users(self.group)]
        if invalid_users:
            raise ValidationError('%s cannot be added to %s' % (
                ', '.join([u.user_profile.user.username for u in invalid_users]),
                self.group,
            ))
        return users

    def get_valid_users(self, group):
        return GardenMembership.objects.filter(garden__in=group.active_gardens())
