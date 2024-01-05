from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view

from .forms import DataEntryForm
from .models import DataEntry


def home(request):
    entries = DataEntry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def add(request):
    if request.method == 'POST':
        form = DataEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page
        else:
            return HttpResponseBadRequest(render(request, 'error_page.html', {'error_code': '400'}))
    else:
        form = DataEntryForm()

    return render(request, 'add_data_form.html', {'form': form})


@require_POST
def delete(request, record_id):
    if request.method == 'POST':
        try:
            entry = DataEntry.objects.get(id=record_id)
        except DataEntry.DoesNotExist:
            return HttpResponseNotFound(render(request, 'error_page.html', {'error_code': '404'}))

        entry.delete()
        return redirect('home')

    return HttpResponseNotFound(render(request, 'error_page.html', {'error_code': '404'}))



