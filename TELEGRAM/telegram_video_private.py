import requests
import os
import random

# Replace with your actual bot token and group chat ID
BOT_TOKEN = "7886846116:AAG2qFh1OO86_heKxbZY0ijltjLL5sgUBk0"
CHAT_ID = "-1002366479318"  # Make sure to include the negative sign

# Folder containing videos
VIDEO_FOLDER = "VIDEO_TO_UPLOAD"  # Change this to your actual folder name

# File to store the last sent video index
COUNTER_FILE = "counter.txt"

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

MESSAGE = [
    "✨ Stay connected with me on social media! Follow here:\n\n"
    "📸 Instagram: https://www.instagram.com/nairaa.babe/\n"
    "📘 Facebook: https://www.facebook.com/profile.php?id=61578129395953\n"
    "🧵 Threads: https://www.threads.com/@nairaa.babe\n"
]

# Telegram API endpoint for sending videos
def send_video(video_path):

    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return

    # Pick a random caption for the message
    message_text = random.choice(MESSAGE)

    payload = {
        "chat_id": CHAT_ID,
        "caption": message_text,
        "parse_mode": "HTML"  # Allows rich text formatting
    }

    # Open video and send the request
    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        response = requests.post(URL, data=payload, files=files)

    # Log the response
    print(f"📤 Sent: {video_path} | Response:", response.json())

def read_counter(counter_file):
    """Read the current counter value from the file, or initialize it."""
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read())
    return 0

def main():
   
    # Define a file to store the counter 
    video_number = read_counter(COUNTER_FILE)
    # Execute the code
    print(f"Video Number : {video_number}")

    video = f"{VIDEO_FOLDER}/video_{video_number}.mp4"

    # Send the video
    send_video(video)

if __name__ == "__main__":
    main()
