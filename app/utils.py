from pytube import YouTube
from pytube.exceptions import PytubeError


def download_youtube_stream(url):
    try:
        yt = YouTube(url, use_oauth=False)
        stream = yt.streams.get_highest_resolution().download("/web/download/")
        return stream
    except PytubeError:
        return None
