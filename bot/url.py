import urllib.parse as urlparse
from urllib.parse import urlencode
import hashlib
from config import Config
cfg = Config()

class Web:
    def __init__(self, folder):
        self.__folder = hashlib.sha256(folder.encode('utf8')).hexdigest()

        params = {
        'folder': self.__folder
        }

        url_parts = list(urlparse.urlparse(cfg.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query) 
        self.url = urlparse.urlunparse(url_parts)