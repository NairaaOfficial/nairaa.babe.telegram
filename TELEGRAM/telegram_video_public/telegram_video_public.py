import requests
import os
import random
import urllib.parse
import http.client

NAIRAGRAM_PUBLIC_BOT_TOKEN = os.environ["NAIRAGRAM_PUBLIC_BOT_TOKEN"]
NAIRAGRAM_PUBLIC_CHAT_ID = os.environ["NAIRAGRAM_PUBLIC_CHAT_ID"]
RENDER_BASE_VIDEO_URL = os.environ["RENDER_BASE_VIDEO_URL"]

URL = f"https://api.telegram.org/bot{NAIRAGRAM_PUBLIC_BOT_TOKEN}/sendVideo"

MESSAGE = [
    "✨ Stay connected with me on social media! Follow here:\n\n"
    "📸 Instagram: https://www.instagram.com/nairaa.babe/\n"
    "📘 Facebook: https://www.facebook.com/profile.php?id=61578129395953\n"
    "🧵 Threads: https://www.threads.com/@nairaa.babe\n"
]

# Telegram API endpoint for sending videos
def send_video(video_path):

    # Pick a random caption for the message
    message_text = random.choice(MESSAGE)

    payload = {
        "chat_id": NAIRAGRAM_PUBLIC_CHAT_ID,
        "caption": message_text,
        "parse_mode": "HTML"
    }

    # If input is an HTTP(S) URL, send as string (Telegram will fetch it)
    if isinstance(video_path, str) and (video_path.startswith("http://") or video_path.startswith("https://")):
        payload["video"] = video_path
        response = requests.post(URL, data=payload)
        print(f"📤 Sent (URL): {video_path} | Response:", response.json())
        return

    # Otherwise, treat as local file path
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return

    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        response = requests.post(URL, data=payload, files=files)
        print(f"📤 Sent (File): {video_path} | Response:", response.json())

def read_counter(counter_file):
    """Read the current counter value from the file, or initialize it."""
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read())
    return 0

def get_video_url_for_day(counter):
    """
    Returns a valid video URL for a given day.
    Stops when a video is not found or max_attempts is reached.
    """
    
    url = f"{RENDER_BASE_VIDEO_URL}/Video_{counter}.mp4"
    parsed_url = urllib.parse.urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("HEAD", parsed_url.path)
    response = conn.getresponse()
    if response.status == 200:
        return url
    else:
        return None
    
def main():
   
    # Define a file to store the counter
    counter_file = 'counter_video_public.txt'
    counter = read_counter(counter_file)
    # Execute the code
    print(f"Counter : {counter}")

    video_url = get_video_url_for_day(counter)
    print("Video URL for the day:", video_url)

    # Send the video
    send_video(video_url)

if __name__ == "__main__":
    main()
