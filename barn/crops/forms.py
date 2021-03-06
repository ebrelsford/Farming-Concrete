from django.forms import HiddenInput, ModelForm, ModelChoiceField

from floppyforms.widgets import Select

from .models import Crop, Variety


class AddNewCropWidget(Select):
    template_name = 'crops/crop/new_crop_widget.html'


class CropForm(ModelForm):

    class Meta:
        fields = '__all__'
        model = Crop
        widgets = {
            'added_by': HiddenInput(),
            'needs_moderation': HiddenInput(),
            'updated_by': HiddenInput(),
        }


class AddNewVarietyWidget(Select):
    template_name = 'crops/variety/new_crop_variety_widget.html'


class VarietyField(ModelChoiceField):
    label = 'Variety name'
    widget = AddNewVarietyWidget()


class VarietyForm(ModelForm):

    class Meta:
        fields = '__all__'
        model = Variety
        widgets = {
            'added_by': HiddenInput(),
            'crop': HiddenInput(),
            'needs_moderation': HiddenInput(),
            'updated_by': HiddenInput(),
        }
