import logging
import os
import shutil
from fastapi import APIRouter, HTTPException, Request
from core.module import LifeLogModule
from .opml import OPMLManager
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

            if not os.path.exists(opml_file):
                logging.warning(f"Podcasts OPML file {opml_file} not found. Creating a new one from template.")
                template_path = os.path.join(os.path.dirname(__file__), 'templates', 'example.opml')
                if not os.path.exists(template_path):
                    logging.error(f"Template OPML file {template_path} not found.")
                    return False
                os.makedirs(os.path.dirname(opml_file), exist_ok=True)
                shutil.copy(template_path, opml_file)

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
