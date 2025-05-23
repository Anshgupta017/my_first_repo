import os
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import requests
import pygame  
from pytube import YouTube  # For playing YouTube songs
import webbrowser  # To open YouTube links in the browser
from datetime import datetime  # For real-time date and time

# Configure Google Gemini API (replace 'your-api-key-here' with the actual API key if not using an environment variable)
gemini_api_key = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
genai.configure(api_key='get your own')

# Initialize the generative model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice to female (adjusting for a more realistic voice)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 150)  # Adjust speech rate for better clarity
engine.setProperty('volume', 1)  # Set volume to max

# Initialize Pygame for sound playback
pygame.mixer.init()

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input and convert it to text."""
    try:
        pygame.mixer.music.load('C:/Users/Piyush gupta/Downloads/beep.wav')  # Path to your beep sound file
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"Error playing sound: {e}")

    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language='en-IN')
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Could you please repeat?")
            return ""
        except sr.RequestError as e:
            speak("Sorry, I'm having trouble understanding. Please try again.")
            print(f"Error: {e}")
            return ""

def get_weather(city):
    """Get weather information for a city."""
    api_key = '29109132a19ad2547ccf5cca1abd3950'  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    if response['cod'] == 200:
        temp = response['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        return f"The current temperature in {city} is {temp:.2f} degrees Celsius."
    else:
        return "I couldn't retrieve the weather information."

def search_with_gemini(query):
    """Search using Google Gemini Generative AI (Gemini-1.5-flash)."""
    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't retrieve information from the internet."

def open_application(app_name, function=None):
    """Open specific applications or their functionalities (like open Gmail in Chrome)."""
    try:
        if 'chrome' in app_name:
            os.system("start chrome")
            speak("Opening Google Chrome.")
            if function:
                webbrowser.open(function)
                speak(f"Opening {function}.")
        elif 'notepad' in app_name:
            os.system("start notepad")
            speak("Opening Notepad.")
        elif 'word' in app_name:
            os.system("start winword")
            speak("Opening Microsoft Word.")
        elif 'whatsapp' in app_name:
            webbrowser.open("https://web.whatsapp.com")
            speak("Opening WhatsApp.")
        else:
            os.system(f"start {app_name}")
            speak(f"Opening {app_name}.")
    except Exception as e:
        speak(f"Sorry, I can't open {app_name}.")
        print(f"Error: {e}")

def play_youtube(song_name):
    """Play a song from YouTube using YouTube Data API."""
    API_KEY = 'AIzaSyAUdQiVAwSvRsagdMoI8m_4fBgLA5TW7m0'  # Replace with your actual YouTube API key
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_name}&type=video&key={API_KEY}"

    try:
        response = requests.get(search_url)
        result = response.json()

        if result['items']:
            video_id = result['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            webbrowser.open(video_url)
            speak(f"Playing {song_name} on YouTube.")
        else:
            speak(f"Sorry, I couldn't find {song_name} on YouTube.")

    except Exception as e:
        speak("Sorry, I couldn't play the song from YouTube.")
        print(f"Error: {e}")

def play_song(song_name):
    """Play a song either offline or online."""
    music_dir = "E:/bhakti songs"
    song_path = os.path.join(music_dir, f"{song_name}.mp3")

    if os.path.exists(song_path):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            speak(f"Playing {song_name} from offline storage.")
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except pygame.error as e:
            speak("Sorry, there was an error playing the song.")
            print(f"Pygame error: {e}")
    else:
        speak(f"Sorry, I couldn't find {song_name} in your offline music directory. I will try to play it online.")
        play_youtube(song_name)

def open_file(file_name):
    """Open any file format from anywhere on the system with progress percentage updates."""
    try:
        total_dirs = sum([len(dirs) for _, dirs, _ in os.walk('E:/')])  # Count total directories in E drive
        scanned_dirs = 0  # Track how many directories have been scanned

        # Search for the file in the entire system
        for root, dirs, files in os.walk('E:/'):  # You can change 'E:/' to any other root directory
            scanned_dirs += 1
            percentage_scanned = (scanned_dirs / total_dirs) * 100
            speak(f"System scan progress: {percentage_scanned:.2f}% completed.")

            for file in files:
                if file_name.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    os.startfile(file_path)  # Open the file
                    speak(f"Opening {file_name}.")
                    return
        speak(f"Sorry, I couldn't find the file named {file_name} on your system.")
    except Exception as e:
        speak(f"Sorry, there was an error opening {file_name}.")
        print(f"Error: {e}")

def process_command(command):
    """Decide if the command is a system command or a query to answer using Gemini AI."""
    if 'your name' in command:
        result = "Hello... I'm your Nivedita."

    elif 'weather' in command:
        speak("Which city do you want the weather for?")
        city = listen()
        if city:
            weather_info = get_weather(city)
            result = weather_info
        else:
            result = "Sorry, I didn't catch the city name."

    elif 'open' in command:
        if 'gmail' in command and 'chrome' in command:
            open_application('chrome', 'https://mail.google.com')
        elif 'youtube' in command and 'chrome' in command:
            open_application('chrome', 'https://www.youtube.com')
        elif 'file' in command:
            speak("Which file do you want to open?")
            file_name = listen()
            if file_name:
                open_file(file_name)
        else:
            app_name = command.replace('open', '').strip()
            open_application(app_name)
        return

    elif 'play song' in command or 'play music' in command:
        speak("Which song would you like to listen to?")
        song_name = listen()
        if song_name:
            play_song(song_name)
        return
    

    elif 'time' in command or 'date' in command:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%m-%d-%Y")
        result = f"The current time is {current_time}, and today's date is {current_date}."

    else:
        result = search_with_gemini(command)

    print(f"Nivedita's answer: {result}")
    speak(result)

def main():
    speak("Hello! I'm Nivedita. You can ask me anything.")
    
    while True:
        command = listen()

        if 'stop' in command or 'goodbye' in command:
            speak("Goodbye! Have a nice day... Feel free to ask me anything anytime.")
            break
        elif command:
            process_command(command)

if __name__ == '__main__':
    main()
