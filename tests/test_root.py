"""
Tests for the root endpoint (GET /)
"""
import pytest


class TestRoot:
    """Test suite for the root endpoint"""

    def test_root_redirect_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /
        - Assert: Response is a redirect (307) to /static/index.html
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_follows(self, client):
        """
        Test that following the redirect from / works
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to / with follow_redirects=True
        - Assert: Final response status is 200 (or 404 if file not found in test)
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=True)
        
        # Assert - Should redirect and attempt to load the HTML file
        # In test environment, the static file mount will handle this
        assert response.status_code == 200
