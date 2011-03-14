from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def account(request):
    return render_to_response('farmingconcrete/account.html', { })
