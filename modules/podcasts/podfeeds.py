from fastapi import HTTPException
from fastapi.responses import JSONResponse

from .opml import OPMLManager

class PodFeeds:
    def __init__(self, file_path) -> None:
        self.opml_manager = OPMLManager(file_path)

    async def get_podcasts(self):
        feeds = self.opml_manager.extract_feeds()
        return JSONResponse(content=feeds, status_code=200)

    async def delete_podcast(self, podcast_id: str):
        if self.opml_manager.remove_feed_by_url(podcast_id):
            deleted_podcast = {
                'podcast_id': podcast_id,
                'status': 'deleted'
            }
            self.opml_manager.save_opml()
            return JSONResponse(content=deleted_podcast, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Podcast not found")

    async def put_podcast(self, podcast_rss: str):
        if self.opml_manager.add_feed_from_rss(podcast_rss):
            self.opml_manager.save_opml()
            return JSONResponse(status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Failed to add podcast")
