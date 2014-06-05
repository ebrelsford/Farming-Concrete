import json

from django.http import HttpResponse
from django.views.generic import CreateView, ListView

from generic.views import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CropForm, VarietyForm
from .models import Crop, Variety
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


class CreateVarietyView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = VarietyForm
    model = Variety
    permission = 'crops.add_variety'
    template_name = 'crops/variety/variety_form.html'

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'added_by': self.request.user,
            'updated_by': self.request.user,
        })
        return initial

    def get_variety(self, name, crop, user):
        """Get a variety with the given name, creating it if necessary"""
        if not name or not user:
            return None, False

        # Try to find an already-existing variety with that name
        varieties = Variety.objects.filter(
            crop=crop,
            name__istartswith=name,
            needs_moderation=False,
        )
        if varieties:
            return varieties[0], False

        # Try to find a variety this user added but is not moderated
        user_varieties = Variety.objects.filter(
            crop=crop,
            name__istartswith=name,
            added_by=user
        )
        if user_varieties:
            return user_varieties[0], False

        # Else create one
        moderated = not user.has_perm('crops.add_variety_unmoderated')
        variety = Variety(name=name, crop=crop, added_by=user,
                          needs_moderation=moderated)
        variety.save()
        return variety, True

    def form_valid(self, form):
        name = form.cleaned_data['name']
        crop = form.cleaned_data['crop']
        variety, created = self.get_variety(name, crop, self.request.user)
        self.object = variety
        return HttpResponse(json.dumps({
            'name': variety.name,
            'pk': variety.pk,
        }), content_type='application/json')


class ListVarietiesView(LoginRequiredMixin, ListView):

    def get_variety_dicts(self, qs):
        for variety in qs:
            yield {
                'crop': variety.crop.pk,
                'name': variety.name,
                'pk': variety.pk,
            }

    def get_queryset(self):
        qs = Variety.objects.all()

        crop = self.request.GET.get('crop', None)
        if crop:
            qs = qs.filter(crop__pk=crop)

        return qs

    def get_context_data(self, **kwargs):
        return list(self.get_variety_dicts(self.get_queryset()))

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(json.dumps(context), content_type='application/json',
                            **response_kwargs);
