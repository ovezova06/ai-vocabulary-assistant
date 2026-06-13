"""
Unit tests for AI Vocabulary Assistant
Run with: pytest tests/test_app.py -v
"""

import pytest
import tempfile
import os
from app import app
from database import init_db

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    # Initialize test database
    init_db()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

class TestAuthentication:
    """Test user authentication routes"""
    
    def test_home_page(self, client):
        """Test home page redirects to login"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_register_page(self, client):
        """Test register page loads"""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_register_new_user(self, client):
        """Test user registration"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_register_duplicate_user(self, client):
        """Test duplicate user registration"""
        # Register first user
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        # Try to register with same username
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        assert b'already exists' in response.data
    
    def test_login_valid_user(self, client):
        """Test valid user login"""
        # Register user
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        # Login
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_login_invalid_user(self, client):
        """Test invalid user login"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'wrongpassword'
        })
        assert b'Invalid' in response.data

class TestDashboard:
    """Test dashboard routes"""
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_dashboard_search(self, client):
        """Test word search functionality"""
        # Would need to login first and add words
        pass

class TestAIAgent:
    """Test AI agent functionality"""
    
    def test_generate_word_data_demo_word(self):
        """Test generating data for demo word"""
        from ai_agent import generate_word_data
        
        data = generate_word_data('teacher')
        assert data['word'] == 'teacher'
        assert 'phonetic' in data
        assert 'meaning' in data
        assert 'example_sentence' in data
    
    def test_generate_word_data_unknown_word(self):
        """Test generating data for unknown word"""
        from ai_agent import generate_word_data
        
        data = generate_word_data('xyzabc')
        assert data['word'] == 'xyzabc'
        assert data['part_of_speech'] == 'noun'
        assert 'definition' in data['meaning'].lower()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
