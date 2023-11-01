import yt_dlp
import Data
import urllib3
import time

data = Data.BaseData()   
LANG = "en"

info_options = { 
    "cache": False, 
    "quiet": True, 
    "dump_single_json": True, 
    "writesubtitles": True, 
    "writeautomaticsub": True, 
    "subtitleslangs": LANG, 
    "skip_download": True, 
    "verbose": True, 
    "ignoreerrors": True, 
}

id_options = { 
    "cache": False, 
    "quiet": True, 
    "dump_single_json": True, 
    "forceid": True, 
    "writeinfojson": True, 
    "extract_flat": True, 
    "skip_download": True, 
    "ignoreerrors": True, 
}

def get_info(url):
  ydl = yt_dlp.YoutubeDL(info_options)
  info = ydl.extract_info(url, download=False)
  return info

def get_id(channel_url):
  ydl = yt_dlp.YoutubeDL(id_options)
  info = ydl.extract_info(channel_url, download=False)
  return info

def extract_subtitles(info):

    if "requested_subtitles" in info and LANG in info["requested_subtitles"]:
        subtitle = info["requested_subtitles"]

    elif "subtitle" in info and LANG in info["subtitle"]:
        subtitle = info["subtitle"]
    
    elif "automatic_captions" in info and LANG in info["automatic_captions"]:
        subtitle = info["automatic_captions"]
        for sub in subtitle[LANG]:
            if sub["ext"] == "vtt":
                return sub["url"]
    
    if LANG in subtitle:
        if type(subtitle) is list:
            for sub in subtitle[LANG]:
                if sub["ext"] == "vtt":
                    return sub["url"]

        else:
            return subtitle[LANG]["url"]

    else:
        return False

def manage_info(info):

    subtitle = extract_subtitles(info)
    
    if subtitle:
        http = urllib3.PoolManager()
        response = http.request('GET', f"{subtitle}")        
        text = response.data.decode('utf-8')
        
        try:
            data.add_text(text, info['id'], info['channel'], info['upload_date'], info['duration'], info['view_count'])
        except Exception as e:
           print(f"ERROR: {e}")
           print(f"Was not possible to manage {subtitle}")
    else:
       print(f"info {subtitle} has not a subtitle")

def updatechannelvideos(channel_url):
    channel_info = get_id(channel_url)
    channel_name = channel_info['channel']
    if channel_name not in data.videolist:
        data.videolist[channel_name] = {}

    videolist = data.videolist[channel_name]
    current = [key for key in videolist]
    queue = []
    info = channel_info['entries']
    for part in info:
       video = part["url"]
       address = video.replace("https://www.youtube.com/watch?v=", "")
       if address not in current:
            queue.append(video)

    while len(queue) > 0:
        current = queue.pop()
        try:
            current_info = get_info(current)
            manage_info(current_info)

        except Exception as e:
           print(f"error on uploading {current}")
           print(f"ERROR: {e}")

    data.save_data()

 
def find_videos(query):
   return data.search(query)

def video_details(name):
    return data.video_details(name)
