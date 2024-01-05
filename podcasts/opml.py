import os
import os.path
import shutil
import xml.etree.ElementTree as ET
import requests
import hashlib

"""
OPMLManager class for managing OPML files.

This class provides methods for reading, extracting, adding, removing, and saving feeds in an OPML file.
It also includes a method for updating the image associated with a feed URL.

Attributes:
    file_path (str): The path to the OPML file.
    opml_root (Element): The root element of the OPML file.

Methods:
    __init__(file_path): Initializes the OPMLManager object with the specified file path.
    read_opml(): Reads the OPML file and returns the root element.
    extract_feeds(): Extracts the feeds from the OPML file and returns a list of dictionaries.
    add_feed(title, new_feed_url, type='rss', html=None, imageUrl=None): Adds a new feed to the OPML file.
    remove_feed_by_url(feed_url): Removes a feed from the OPML file based on its URL.
    save_opml(): Saves the changes made to the OPML file.
    get_image_url(feed_url): Returns the image URL associated with a feed URL.
    update_image(url): Updates the image associated with a feed URL by caching it locally.

"""


class OPMLManager:
    """
    A class for managing OPML (Outline Processor Markup Language) files.

    Attributes:
        file_path (str): The file path of the OPML file.
        opml_root (Element): The root element of the OPML file.
    """

    class OPMLParseError(Exception):
        pass

    class CustomException(Exception):
        pass

    class ImageDownloadError(Exception):
        pass

    def __init__(self, file_path):
        """
        Initializes the OPMLManager instance with the file path of the OPML file.

        Args:
            file_path (str): The file path of the OPML file.
        """
        self.file_path = file_path
        self.opml_root = self.read_opml()

    def read_opml(self):
        """
        Reads the OPML file and returns the root element.

        Returns:
            Element: The root element of the OPML file.
        """
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            raise self.OPMLParseError(f"Error parsing OPML file: {e}")

    def extract_feeds(self):
        """
        Extracts feeds from the OPML file and returns a list of dictionaries containing feed information.

        Returns:
            list: A list of dictionaries containing feed information.
        """
        feeds = []
        for outline in self.opml_root.findall(".//outline"):
            feed = {}
            feed['title'] = outline.get('text')
            feed['type'] = outline.get('type')
            feed['url'] = outline.get('xmlUrl')
            feed['imageUrl'] = outline.get('imageUrl')
            feed['html'] = outline.get('htmlUrl')
            feeds.append(feed)
        self.feeds = feeds
        return feeds

    def add_feed(self, title, new_feed_url, type='rss', html=None, imageUrl=None):
        """
        Adds a new feed to the OPML file.

        Args:
            title (str): The title of the new feed.
            new_feed_url (str): The URL of the new feed.
            type (str, optional): The type of the new feed. Defaults to 'rss'.
            html (str, optional): The HTML URL of the new feed. Defaults to None.
            imageUrl (str, optional): The image URL of the new feed. Defaults to None.
        """
        if not isinstance(title, str):
            raise ValueError("Title must be a string.")
        if not isinstance(new_feed_url, str):
            raise ValueError("New feed URL must be a string.")
        if not isinstance(type, str):
            raise ValueError("Type must be a string.")
        if html is not None and not isinstance(html, str):
            raise ValueError("HTML URL must be a string.")
        if imageUrl is not None and not isinstance(imageUrl, str):
            raise ValueError("Image URL must be a string.")
    
        body = self.opml_root.find(".//body")
        new_feed_attributes = {"text": title, "type": type, "xmlUrl": new_feed_url}
        if html is not None:
            new_feed_attributes["htmlUrl"] = html
        if imageUrl is not None:
            new_feed_attributes["imageUrl"] = imageUrl
        new_feed = ET.Element("outline", new_feed_attributes)
        body.append(new_feed)

    def remove_feed_by_url(self, feed_url):
        """
        Removes a feed from the OPML file based on its URL.

        Args:
            feed_url (str): The URL of the feed to be removed.
        """
        body = self.opml_root.find(".//body")
        for outline in body.findall(".//outline"):
            if outline.get("xmlUrl") == feed_url:
                body.remove(outline)

    def save_opml(self):
        """
        Saves the changes made to the OPML file.
        """
        tree = ET.ElementTree(self.opml_root)
        tree.write(self.file_path)

    def get_image_url(self, feed_url):
        """
        Returns the image URL for a feed based on its URL.

        Args:
            feed_url (str): The URL of the feed.

        Returns:
            str: The image URL of the feed.
        """
        for outline in self.opml_root.findall(".//outline"):
            if outline.get("xmlUrl") == feed_url:
                return outline.get("imageUrl")
        return None

    @staticmethod
    def update_image(url, cache_directory):
        """
        Updates the image for a feed by downloading it from the provided URL and saving it locally.

        Args:
            url (str): The URL of the image.
            cache_directory (str): The directory to cache the image.
        """
        file_name = hashlib.sha256(str(url).encode()).hexdigest()
        file_path = os.path.join(cache_directory, file_name)
        cached_image = os.path.isfile(file_path)
        if cached_image is not False:
            print(cached_image)
        else:
            try:
                response = requests.get(url, stream=True)
                if response:
                    with open(file_path, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                else:
                    raise self.ImageDownloadError('Was not possible to cache the file')
            except Exception as e:
                raise self.CustomException(f"Error updating image: {e}")
