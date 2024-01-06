from wsgiref.simple_server import make_server
import falcon
from datetime import date
from core.config import Config
from podcasts.podcast_service import Podcasts


actual_date = date.today()
configuration = Config()

app = falcon.App()

podcasts = Podcasts(configuration.config['podcasts_opml_file'])

# things will handle all requests to the '/things' URL path
app.add_route('/podcasts', podcasts)
app.add_route('/podcasts/delete', podcasts)
app.add_route('/podcasts/add', podcasts)

if __name__ == '__main__':
    with make_server('', 5000, app) as httpd:
        print('Serving on port 5000...')

        # Serve until process is killed
        httpd.serve_forever()
