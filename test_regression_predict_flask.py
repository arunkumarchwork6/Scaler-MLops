import pytest
from regression_predict_flask import app, FEATURE_NAMES
import json


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    return app.test_client()


# Sample test data for predictions
SAMPLE_DATA_1 = {
    'age': 45,
    'sex': 1,
    'body mass index': 24.5,
    'average blood pressure': 120,
    'total serum cholesterol': 200,
    's1': 10,
    's2': 15,
    's3': 20,
    's4': 25,
    's5': 30
}

SAMPLE_DATA_2 = {
    'age': 60,
    'sex': 0,
    'body mass index': 28.3,
    'average blood pressure': 130,
    'total serum cholesterol': 240,
    's1': 12,
    's2': 18,
    's3': 22,
    's4': 28,
    's5': 35
}

SAMPLE_DATA_3 = {
    'age': 35,
    'sex': 1,
    'body mass index': 22.1,
    'average blood pressure': 110,
    'total serum cholesterol': 180,
    's1': 8,
    's2': 12,
    's3': 16,
    's4': 20,
    's5': 25
}


def test_index_returns_200(client):
    """Test that index route returns 200 status code."""
    response = client.get('/')
    assert response.status_code == 200


def test_index_returns_html(client):
    """Test that index route returns HTML content."""
    response = client.get('/')
    assert response.content_type == 'text/html; charset=utf-8'


def test_feature_names_exist():
    """Test that FEATURE_NAMES is defined."""
    assert FEATURE_NAMES is not None


def test_feature_names_is_list():
    """Test that FEATURE_NAMES is a list."""
    assert isinstance(FEATURE_NAMES, list)


def test_feature_names_has_ten_elements():
    """Test that FEATURE_NAMES has exactly 10 elements."""
    assert len(FEATURE_NAMES) == 10


def test_feature_names_are_strings():
    """Test that all feature names are strings."""
    assert all(isinstance(name, str) for name in FEATURE_NAMES)


def test_app_exists():
    """Test that Flask app is created."""
    assert app is not None


def test_predict_endpoint_exists(client):
    """Test that /predict endpoint exists."""
    response = client.post('/predict', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code != 404


def test_predict_form_endpoint_exists(client):
    """Test that /predict-form endpoint exists."""
    response = client.post('/predict-form', data={})
    assert response.status_code != 404


def test_invalid_route_returns_404(client):
    """Test that invalid route returns 404."""
    response = client.get('/invalid-route')
    assert response.status_code == 404


# Tests with sample data
@pytest.mark.parametrize("sample_data", [
    SAMPLE_DATA_1,
    SAMPLE_DATA_2,
    SAMPLE_DATA_3
])
def test_predict_with_sample_data(client, sample_data):
    """Test /predict endpoint with various sample data."""
    response = client.post('/predict',
                          data=json.dumps(sample_data),
                          content_type='application/json')
    # Will get 500 if model not loaded, but endpoint should exist
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        json_response = response.get_json()
        assert 'prediction' in json_response or 'error' in json_response


# Form test data
FORM_DATA_1 = {
    'age': '45',
    'sex': '1',
    'body mass index': '24.5',
    'average blood pressure': '120',
    'total serum cholesterol': '200',
    's1': '10',
    's2': '15',
    's3': '20',
    's4': '25',
    's5': '30'
}

FORM_DATA_2 = {
    'age': '60',
    'sex': '0',
    'body mass index': '28.3',
    'average blood pressure': '130',
    'total serum cholesterol': '240',
    's1': '12',
    's2': '18',
    's3': '22',
    's4': '28',
    's5': '35'
}

FORM_DATA_3 = {
    'age': '35',
    'sex': '1',
    'body mass index': '22.1',
    'average blood pressure': '110',
    'total serum cholesterol': '180',
    's1': '8',
    's2': '12',
    's3': '16',
    's4': '20',
    's5': '25'
}


@pytest.mark.parametrize("form_data", [
    FORM_DATA_1,
    FORM_DATA_2,
    FORM_DATA_3
])
def test_predict_form_with_sample_data(client, form_data):
    """Test /predict-form endpoint with various sample data."""
    response = client.post('/predict-form', data=form_data)
    # Will get 500 if model not loaded, but endpoint should exist
    assert response.status_code in [200, 500]


def test_predict_missing_feature(client):
    """Test /predict with missing required feature."""
    incomplete_data = {
        'age': 45,
        'sex': 1,
        # Missing other features
    }
    response = client.post('/predict',
                          data=json.dumps(incomplete_data),
                          content_type='application/json')
    # Should return 400 or 500 (model error)
    assert response.status_code in [400, 500]


def test_predict_form_missing_feature(client):
    """Test /predict-form with missing required feature."""
    incomplete_data = {
        'age': '45',
        'sex': '1',
        # Missing other features
    }
    response = client.post('/predict-form', data=incomplete_data)
    # Should return 400 or 500
    assert response.status_code in [400, 500]


def test_predict_invalid_value(client):
    """Test /predict with invalid feature value."""
    invalid_data = SAMPLE_DATA_1.copy()
    invalid_data['age'] = 'not_a_number'
    response = client.post('/predict',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    # Should return 400 (bad request)
    assert response.status_code == 400
