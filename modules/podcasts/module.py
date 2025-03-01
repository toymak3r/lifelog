from typing import Dict
import logging
from core.module import LifeLogModule
from .opml import OPMLManager
from fastapi import APIRouter, HTTPException, Request
from .podfeeds import PodFeeds

class Podcasts(LifeLogModule):
    def __init__(self):
        self.service = None
        self.router = APIRouter(prefix="/podcasts", tags=["podcasts"])
        self._setup_routes()

    def initialize(self, config: dict) -> bool:
        try:
            opml_file = config.get('podcasts_opml_file')
            if not opml_file:
                logging.error("Podcasts OPML file not specified in the configuration.")
                return False

            self.service = PodFeeds(opml_file)
            return True
        except Exception as e:
            logging.error(f"Failed to initialize podcasts module: {e}")
            return False

    def get_name(self) -> str:
        return "podcasts"

    def get_router(self) -> APIRouter:
        return self.router

    def _setup_routes(self):
        @self.router.get("")
        async def get_podcasts():
            if not self.service:
                raise HTTPException(
                    status_code=500, 
                    detail="Podcasts module not available"
                )
            return await self.service.get_podcasts()

        @self.router.delete("/{podcast_id}")
        async def delete_podcast(podcast_id: str):
            if not self.service:
                raise HTTPException(
                    status_code=500, 
                    detail="Podcasts module not available"
                )
            return await self.service.delete_podcast(podcast_id)

        @self.router.put("")
        async def put_podcast(request: Request):
            if not self.service:
                raise HTTPException(
                    status_code=500, 
                    detail="Podcasts module not available"
                )
            data = await request.json()
            podcast_rss = data.get('podcast_rss')
            if not podcast_rss:
                raise HTTPException(
                    status_code=400, 
                    detail="podcast_rss is required"
                )
            return await self.service.put_podcast(podcast_rss)
