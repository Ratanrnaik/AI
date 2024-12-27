import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import time
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch

# Function to search and play the first YouTube video
def play_youtube_song(song_name):
    try:
        text_to_speech(f"Searching for {song_name} on YouTube...")

        # Use youtube-search-python to search for the song
        videos_search = VideosSearch(song_name, limit=1)
        result = videos_search.result()

        # Check if the 'videos' key is in the result
        if 'result' in result:
            first_video = result['result'][0]
            video_url = first_video['link']
            text_to_speech(f"Playing the first video for {song_name} on YouTube.")
            webbrowser.open(video_url)
        else:
            text_to_speech(f"Sorry, I couldn't find a video for {song_name}.")
    except Exception as e:
        text_to_speech("An error occurred while searching for the video.")
        print(f"Error: {e}")

# Text-to-speech function
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to take voice command
def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error with the Speech Recognition service: {e}")
        return ""

# Function to search Google and display the result
def search_google(query):
    text_to_speech("Searching Google...")
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

    # Perform a GET request to Google search
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title and snippet of the first search result
    first_result = soup.find('h3')
    if first_result:
        result_text = first_result.text
        text_to_speech(f"Here is the result: {result_text}")
    else:
        text_to_speech("Sorry, I couldn't find any relevant results.")

# Main logic
if __name__ == "__main__":
    text_to_speech("Hello, I am Jarvis AI. How can I help you?")
    while True:
        query = takeCommand()

        # Check for YouTube song request
        if "play" in query and "song" in query:
            song_name = query.replace("play", "").replace("song", "").strip()
            play_youtube_song(song_name)
        
        # Fetch current time
        elif "what's the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            text_to_speech(f"Sir, the time is {hour} hour {minute} minutes.")

        # Exit command
        elif "exit" in query:
            text_to_speech("Goodbye, Ratan.")
            exit()

        # Fallback search on Google
        elif query:
            search_google(query)
