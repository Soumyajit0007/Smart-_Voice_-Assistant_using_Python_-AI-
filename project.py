import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import webbrowser
import os
import subprocess
import pyjokes
import pyautogui

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Slow down the voice speed
rate = tts_engine.getProperty('rate')
tts_engine.setProperty('rate', rate - 50)

# Function to convert text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen to user's speech and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return "None"

# Function to greet the user
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your AI assistant. How can I help you today?")

# Function to handle the user's commands
def handle_command(command):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif 'wikipedia' in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        try:
            result = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any results for that.")
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif 'open settings' in command:
        if os.name == 'nt':  # For Windows
            subprocess.Popen(['start', 'ms-settings:'], shell=True)
        elif os.name == 'posix':  # For macOS
            subprocess.Popen(['open', '-a', 'System Preferences'])
        speak("Opening settings")
    elif 'open notepad' in command:
        if os.name == 'nt':  # For Windows
            subprocess.Popen(['notepad'])
        elif os.name == 'posix':  # For macOS
            subprocess.Popen(['open', '-a', 'TextEdit'])
        speak("Opening Notepad")
    elif 'tell me a joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
    elif 'take a screenshot' in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot taken and saved as screenshot.png")
    elif 'shutdown' in command:
        speak("Shutting down the computer")
        if os.name == 'nt':  # For Windows
            os.system("shutdown /s /t 1")
        elif os.name == 'posix':  # For macOS
            os.system("sudo shutdown -h now")
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I don't know that command.")

# Main function to run the assistant
def run_assistant():
    greet_user()
    while True:
        command = listen()
        if command != "None":
            handle_command(command)

# Run the assistant
if __name__ == "__main__":
    run_assistant()
