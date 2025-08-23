import requests
import os
import random

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Telegram endpoint for sending text
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def gemini_generate_text(prompt):
    """
    Uses Google Gemini API to generate text based on the input prompt.
    Returns the generated text as a string.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    params = {"key": GEMINI_API_KEY}
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "No output from Gemini API."
    else:
        return f"Error: {response.status_code} - {response.text}"

def read_caption(caption_file):
    print (caption_file)
    try:
        with open(caption_file, "r", encoding="utf-8") as file:
            caption = file.read()
        return caption
    except FileNotFoundError:
        return "Caption file not found."
    except Exception as e:
        return f"An error occurred: {e}"

def send_text(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(URL, data=payload)
    print("✅ Message sent:", response.json())

def read_prompt(prompt_file):
    print (prompt_file)
    try:
        with open(prompt_file, "r", encoding="utf-8") as file:
            prompt = file.read()
        return prompt
    except FileNotFoundError:
        return "prompt file not found."
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    # Execute the code
    prompt_file = 'TELEGRAM/prompt.txt'
    user_prompt = read_prompt(prompt_file)
    caption_part1 = gemini_generate_text(user_prompt)
    caption_file = 'TELEGRAM/caption.txt'
    caption_part2 = read_caption(caption_file)
    caption = caption_part1 + caption_part2
    print(f"Caption : {caption}")
    send_text(caption)
    
if __name__ == "__main__":
    main()