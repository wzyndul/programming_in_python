from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from .forms import DataEntryForm
from .models import DataEntry
from .serializers import DataEntrySerializer, PredictionSerializer


@require_GET
def home(request):
    entries = DataEntry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def add(request):
    if request.method == 'POST':
        form = DataEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponseBadRequest(render(request, 'error_page.html', {'error_code': '400'}))
    else:
        form = DataEntryForm()

    return render(request, 'add_data_form.html', {'form': form})


@require_POST
def delete(request, record_id):
    try:
        entry = DataEntry.objects.get(id=record_id)
    except DataEntry.DoesNotExist:
        return HttpResponseNotFound(render(request, 'error_page.html', {'error_code': '404'}), status=404)

    entry.delete()
    return redirect('home')


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
        value_feature1 = request.POST.get('continuous_feature1', 0)
        value_feature2 = request.POST.get('continuous_feature2', 0)
        try:
            form_data['continuous_feature1'] = float(value_feature1)
            form_data['continuous_feature2'] = float(value_feature2)
        except ValueError:
            return HttpResponseBadRequest(render(request, 'error_page.html', {'error_code': '400'}))

        all_entries = DataEntry.objects.all()
        continuous_features = [[entry.continuous_feature1, entry.continuous_feature2] for entry in all_entries]
        categorical_feature = [entry.categorical_feature for entry in all_entries]

        scaler = StandardScaler()
        standardized_values = scaler.fit_transform(continuous_features)
        knn_classifier = KNeighborsClassifier(n_neighbors=3)
        knn_classifier.fit(standardized_values, categorical_feature)

        new_sample = scaler.transform([list(form_data.values())])
        predicted_category = knn_classifier.predict(new_sample)
        # TODO should I add record to the database?
        return render(request, 'prediction_result.html', {'predicted_category': predicted_category[0]})

    elif request.method == 'GET':
        fields = ['continuous_feature1', 'continuous_feature2']
        return render(request, 'predict_form.html', {'fields': fields})


@api_view(['GET'])
def api_predictions(request):
    # Create the serializer instance
    serializer = PredictionSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    all_entries = DataEntry.objects.all()

    continuous_features = [[entry.continuous_feature1, entry.continuous_feature2] for entry in all_entries]
    categorical_feature = [entry.categorical_feature for entry in all_entries]

    scaler = StandardScaler()
    standardized_values = scaler.fit_transform(continuous_features)

    knn_classifier = KNeighborsClassifier(n_neighbors=3)
    knn_classifier.fit(standardized_values, categorical_feature)

    new_sample = scaler.transform(
        [[serializer.validated_data['continuous_feature1'], serializer.validated_data['continuous_feature2']]])

    predicted_category = knn_classifier.predict(new_sample)

    return JsonResponse({'predicted_category': int(predicted_category[0])})
