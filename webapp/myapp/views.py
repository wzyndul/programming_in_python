from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from .forms import DataEntryForm
from .models import DataEntry
from .serializers import DataEntrySerializer


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
            return HttpResponseNotFound(render(request, 'error_page.html', {'error_code': '404'}), status=404)

        entry.delete()
        return redirect('home')

    return HttpResponseNotFound(render(request, 'error_page.html', {'error_code': '404'}), status=404)


@api_view(['GET', 'POST', 'DELETE'])
def api_data(request, record_id=None):
    if request.method == 'GET':
        entries = DataEntry.objects.all()
        serializer = DataEntrySerializer(entries, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = DataEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'pk': serializer.data['id']}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if record_id is not None:
            try:
                entry = DataEntry.objects.get(id=record_id)
            except DataEntry.DoesNotExist:
                return JsonResponse({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

            entry.delete()
            return JsonResponse({'pk': record_id}, status=status.HTTP_200_OK)


def predict(request):
    if request.method == 'POST':
        form_data = {}
        for field in DataEntry._meta.get_fields():
            if field.name.startswith('continuous_feature'):
                value = request.POST.get(field.name, 0)
                try:
                    form_data[field] = float(value)
                except ValueError:
                    return HttpResponseBadRequest(render(request, 'error_page.html', {'error_code': '400'}))

        all_entries = DataEntry.objects.all()
        continuous_features = []
        categorical_feature = []
        for entry in all_entries:
            continuous_features.append([getattr(entry, field.name) for field in DataEntry._meta.get_fields() if
                                        field.name.startswith('continuous_feature')])
            categorical_feature.append(entry.categorical_feature)

        scaler = StandardScaler()
        standardized_values = scaler.fit_transform(continuous_features)
        knn_classifier = KNeighborsClassifier(n_neighbors=3)
        knn_classifier.fit(standardized_values, categorical_feature)

        new_sample = scaler.transform([list(form_data.values())])
        predicted_category = knn_classifier.predict(new_sample)
        #TODO should I add record to the database?
        return render(request, 'prediction_result.html', {'predicted_category': predicted_category[0]})

    else:
        fields = [field.name for field in DataEntry._meta.get_fields() if field.name.startswith('continuous_feature')]
        return render(request, 'predict_form.html', {'fields': fields})
