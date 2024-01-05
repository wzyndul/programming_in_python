# views.py

from django.shortcuts import render, redirect

from .forms import DataEntryForm
from .models import DataEntry


def home(request):
    entries = DataEntry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def add_data(request):
    if request.method == 'POST':
        form = DataEntryForm(request.POST)
        if form.is_valid():
            # Save the new data point to the database
            form.save()
            return redirect('index')  # Redirect to the home page
    else:
        form = DataEntryForm()

    return render(request, 'add_data_form.html', {'form': form})