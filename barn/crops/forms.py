from django.forms import HiddenInput, ModelForm

from floppyforms.widgets import Select

from .models import Crop


class AddNewCropWidget(Select):
    template_name = 'crops/crop/new_crop_widget.html'


class CropForm(ModelForm):

    class Meta:
        model = Crop
        widgets = {
            'added_by': HiddenInput(),
            'needs_moderation': HiddenInput(),
            'updated_by': HiddenInput(),
        }
