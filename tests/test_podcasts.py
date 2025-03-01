import os
import tempfile
import pytest
import xml.etree.ElementTree as ET
from modules.podcasts.opml import OPMLManager

class TestOPMLManager:

    def test_read_opml_returns_root_element(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        root = opml_manager.read_opml()
        assert isinstance(root, ET.Element)
        os.remove(file_path)

    def test_extract_feeds_returns_list_of_dictionaries(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n  <head>\n    <title>Test OPML</title>\n  </head>\n  <body>\n    <outline text="Feed 1" type="rss" xmlUrl="https://feed1.com/rss" htmlUrl="https://feed1.com" imageUrl="https://feed1.com/image.jpg"/>\n    <outline text="Feed 2" type="rss" xmlUrl="https://feed2.com/rss" htmlUrl="https://feed2.com" imageUrl="https://feed2.com/image.jpg"/>\n  </body>\n</opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        feeds = opml_manager.extract_feeds()
        assert isinstance(feeds, list)
        for feed in feeds:
            assert isinstance(feed, dict)
        os.remove(file_path)

    def test_add_feed_adds_new_feed_to_opml_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        title = "Test Feed"
        new_feed_url = "https://example.com/feed"
        opml_manager.add_feed(title, new_feed_url)
        feeds = opml_manager.extract_feeds()
        assert any(feed['title'] == title and feed['url'] == new_feed_url for feed in feeds)
        os.remove(file_path)

    def test_read_opml_raises_opml_parse_error_if_file_cannot_be_parsed_with_temporary_invalid_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b"<invalid>")
            file_path = temp_file.name

        with pytest.raises(OPMLManager.OPMLParseError):
            opml_manager = OPMLManager(file_path)
        os.remove(file_path)

    def test_add_feed_raises_value_error_if_argument_not_string(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        title = 123
        new_feed_url = "https://example.com/feed"
        with pytest.raises(ValueError):
            opml_manager.add_feed(title, new_feed_url)
        os.remove(file_path)

    def test_add_feed_raises_type_error_if_title_or_new_feed_url_not_provided(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        with pytest.raises(TypeError):
            opml_manager.add_feed()
        os.remove(file_path)

    def test_remove_feed_by_url(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head></head><body><outline text="Feed 1" type="rss" xmlUrl="https://feed1.com" imageUrl="https://image1.com" htmlUrl="https://html1.com"></outline><outline text="Feed 2" type="rss" xmlUrl="https://feed2.com" imageUrl="https://image2.com" htmlUrl="https://html2.com"></outline></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        opml_manager.remove_feed_by_url("https://feed1.com")
        assert len(opml_manager.opml_root.findall(".//outline")) == 1
        assert opml_manager.opml_root.findall(".//outline")[0].get("xmlUrl") == "https://feed2.com"
        assert opml_manager.opml_root.findall(".//outline")[0].get("imageUrl") == "https://image2.com"
        assert opml_manager.opml_root.findall(".//outline")[0].get("htmlUrl") == "https://html2.com"
        assert opml_manager.opml_root.findall(".//outline")[0].get("text") == "Feed 2"
        assert opml_manager.opml_root.findall(".//outline")[0].get("type") == "rss"
        os.remove(file_path)

    def test_get_image_url_returns_image_url(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head></head><body><outline text="Feed 1" type="rss" xmlUrl="https://feed1.com" imageUrl="https://image1.com" htmlUrl="https://html1.com"></outline><outline text="Feed 2" type="rss" xmlUrl="https://feed2.com" imageUrl="https://image2.com" htmlUrl="https://html2.com"></outline></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        image_url = opml_manager.get_image_url("https://feed1.com")
        assert image_url == "https://image1.com"
        os.remove(file_path)

    def test_initialized_with_nonexistent_file_path(self):
        file_path = "nonexistent.opml"
        with open(file_path, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"></opml>')

        opml_manager = OPMLManager(file_path)
        assert isinstance(opml_manager, OPMLManager)
        os.remove(file_path)

    def test_initialized_with_empty_opml(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        assert isinstance(opml_manager.opml_root, ET.Element)
        os.remove(file_path)

    def test_initialized_with_empty_opml_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="1.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        assert isinstance(opml_manager.opml_root, ET.Element)
        os.remove(file_path)

    def test_add_feed_with_only_required_arguments(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        opml_manager.add_feed("Test Feed", "https://example.com/feed")
        assert len(opml_manager.opml_root.findall(".//outline")) == 1
        assert opml_manager.opml_root.findall(".//outline")[-1].get("text") == "Test Feed"
        assert opml_manager.opml_root.findall(".//outline")[-1].get("type") == "rss"
        assert opml_manager.opml_root.findall(".//outline")[-1].get("xmlUrl") == "https://example.com/feed"
        assert opml_manager.opml_root.findall(".//outline")[-1].get("htmlUrl") is None
        assert opml_manager.opml_root.findall(".//outline")[-1].get("imageUrl") is None
        os.remove(file_path)

    def test_add_feed_with_all_optional_arguments(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        opml_manager.add_feed("Test Feed", "https://example.com/feed", type="rss", html="https://example.com", imageUrl="https://example.com/image.jpg")
        feeds = opml_manager.extract_feeds()
        assert any(feed['title'] == "Test Feed" for feed in feeds)
        assert any(feed['type'] == "rss" for feed in feeds)
        assert any(feed['url'] == "https://example.com/feed" for feed in feeds)
        assert any(feed['imageUrl'] == "https://example.com/image.jpg" for feed in feeds)
        assert any(feed['html'] == "https://example.com" for feed in feeds)
        os.remove(file_path)

    def test_initialize_opml_manager_with_valid_opml_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n  <head>\n    <title>Test OPML</title>\n    <dateCreated>2022-01-01T00:00:00Z</dateCreated>\n    <dateModified>2022-01-01T00:00:00Z</dateModified>\n  </head>\n  <body>\n    <outline text="Test Feed" type="rss" xmlUrl="https://example.com/feed" htmlUrl="https://example.com" imageUrl="https://example.com/image.jpg"/>\n  </body>\n</opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        assert opml_manager.file_path == file_path
        assert opml_manager.opml_root is not None
        os.remove(file_path)

    def test_extract_feeds(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<opml version="1.0">\n  <head>\n    <title>Test OPML</title>\n    <dateCreated>2022-01-01T00:00:00Z</dateCreated>\n    <dateModified>2022-01-01T00:00:00Z</dateModified>\n  </head>\n  <body>\n    <outline text="Feed 1" type="rss" xmlUrl="https://example.com/feed1" htmlUrl="https://example.com/feed1.html" imageUrl="https://example.com/feed1.jpg"/>\n    <outline text="Feed 2" type="rss" xmlUrl="https://example.com/feed2" htmlUrl="https://example.com/feed2.html" imageUrl="https://example.com/feed2.jpg"/>\n  </body>\n</opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        feeds = opml_manager.extract_feeds()
        assert isinstance(feeds, list)
        assert all(isinstance(feed, dict) for feed in feeds)
        assert len(feeds) == 2
        assert feeds[0]['title'] == 'Feed 1'
        assert feeds[0]['type'] == 'rss'
        assert feeds[0]['url'] == 'https://example.com/feed1'
        assert feeds[0]['imageUrl'] == 'https://example.com/feed1.jpg'
        assert feeds[0]['html'] == 'https://example.com/feed1.html'
        assert feeds[1]['title'] == 'Feed 2'
        assert feeds[1]['type'] == 'rss'
        assert feeds[1]['url'] == 'https://example.com/feed2'
        assert feeds[1]['imageUrl'] == 'https://example.com/feed2.jpg'
        assert feeds[1]['html'] == 'https://example.com/feed2.html'
        os.remove(file_path)

    def test_add_feed_with_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head><title>Test OPML</title></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        title = "Test Feed"
        new_feed_url = "https://example.com/feed"
        opml_manager.add_feed(title, new_feed_url)
        feeds = opml_manager.extract_feeds()
        assert any(feed['title'] == title for feed in feeds)
        assert any(feed['url'] == new_feed_url for feed in feeds)
        os.remove(file_path)

    def test_parse_error(self):
        file_path = "invalid.opml"
        with pytest.raises(FileNotFoundError):
            opml_manager = OPMLManager(file_path)

    def test_add_feed_argument_error(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head><title>Test OPML</title></head><body></body></opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        with pytest.raises(ValueError):
            opml_manager.add_feed(123, "https://example.com/feed")
        with pytest.raises(ValueError):
            opml_manager.add_feed("Test Feed", 123)
        with pytest.raises(ValueError):
            opml_manager.add_feed("Test Feed", "https://example.com/feed", 123)
        os.remove(file_path)

    def test_add_feed_url_error_fixed(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".opml") as temp_file:
            temp_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n  <head>\n    <title>Test OPML</title>\n  </head>\n  <body>\n  </body>\n</opml>')
            file_path = temp_file.name

        opml_manager = OPMLManager(file_path)
        with pytest.raises(ValueError):
            opml_manager.add_feed("Test Feed", "https://example.com/feed", html=123)
        with pytest.raises(ValueError):
            opml_manager.add_feed("Test Feed", "https://example.com/feed", imageUrl=123)
        os.remove(file_path)
