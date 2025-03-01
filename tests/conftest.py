import pytest
import os
from pathlib import Path
from core.config import Config

# Fixtures
@pytest.fixture(scope="session")
def test_dir():
    """Create and manage test directory"""
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    yield test_dir
    if test_dir.exists():
        for file in test_dir.glob("*"):
            file.unlink()
        test_dir.rmdir()

@pytest.fixture
def test_config(test_dir):
    """Create test configuration"""
    config = Config(str(test_dir))
    config.config = {
        "enable_podcasts": True,
        "podcasts_opml_file": str(test_dir / "test.opml")
    }
    return config

@pytest.fixture
def app(test_config):
    """Create FastAPI app instance with test configuration"""
    from main import create_app
    return create_app(test_config)

@pytest.fixture(autouse=True)
def setup_test_config(test_config):
    # This fixture will automatically run for all tests
    yield test_config
    
    # Cleanup after tests
    test_dir = Path(test_config.user_dir)
    if test_dir.exists():
        for file in test_dir.glob("*"):
            file.unlink()
        test_dir.rmdir()