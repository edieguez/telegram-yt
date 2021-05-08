from os.path import join
from tempfile import gettempdir
import youtube_dl

# Options extracted from
# https://www.programcreek.com/python/example/98358/youtube_dl.YoutubeDL
_info_options = {
    'format': '140',
#    'writeinfojson': True,
    'continue_dl': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}


def get_video_info(video_url):
    with youtube_dl.YoutubeDL(_info_options) as ydl:
        return ydl.extract_info(video_url, download=False)


def download_audio(video_url):
    video_info = get_video_info(video_url)
    output_filename = f'{join(gettempdir(), video_info["id"])}'

    audio_options = {
        'outtmpl': output_filename,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with youtube_dl.YoutubeDL(audio_options) as ydl:
        ydl.download([video_url])

    return open(f'{output_filename}.mp3', 'rb'), video_info['title']
