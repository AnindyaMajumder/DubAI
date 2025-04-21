from pytubefix import YouTube
from pytubefix.cli import on_progress

def video_download(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    yt.title = "vid"

    ys = yt.streams.get_highest_resolution()
    ys.download(output_path="tempfile/")
    print("Download complete!")
    
# video_download(input("Enter the URL of the YouTube video: "))