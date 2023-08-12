from django.shortcuts import render

def clients_list_view(request):
    return render(request, 'clients/clients.html', {})
