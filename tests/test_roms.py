import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from unittest.mock import Mock, patch
from modules.roms.module import Roms
from modules.roms.service import RomService
from main import app

@pytest.fixture
def app_with_mocks(test_roms):
    """Create app with mocked modules for testing"""
    with patch('modules.roms.module.RomService') as mock_service_class:
        # Setup mock service
        mock_service = Mock()
        mock_service.get_all_roms.return_value = test_roms
        mock_service.get_rom.side_effect = lambda path: next(
            (rom for rom in test_roms if rom['path'] == path), None
        )
        mock_service_class.return_value = mock_service
        
        # Import here to use the mock
        from main import create_app
        app = create_app()
        
        yield app

@pytest.fixture
def client(app_with_mocks):
    """Create test client with mocked app"""
    with TestClient(app_with_mocks) as client:
        yield client

class TestRomsModule:
    @pytest.fixture
    def roms_module(self):
        return Roms()

    def test_initialize_success(self, roms_module, tmp_path):
        """Test successful initialization with valid directory"""
        # Create test config with temp directory
        config = {'roms_directory': str(tmp_path)}
        
        # Test initialization
        result = roms_module.initialize(config)
        
        assert result is True
        assert isinstance(roms_module.service, RomService)
        assert roms_module.service.roms_directory == tmp_path

    def test_initialize_missing_config(self, roms_module):
        """Test initialization fails with missing directory config"""
        # Test with empty config
        result = roms_module.initialize({})
        
        assert result is False

    def test_initialize_invalid_directory(self, roms_module):
        """Test initialization fails with non-existent directory"""
        # Create config with non-existent path
        config = {'roms_directory': '/not/a/real/path'}
        
        # Test initialization
        result = roms_module.initialize(config)
        
        assert result is False

    @patch('modules.roms.module.RomService')
    def test_initialize_handles_exception(self, mock_service, roms_module):
        """Test initialization handles exceptions gracefully"""
        # Configure mock to raise exception
        mock_service.side_effect = Exception("Test error")
        
        # Test initialization with valid config
        config = {'roms_directory': '/some/path'}
        result = roms_module.initialize(config)
        
        assert result is False

    def test_get_name(self, roms_module):
        """Test get_name returns correct module name"""
        assert roms_module.get_name() == "roms"

    def test_get_router(self, roms_module):
        """Test get_router returns FastAPI router"""
        router = roms_module.get_router()
        assert router.prefix == "/roms"
        assert router.tags == ["roms"]

class TestRomsAPI:
    @pytest.fixture
    def test_roms(self):
        return [
            {
                "name": "Super Mario Bros",
                "path": "nes/mario.nes",
                "size": 40960,
                "system": "Nintendo Entertainment System"
            },
            {
                "name": "Sonic",
                "path": "genesis/sonic.bin",
                "size": 524288,
                "system": "Sega Genesis"
            }
        ]

    @pytest.fixture
    def mock_rom_service(self, test_roms):
        with patch('modules.roms.service.RomService') as mock:
            service = mock.return_value
            service.get_all_roms.return_value = test_roms
            service.get_rom.side_effect = lambda path: next(
                (rom for rom in test_roms if rom['path'] == path), None
            )
            yield service

    def test_list_roms_returns_200(self, client):
        """Test that /roms endpoint returns 200 status code"""
        response = client.get("/roms")
        assert response.status_code == 200

    def test_list_roms_returns_list(self, client, test_roms):
        """Test that /roms endpoint returns list of ROMs"""
        response = client.get("/roms")
        data = response.json()
        assert "roms" in data
        assert len(data["roms"]) == len(test_roms)

    def test_get_rom_returns_200(self, client):
        """Test that /roms/{path} returns 200 for valid ROM"""
        response = client.get("/roms/nes/mario.nes")
        assert response.status_code == 200
        
    def test_get_rom_returns_404(self, client):
        """Test that /roms/{path} returns 404 for invalid ROM"""
        response = client.get("/roms/invalid/path.rom")
        assert response.status_code == 404

    def test_get_rom_returns_correct_data(self, client, test_roms):
        """Test that /roms/{path} returns correct ROM data"""
        path = "nes/mario.nes"
        response = client.get(f"/roms/{path}")
        data = response.json()
        expected = next(rom for rom in test_roms if rom['path'] == path)
        assert data == expected

    @pytest.mark.asyncio
    async def test_list_roms_async(self, client, test_roms):
        """Test async ROM listing"""
        response = client.get("/roms")
        data = response.json()
        assert "roms" in data
        assert isinstance(data["roms"], list)