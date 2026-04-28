import pytest
from appflask import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
    # we can do some cleanup here if needed after tests run


class TestPingEndpoint:
    """Tests for the /ping endpoint."""
    
    def test_ping_get_request(self, client):
        """Test GET request to /ping endpoint returns correct response."""
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.data.decode() == "I am working fine"
    
    def test_ping_response_type(self, client):
        """Test that /ping returns string response."""
        response = client.get('/ping')
        assert isinstance(response.data.decode(), str)
    
    def test_ping_post_not_allowed(self, client):
        """Test that POST request to /ping is not allowed."""
        response = client.post('/ping')
        assert response.status_code == 405


class TestHomeEndpoint:
    """Tests for the / (home) endpoint."""
    
    def test_home_get_request(self, client):
        """Test GET request to / endpoint returns correct response."""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data.decode() == "I am in home page"
    
    def test_home_response_type(self, client):
        """Test that / returns string response."""
        response = client.get('/')
        assert isinstance(response.data.decode(), str)
    
    def test_home_post_not_allowed(self, client):
        """Test that POST request to / is not allowed."""
        response = client.post('/')
        assert response.status_code == 405


class TestInvalidRoutes:
    """Tests for invalid routes."""
    
    def test_invalid_route_404(self, client):
        """Test that invalid route returns 404 error."""
        response = client.get('/invalid')
        assert response.status_code == 404
    
    def test_another_invalid_route_404(self, client):
        """Test another invalid route returns 404 error."""
        response = client.get('/api/test')
        assert response.status_code == 404


class TestAppInitialization:
    """Tests for Flask app initialization."""
    
    def test_app_exists(self):
        """Test that Flask app is created."""
        assert app is not None
    
    def test_app_is_testing(self):
        """Test that app can be set to testing mode."""
        app.config['TESTING'] = True
        assert app.config['TESTING'] is True

