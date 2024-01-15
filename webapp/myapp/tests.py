from django.test import TestCase, Client
import random


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_data_post(self):
        data = {"continuous_feature1": 1.23, "continuous_feature2": 1.88,
                "categorical_feature": 1}
        response = self.client.post('/api/data', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('pk'), 1)

    def test_api_data_post_invalid_data(self):
        data = {"continuous_feature1": 1.23, "continuous_feature2": 1.88,
                "categorical_feature": "invalid"}
        response = self.client.post('/api/data', data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid data')

    def test_api_data_get_empty(self):
        response = self.client.get('/api/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_api_data_get(self):
        data = {"continuous_feature1": 1.23, "continuous_feature2": 1.88,
                "categorical_feature": 1}
        self.client.post('/api/data', data)

        response = self.client.get('/api/data')
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.json(), [])

    def test_api_data_get_with_data(self):
        data = {"continuous_feature1": 1.23, "continuous_feature2": 1.88,
                "categorical_feature": 1}
        self.client.post('/api/data', data)
        response = self.client.get('/api/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 1, 'continuous_feature1': 1.23, 'continuous_feature2': 1.88,
             'categorical_feature': 1}])

    def test_api_data_delete(self):
        data = {"continuous_feature1": 1.23, "continuous_feature2": 1.88,
                "categorical_feature": 1}
        self.client.post('/api/data', data)
        response = self.client.delete('/api/data/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('pk'), 1)

    def test_api_data_delete_not_found(self):
        response = self.client.delete('/api/data/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('error'), 'Record not found')

    def test_api_predictions_get(self):
        for i in range(10):
            data = {"continuous_feature1": random.uniform(0, 1000),
                    "continuous_feature2": random.uniform(0, 1000),
                    "categorical_feature": random.randint(1, 3)}
            self.client.post('/api/data', data)

        response = self.client.get(
            '/api/predictions?continuous_feature1=1.23&'
            'continuous_feature2=1.88')
        self.assertEqual(response.status_code, 200)
        predicted_category = response.json().get('predicted_category')
        self.assertTrue(predicted_category in {1, 2, 3})

    def test_api_predictions_get_invalid_data(self):
        response = self.client.get(
            '/api/predictions?continuous_feature1=1.23&'
            'continuous_feature2=invalid')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid data')
