from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from make_estimates import make_all_yield_estimates

@staff_member_required
def make_yield_estimates(request):
    start = datetime(2011, 1, 1, 0, 0, 0)
    end = datetime(2012, 1, 1, 0, 0, 0)

    if request.method == 'POST':
        make_all_yield_estimates(start, end)
        return redirect('admin:estimates_estimatedyield_makeall_success')

    return render_to_response('admin/estimates/estimatedyield/makeall.html', {
        'start': start,
        'end': end,
    }, RequestContext(request))
