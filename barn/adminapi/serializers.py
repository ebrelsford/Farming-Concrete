from django.contrib.auth.models import User

from actstream.models import Action
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class GenericSerializer(serializers.BaseSerializer):

    def display_name(self, obj):
        return str(obj)

    def to_representation(self, obj):
        obj_repr = {
            'app_label': obj._meta.app_label,
            'id': obj.pk,
            'display_name': self.display_name(obj),
            'model_name': obj._meta.model_name,
        }
        try:
            obj_repr['url'] =  obj.get_absolute_url()
        except Exception:
            pass
        return obj_repr


class ActionSerializer(serializers.ModelSerializer):
    actor = UserSerializer()
    action_object = GenericSerializer()
    target = GenericSerializer()

    class Meta:
        depth = 1
        fields = ('id', 'actor', 'verb', 'description', 'action_object',
                  'target', 'timestamp',)
        model = Action
