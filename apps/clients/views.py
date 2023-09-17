from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def clients_list_view(request):
    return render(request, 'clients/clients.html', {})
