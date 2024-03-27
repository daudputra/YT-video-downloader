import tkinter as tk
import requests
import pytube
import re
from tkinter import filedialog
from tqdm import tqdm

# <===Can't download videos that require logging into an account===>

def video_download(urls, save_path):
    for url in urls:
        try:

            yt = pytube.YouTube(url)
            streams = yt.streams.filter(progressive=True, file_extension='mp4')
            high_res_stream = yt.streams.get_highest_resolution()
            file_size = high_res_stream.filesize
            video_filename = high_res_stream.default_filename.replace('/', '')

            response = requests.get(high_res_stream.url, stream=True)

            with open(f'{save_path}/{video_filename}.mp4', 'wb') as f:

                short_title = yt.title[:40]+'...' if len(yt.title) > 30 else yt.title

                with tqdm(total=file_size, unit='B', unit_scale=True,  desc=f'Downloading {short_title}') as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            print(f'Video from {url} successfully downloaded!')

        except Exception as e:
            print(e)

        except KeyboardInterrupt:
            print('Process stopped by user')


def open_file_dialog():
    file_path = filedialog.askdirectory()
    if file_path:
        print(f'Selected Folder: {file_path}')

    return file_path

def validate_url_video(urls):

    youtube_regex = (
    r'(https?://)?(www\.)?'
    '(youtube|youtu|youtube-nocookie)\\.(com|be)/'
    '(watch\\?v=|embed/|v/|.+\\?v=)?([^&=%\\?]{11})')

    match = re.search(youtube_regex, urls)

    return bool(match)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    print('<---Use coma to separate multiple URLs--->')
    video_urls = input('Enter the video URL: ')
    video_url = video_urls.split(',')

    save_path = open_file_dialog()

    if save_path:
        if validate_url_video(video_urls):
            video_download(video_url, save_path)
        else:
            print('Video URL is not valid')
    else:
        print('No path selected')