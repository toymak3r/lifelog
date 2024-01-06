import falcon
import json

from .opml import OPMLManager


class Podcasts:
    def __init__(self, file_path) -> None:
        self.opml_manager = OPMLManager(file_path)

    def on_get(self, req, resp):
        feeds = self.opml_manager.extract_feeds()
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps(feeds, ensure_ascii=False)

    def on_delete(self, req, resp):
        podcast_id = req.params['podcast_id']

        # Assume you have some logic to delete the podcast with the given ID
        # Replace this with your actual delete logic
        if self.opml_manager.remove_feed_by_url(podcast_id):

            deleted_podcast = {
                'podcast_id': req.params['podcast_id'],
                'status': 'deleted'
            }

            self.opml_manager.save_opml()

            resp.status = falcon.HTTP_200  # OK
            resp.body = json.dumps(deleted_podcast)

        else:
            resp.status = falcon.HTTP_404  # NOK

    def on_put(self, req, resp):
        podcast_rss = req.params['podcast_rss']

        if self.opml_manager.add_feed_from_rss(podcast_rss):

            self.opml_manager.save_opml()
            resp.status = falcon.HTTP_200  # OK
        else:
            resp.status = falcon.HTTP_404  # NOK