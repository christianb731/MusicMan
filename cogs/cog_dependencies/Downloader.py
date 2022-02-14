import yt_dlp
class initQueue:
    """Represents the queue as an object"""
    queue = []

    def __init__(self):
        self.queue = []

    def get_queue(self):
        return self.queue
    
    def has_next(self):
        if(len(self.queue)> 1):
            return True
        return False

    def add_song(self, url):
        self.queue.append(url)

    def next_song(self):
        if(len(self.queue) != 0):
            self.queue.pop(0)
        return self.queue


class YTDL():
    """Holds the ydl object for use, should only be created once.
    Holds all current video information in dictionary.
    Contains a queue object."""
    ydl = None
    queue = None
    video_url = None
    video_id = None
    video_length = None
    video_get = None
    video_title = None
    info_dict = {}

    def __init__(self, options):
        self.ydl = yt_dlp.YoutubeDL(options)
        self.ydl.add_info_extractor
        self.queue = initQueue()

    def download_and_get_info(self, url, search):
        """Search is a boolean that tells this method whether or not to grab the 0th entry in entry, which
        is the first url parsed from the text search."""
        self.info_dict = self.ydl.extract_info(url, download=True)
        if search:
            self.info_dict = self.info_dict.get('entries')[0]
        self.video_url = self.info_dict.get("url", None)
        self.video_id = self.info_dict.get("id", None)
        self.video_length = self.info_dict.get('duration')
        self.video_get = self.info_dict.get('outtmpl')
        self.video_title = self.info_dict.get('title')
        self.original_title = self.video_title
        # illegal characters are handled by ytdl in a unique fashion, each of these unique cases must be addressed
        for i in self.video_title:
            if i == "\"" :
                self.video_title = self.video_title.replace(i, '\'')
            elif i == ":":
                self.video_title = self.video_title.replace(i,' -')
            elif i =="|":
                self.video_title = self.video_title.replace(i,'_')
            elif i =="?" or i == "/" or i== "*" or i == "\\":
                self.video_title = self.video_title.replace(i,'')
        return self.info_dict

