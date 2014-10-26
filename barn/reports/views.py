from datetime import date, datetime
from tablib import Databook

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import TemplateView

from easy_pdf.views import PDFTemplateView

from generic.views import LoginRequiredMixin, TablibView
from metrics.utils import get_min_recorded
from metrics.views import GardenMixin
from metrics.registry import registry


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'


class ExportView(LoginRequiredMixin, GardenMixin, TablibView):
    """
    Export data for a garden for some or all metrics as an Excel spreadsheet.
    """
    format = 'xlsx'

    def get(self, request, *args, **kwargs):
        self.object = self.garden = self.get_object()
        self.metrics = self.get_metrics()
        return super(ExportView, self).get(request, *args, **kwargs)

    def get_dataset_class(self, metric_name):
        try:
            return registry[metric_name]['dataset']
        except KeyError:
            return None

    def can_download_all(self, user, garden):
        """
        If user has superadmin permissions or is listed as an admin for a
        garden, let them download all the data for the garden.
        """
        if user.has_perm('farmingconcrete.can_edit_any_garden'):
            return True
        return user.gardenmembership_set.filter(
            garden=garden,
            is_admin=True,
        ).exists()

    def get_metrics(self):
        try:
            return self.request.GET['metrics'].split(',')
        except Exception:
            # If no metrics and user has access, get all metrics
            if self.can_download_all(self.request.user, self.garden):
                return registry.keys()
            else:
                raise PermissionDenied

    def get_dataset(self):
        datasets = []
        for metric in sorted(self.metrics):
            dataset_cls = self.get_dataset_class(metric)
            if not dataset_cls:
                continue
            ds = dataset_cls(gardens=[self.garden])

            # Only append if there is data to append
            if not ds.height:
                continue

            # Sheet titles can be 31 characters at most, cannot contain :s
            ds.title = metric[:31].replace(':', '')
            datasets.append(ds)
        if not datasets:
            raise Http404
        return Databook(datasets)

    def get_filename(self):
        return '%s - %s - %s' % (
            self.garden.name,
            'Barn export',
            date.today().strftime('%Y-%m-%d'),
        )


class ReportView(GardenMixin, PDFTemplateView):
    template_name = 'reports/pdf.html'

    def get_params(self):
        return (
            self.request.GET.get('min', None),
            self.request.GET.get('max', None),
            self.request.GET.get('year', None),
        )

    def get_pdf_filename(self):
        garden = self.get_object()
        min_date, max_date, year = self.get_params()
        dates = ''
        if year:
            dates = year
        else:
            dates = '%s to %s' % (min_date, max_date,)
        return '%s - %s - %s' % (garden.name, 'Barn', dates,)

    def get_context_data(self, pk=None):
        self.object = self.get_object()
        context = super(ReportView, self).get_context_data()
        min_date, max_date, year = self.get_params()

        if min_date:
            min_date = datetime.strptime(min_date, '%m/%d/%Y')
        if max_date:
            max_date = datetime.strptime(max_date, '%m/%d/%Y')

        if year:
            min_date = date(int(year), 1, 1)
            max_date = date(int(year), 12, 31)

        if not min_date:
            min_date = get_min_recorded(self.object)

        if not max_date:
            max_date = date.today()

        context.update({
            'garden': self.object,
            'min': min_date,
            'max': max_date,
        })
        return context
