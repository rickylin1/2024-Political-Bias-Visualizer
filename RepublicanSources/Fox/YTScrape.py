import yt_dlp as youtube_dl

def get_mp3_url(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # only keep the audio
        'audioformat': 'mp3',  # convert to mp3
        'outtmpl': '%(id)s.%(ext)s',  # name the file the ID of the video
        'noplaylist': True,  # download only single song, not playlist
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_url = info_dict['url']
        return audio_url
