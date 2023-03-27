#! python3.10
# Youtube download
from pytube import YouTube
import sys, pyperclip

def confirm_command():
    if len(sys.argv) == 1:
        url = pyperclip.paste()
        get_youtube(url,resolution='default')

    elif len(sys.argv) > 1 and sys.argv[1] == 'res':
        url = pyperclip.paste()
        resolution = sys.argv[2]
        get_youtube(url,resolution)

def get_youtube(url, resolution):
    yt = YouTube(url, on_progress_callback=progress, on_complete_callback=complete)
    title = yt.title
    if resolution == 'default':
        try:
            video = yt.streams.get_highest_resolution()
            res = video.resolution
            size = f'{str(round(video.filesize/(1024*1024)))} MB'
            print(f'Video: {title} | Resolution: {res} | Filesize: {size}')
            confirm = input('Confirm download this video? Type "y" for yes.')
            if confirm == 'y':
                video.download('C:\\Users\\Scott\\Downloads',title)
            else: sys.exit()
        except Exception as error:
            print('Download error. Try again.')
    else:
        try:
            video = yt.streams.get_by_resolution(resolution=resolution)
            size = f'{str(round(video.filesize / (1024 * 1024)))} MB'
            print(f'Video: {title} | Resolution: {resolution} | Filesize: {size}')
            confirm = input('Confirm download this video? Type "y" for yes.')
            if confirm == 'y':
                video.download('C:\\Users\\Scott\\Downloads',title)
            else:
                sys.exit()
        except Exception as error:
            print('Download error. Maybe no such resolution found. Try again.')

def progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")

def complete(title):
    print(f'{title} download completed.')

if __name__ == '__main__':
    confirm_command()