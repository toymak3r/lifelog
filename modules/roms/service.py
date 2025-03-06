import os
import logging
from pathlib import Path
from typing import List, Dict, Optional

class RomService:
    def __init__(self, roms_directory: str):
        self.roms_directory = Path(roms_directory)
        if not self.roms_directory.exists():
            self.roms_directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created ROMs directory: {roms_directory}")
            
    def get_all_roms(self) -> List[Dict]:
        """Get list of all ROMs with metadata"""
        roms = []
        try:
            for rom_file in self.roms_directory.rglob("*"):
                # Skip directories and only process files
                if not rom_file.is_file():
                    continue
                    
                if self._is_rom_file(rom_file):
                    roms.append({
                        "name": rom_file.stem,
                        "path": str(rom_file.relative_to(self.roms_directory)),
                        "size": rom_file.stat().st_size,
                        "system": self._detect_system(rom_file)
                    })
        except Exception as e:
            logging.error(f"Error listing ROMs: {e}")
            
        return roms

    def get_rom(self, rom_path: str) -> Optional[Dict]:
        """Get metadata for a specific ROM"""
        try:
            full_path = self.roms_directory / rom_path
            if full_path.is_file() and self._is_rom_file(full_path):
                return {
                    "name": full_path.stem,
                    "path": rom_path,
                    "size": full_path.stat().st_size,
                    "system": self._detect_system(full_path)
                }
        except Exception as e:
            logging.error(f"Error getting ROM {rom_path}: {e}")
            
        return None

    def _is_rom_file(self, file_path: Path) -> bool:
        """Check if file is a valid ROM based on extension"""
        valid_extensions = {'.nes', '.smc', '.n64', '.gba', '.gb', '.iso'}
        return file_path.suffix.lower() in valid_extensions

    def _detect_system(self, rom_path: Path) -> str:
        """Detect gaming system based on file extension"""
        extension_map = {
            '.nes': 'Nintendo Entertainment System',
            '.smc': 'Super Nintendo',
            '.n64': 'Nintendo 64',
            '.gba': 'Game Boy Advance',
            '.gb': 'Game Boy',
            '.iso': 'PlayStation'
        }
        return extension_map.get(rom_path.suffix.lower(), 'Unknown')