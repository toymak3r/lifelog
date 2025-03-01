import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from main import app

# Constants
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_OPML_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head><title>Test Podcasts</title></head>
    <body></body>
</opml>'''

class TestPodcastAPI:
    """Test cases for Podcast API endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_dir):
        """Setup test environment"""
        # Create test OPML file
        opml_path = test_dir / "test.opml"
        with open(opml_path, "w") as f:
            f.write(TEST_OPML_CONTENT)
            
        # Initialize test client
        self.client = TestClient(app)
        
        yield
        
        # Cleanup
        if opml_path.exists():
            opml_path.unlink()

    def test_root_returns_404(self):
        """Test that undefined routes return 404"""
        response = self.client.get("/")
        assert response.status_code == 404

    def test_get_podcasts_returns_list(self):
        """Test that /podcasts endpoint returns a list"""
        response = self.client.get("/podcasts")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_get_podcasts_async(self):
        """Test async podcast retrieval"""
        response = self.client.get("/podcasts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)