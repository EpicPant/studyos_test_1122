from pytubefix import YouTube
from pytubefix.cli import on_progress
import io


def download_audio(url):
    #print('start')
    yt = YouTube(url, on_progress_callback=on_progress)
    audio_stream = yt.streams.get_audio_only()
    # Create a BytesIO buffer
    buffer = io.BytesIO()
    # Download the audio into the buffer
    audio_stream.stream_to_buffer(buffer)
    # Seek to the beginning of the buffer
    buffer.seek(0)
    return buffer
