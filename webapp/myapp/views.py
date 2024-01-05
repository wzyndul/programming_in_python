# views.py
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

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