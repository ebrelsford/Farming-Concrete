import json

from django.http import HttpResponse
from django.views.generic import CreateView

from generic.views import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CropForm
from .models import Crop
from .utils import get_crop


class CreateCropView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CropForm
    model = Crop
    permission = 'crops.add_crop'
    template_name = 'crops/crop/crop_form.html'

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'added_by': self.request.user,
            'updated_by': self.request.user,
        })
        return initial

    def form_valid(self, form):
        name = form.cleaned_data['name']
        crop, created = get_crop(name, self.request.user)
        self.object = crop
        return HttpResponse(json.dumps({
            'name': crop.name,
            'pk': crop.pk,
        }), content_type='application/json')
