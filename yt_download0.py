from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "hhttps://www.youtube.com/watch?v=XALBGkjkUPQ"
yt = YouTube(url, on_progress_callback=on_progress)
yt.title = "vid"

ys = yt.streams.get_highest_resolution()
ys.download(output_path="temfile/")
print("Download complete!")