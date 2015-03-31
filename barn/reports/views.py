from datetime import date, datetime
from tablib import Databook

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import TemplateView

from django_tablib import Field
from easy_pdf.views import PDFTemplateView

from generic.views import LoginRequiredMixin, TablibView
from metrics.utils import get_min_recorded
from metrics.views import GardenMixin
from metrics.registry import registry

from farmingconcrete.views import GardenGroupMixin


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'


class MetricSpreadsheetMixin(object):

    def get_dataset_class(self, metric_name):
        try:
            return registry[metric_name]['dataset']
        except KeyError:
            return None

    def get_filename(self):
        return '%s - %s - %s' % (
            self.object.name,
            'Barn export',
            date.today().strftime('%Y-%m-%d'),
        )

    def get_dataset(self):
        datasets = []
        for metric in sorted(self.metrics):
            dataset_cls = self.get_dataset_class(metric)
            if not dataset_cls:
                continue
            ds = dataset_cls(gardens=self.get_gardens())

            # Only append if there is data to append
            if not ds.height:
                continue

            # Sheet titles can be 31 characters at most, cannot contain :s
            ds.title = metric[:31].replace(':', '')
            datasets.append(ds)
        if not datasets:
            raise Http404
        return Databook(datasets)


class SpreadsheetView(MetricSpreadsheetMixin, LoginRequiredMixin, GardenMixin,
                      TablibView):
    """
    Export data for a garden for some or all metrics as an Excel spreadsheet.
    """
    format = 'xlsx'

    def get(self, request, *args, **kwargs):
        self.object = self.garden = self.get_object()
        self.metrics = self.get_metrics()
        return super(SpreadsheetView, self).get(request, *args, **kwargs)

    def get_gardens(self):
        return [self.garden,]

    def get_metrics(self):
        try:
            return self.request.GET['metrics'].split(',')
        except Exception:
            # If no metrics and user has access, get all metrics
            if self.garden.is_admin(self.request.user):
                return registry.keys()
            else:
                raise PermissionDenied


class SpreadsheetGroupView(MetricSpreadsheetMixin, GardenGroupMixin,
                           LoginRequiredMixin, TablibView):
    """
    Export data for a garden group for some or all metrics as an Excel 
    spreadsheet.
    """
    format = 'xlsx'

    def get(self, request, *args, **kwargs):
        self.object = self.garden_group = self.get_object()
        self.metrics = self.get_metrics()
        return super(SpreadsheetGroupView, self).get(request, *args, **kwargs)

    def get_dataset_class(self, metric_name):
        try:
            dataset_cls = super(SpreadsheetGroupView, self).get_dataset_class(metric_name)

            # Wrap the dataset from the metric with a class that inserts the
            # garden name as a field
            class GardenDataset(dataset_cls):
                garden = Field(header='garden')
                def __init__(self, *args, **kwargs):
                    self._meta.fields = ['garden',] + super(GardenDataset, self)._meta.fields
                    # garden will be made first in MetricDatasetMixin
                    super(GardenDataset, self).__init__(*args, **kwargs)
            return GardenDataset
        except KeyError:
            return None

    def get_gardens(self):
        return list(self.garden_group.active_gardens.all())

    def get_metrics(self):
        try:
            return self.request.GET['metrics'].split(',')
        except Exception:
            return registry.keys()


class PDFView(LoginRequiredMixin, GardenMixin, PDFTemplateView):
    template_name = 'reports/pdf.html'

    def get_params(self):
        metrics = self.request.GET.get('metrics', None)
        if metrics:
            metrics = metrics.split(',')
        return (
            self.request.GET.get('min', None),
            self.request.GET.get('max', None),
            self.request.GET.get('year', None),
            metrics,
        )

    def get_pdf_filename(self):
        garden = self.get_object()
        min_date, max_date, year, metrics = self.get_params()
        dates = ''
        if year:
            dates = year
        elif min_date and max_date:
            dates = '%s to %s' % (min_date, max_date,)
        else:
            dates = 'All dates'
        return '%s - %s - %s.pdf' % (garden.name, 'Barn', dates,)

    def get_context_data(self, pk=None):
        self.object = self.get_object()
        context = super(PDFView, self).get_context_data()
        min_date, max_date, year, metrics = self.get_params()

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
            'selected_metrics': metrics,
            'today': date.today(),
        })
        return context
