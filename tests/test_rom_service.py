import pytest
from pathlib import Path
import tempfile
from modules.roms.service import RomService

class TestRomService:
    @pytest.fixture
    def test_dir(self):
        """Create a temporary directory for test ROMs"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def rom_service(self, test_dir):
        """Create RomService instance with test directory"""
        return RomService(str(test_dir))

    @pytest.fixture
    def sample_roms(self, test_dir):
        """Create sample ROM files in test directory"""
        # Create system directories
        nes_dir = test_dir / "nes"
        snes_dir = test_dir / "snes"
        nes_dir.mkdir()
        snes_dir.mkdir()

        # Create sample ROM files with actual content
        mario_path = nes_dir / "mario.nes"
        zelda_path = nes_dir / "zelda.nes"
        metroid_path = snes_dir / "metroid.smc"
        
        # Write content to files
        mario_path.write_bytes(b'NESTEST')
        zelda_path.write_bytes(b'NESTEST')
        metroid_path.write_bytes(b'SNESTEST')
        
        # Create a non-ROM file
        (test_dir / "readme.txt").write_text("This is not a ROM file")

        return {
            "mario": "nes/mario.nes",
            "zelda": "nes/zelda.nes",
            "metroid": "snes/metroid.smc"
        }

    def test_init_creates_directory(self):
        """Test that constructor creates directory if it doesn't exist"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            new_dir = Path(tmp_dir) / "roms"
            RomService(str(new_dir))
            assert new_dir.exists()

    def test_get_all_roms_empty_directory(self, rom_service):
        """Test get_all_roms with empty directory"""
        roms = rom_service.get_all_roms()
        assert isinstance(roms, list)
        assert len(roms) == 0

    def test_get_all_roms_with_files(self, rom_service, sample_roms, test_dir):
        """Test get_all_roms returns correct ROM list"""
        # Make sure files exist
        assert (test_dir / "nes" / "mario.nes").exists()
        assert (test_dir / "snes" / "metroid.smc").exists()
        
        # Get ROMs
        roms = rom_service.get_all_roms()
        
        # Verify ROM metadata
        assert len(roms) == 3  # We have 3 ROM files
        
        # Check each ROM has required fields
        for rom in roms:
            assert isinstance(rom, dict)
            assert all(key in rom for key in ["name", "path", "size", "system"])
        
        # Check specific ROMs by name
        mario = next((r for r in roms if r["name"] == "mario"), None)
        assert mario is not None
        assert mario["system"] == "Nintendo Entertainment System"

    def test_get_rom_existing(self, rom_service, sample_roms):
        """Test get_rom with existing ROM file"""
        rom = rom_service.get_rom("nes/mario.nes")
        assert rom["name"] == "mario"
        assert rom["path"] == "nes/mario.nes"
        assert rom["system"] == "Nintendo Entertainment System"

    def test_get_rom_nonexistent(self, rom_service):
        """Test get_rom with non-existent file"""
        assert rom_service.get_rom("invalid.rom") is None

    def test_get_rom_invalid_extension(self, rom_service, test_dir):
        """Test get_rom with invalid file extension"""
        invalid_file = test_dir / "invalid.txt"
        invalid_file.touch()
        assert rom_service.get_rom("invalid.txt") is None

    def test_is_rom_file(self, rom_service):
        """Test _is_rom_file with various extensions"""
        valid_extensions = [".nes", ".smc", ".n64", ".gba", ".gb", ".iso"]
        invalid_extensions = [".txt", ".exe", ".zip", ""]

        for ext in valid_extensions:
            assert rom_service._is_rom_file(Path(f"test{ext}"))

        for ext in invalid_extensions:
            assert not rom_service._is_rom_file(Path(f"test{ext}"))

    def test_detect_system(self, rom_service):
        """Test _detect_system with various file types"""
        test_cases = {
            ".nes": "Nintendo Entertainment System",
            ".smc": "Super Nintendo",
            ".n64": "Nintendo 64",
            ".gba": "Game Boy Advance",
            ".gb": "Game Boy",
            ".iso": "PlayStation",
            ".xyz": "Unknown"
        }

        for ext, system in test_cases.items():
            assert rom_service._detect_system(Path(f"test{ext}")) == system