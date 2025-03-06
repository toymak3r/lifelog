from fastapi import APIRouter, HTTPException
import logging
from core.module import LifeLogModule
from .service import RomService

class Roms(LifeLogModule):
    def __init__(self):
        self.service = None
        self.router = APIRouter(prefix="/roms", tags=["roms"])
        self._setup_routes()

    def initialize(self, config: dict) -> bool:
        try:
            roms_directory = config.get('roms_directory')
            if not roms_directory:
                logging.error("ROMs directory not specified in configuration")
                return False
                
            self.service = RomService(roms_directory)
            return True
        except Exception as e:
            logging.error(f"Failed to initialize ROMs module: {e}")
            return False

    def get_name(self) -> str:
        return "roms"

    def get_router(self) -> APIRouter:
        return self.router

    def _setup_routes(self):
        @self.router.get("/")
        async def list_roms():
            return {"roms": self.service.get_all_roms()}

        @self.router.get("/{rom_path:path}")
        async def get_rom(rom_path: str):
            rom = self.service.get_rom(rom_path)
            if not rom:
                raise HTTPException(status_code=404, detail="ROM not found")
            return rom