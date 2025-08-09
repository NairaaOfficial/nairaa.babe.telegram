import requests
import os
import time
import random
import urllib.parse
import http.client

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RENDER_BASE_IMAGE_URL = os.getenv("RENDER_BASE_IMAGE_URL")

# Telegram API endpoint for sending photos
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

def send_image(image_url, counter):
    payload = {
        "chat_id": CHAT_ID,
        "caption": f"{counter}",
        "parse_mode": "HTML",
        "photo": image_url  # Send image directly from URL
    }

    response = requests.post(URL, data=payload)
    print(f"📤 Sent: Response:", response.json())

    # Optional: Prevent hitting rate limits
    time.sleep(2)  # adjust as needed

def get_image_urls_for_day(counter, max_attempts=20):
    """
    Returns a list of valid image URLs for a given day.
    Stops when an image is not found or max_attempts is reached.
    """
    urls = []
    for idx in range(1, max_attempts + 1):
        url = f"{RENDER_BASE_IMAGE_URL}/{counter}_{idx}.png"
        parsed_url = urllib.parse.urlparse(url)
        conn = http.client.HTTPSConnection(parsed_url.netloc)
        conn.request("HEAD", parsed_url.path)
        response = conn.getresponse()
        if response.status == 200:
            urls.append(url)
        else:
            break
    return urls

def read_counter(counter_file):
    """Read the current counter value from the file, or initialize it."""
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read())
    return 0

def main():
    # Define a file to store the counter
    counter_file = 'counter.txt'
    counter = read_counter(counter_file)
    # Execute the code
    print(f"Counter : {counter}")

    image_urls = get_image_urls_for_day(counter)
    print("Image URLs for the day:", image_urls)

    for image_url in image_urls:
        send_image(image_url, counter)

if __name__ == "__main__":
    main()