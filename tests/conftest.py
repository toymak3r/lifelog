import pytest
import shutil
import tempfile
from pathlib import Path
from core.config import Config

# Fixtures
@pytest.fixture
def test_dir():
    """Create a temporary directory for test ROMs"""
    tmp_dir = tempfile.mkdtemp()
    yield Path(tmp_dir)
    # Clean up the directory
    shutil.rmtree(tmp_dir, ignore_errors=True)

@pytest.fixture
def test_config():
    """Create test configuration"""
    config = Config(user_dir="/tmp/lifelog_test")
    
    # Override settings for testing
    config.config.update({
        "enable_podcasts": True,
        "podcasts_opml_file": "/tmp/test_podcasts.opml",
        "enable_roms": True,
        "roms_directory": "/tmp/test_roms"
    })
    
    return config

@pytest.fixture
def app(test_config):
    """Create FastAPI app instance with test configuration"""
    from main import create_app
    return create_app(test_config)

@pytest.fixture(autouse=True)
def setup_test_config(test_config):
    """Setup and cleanup test environment"""
    # This fixture will automatically run for all tests
    yield test_config
    
    # Cleanup after tests
    test_dir = Path(test_config.user_dir)
    if test_dir.exists():
        # Recursively remove all files and directories
        shutil.rmtree(test_dir, ignore_errors=True)