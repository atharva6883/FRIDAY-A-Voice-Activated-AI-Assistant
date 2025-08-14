import os
import webbrowser
import openai  # Ensure you have installed the OpenAI library
import speech_recognition as sr
import pyttsx3
import datetime
import smtplib
import pyautogui
import time
import random
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 230)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Set to female voice like FRIDAY

# Command history and task list
command_history = []
task_list = []

# Global variables for the assistant state
timer = None

def speak(text):
    print(f"FRIDAY: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source: 
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You: {command}")
        command_history.append(command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return ""

def open_folder(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Get Desktop path
    folder_path = os.path.join(desktop_path, folder_name)  # Construct full folder path
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        os.startfile(folder_path)
        print(f"Opening folder: {folder_path}")
    else:
        print("That folder does not exist on the Desktop. Please check the name.")


def close_window():
    pyautogui.hotkey('alt', 'f4')
    speak("Closed the current window.")

def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Here are the search results for {query}.")

def search_you_tube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    speak(f"Here are the search results for {query}.")

def chatgpt_search(query):
    webbrowser.open(f"https://chat.openai.com/?q={query}")
    speak(f"Searching on ChatGPT for {query}.")

def gemini_search(query):
    webbrowser.open(f"https://gemini.google.com/?q={query}")
    speak(f"Searching on Gemini for {query}.")

def add_task(task):
    task_list.append(task)
    speak(f"Added {task} to your task list.")

def show_tasks():
    if task_list:
        speak("Here are your tasks.")
        for i, task in enumerate(task_list, start=1):
            speak(f"Task {i}: {task}")
    else:
        speak("You have no tasks.")

def show_history():
    if command_history:
        speak("Here is your command history.")
        for i, cmd in enumerate(command_history[-5:], start=1):
            speak(f"Command {i}: {cmd}")
    else:
        speak("No commands in history.")

def send_email(recipient, subject, body):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server.sendmail(sender_email, recipient, msg.as_string())
    server.quit()
    speak(f"Email sent to {recipient}.")

def check_weather(city):
    # Use a weather API like OpenWeatherMap for real-time data
    api_key = "7e8ba36a83f8c1d57d28cdd854e5a4ae"  # You can get this from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data.get("cod") != "404" and "main" in data:  # Check if 'main' is in data
        main = data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather_description = data["weather"][0]["description"]
        speak(f"The weather in {city} is {weather_description} with a temperature of {temperature}°C and humidity of {humidity}%.")
    else:
        speak("City not found. Please check the name and try again.")

def you_tube():
    speak("opening youtube")
    webbrowser.open("https://www.youtube.com/")


def play_music(song_name):
    #  This can open your default music player or any music file
    music_folder = os.path.join(os.path.expanduser("~"), "Music")
    music_file = os.path.join(music_folder, f"{song_name}.mp3")
    
    if os.path.exists(music_file):
        os.startfile(music_file)
        speak(f"Playing {song_name}.")
    else:
        speak(f"Sorry, I couldn't find {song_name} in your music folder.")
def like():
    songs = random.randint(1,6)
    if songs == 1:
            webbrowser.open("https://www.youtube.com/watch?v=6d5SS0gS5bU&list=RD6d5SS0gS5bU&start_radio=1")
    elif songs == 2:
            webbrowser.open("https://www.youtube.com/watch?v=BsqrmY91nUQ")
    elif songs == 3:
            webbrowser.open("https://www.youtube.com/watch?v=BcSejVIxB0E")
    elif songs == 4:
            webbrowser.open("https://www.youtube.com/watch?v=hoNb6HuNmU0")
    elif songs == 5:
            webbrowser.open("https://www.youtube.com/watch?v=qfdShSZZxlg&list=RDEMmiIXlBaJCp9HDHTjh2SwtA&start_radio=1&rv=hoNb6HuNmU0")
    elif songs == 6:
            webbrowser.open("https://www.youtube.com/watch?v=lbCRtrrMvSw")


def chat_with_ai(user_input):
    """Chatbot using OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                      {"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "I'm sorry, but I couldn't process that request."
    

def set_timer(seconds):
    global timer
    if timer:
        speak("Timer is already set.")
        return
    timer = time.time() + seconds
    speak(f"Timer set for {seconds} seconds.")

def check_timer():
    global timer
    if timer:
        remaining_time = int(timer - time.time())
        if remaining_time <= 0:
            speak("The timer is up!")
            timer = None
        else:
            speak(f"Time remaining: {remaining_time} seconds.")
    else:
        speak("No timer is currently set.")

def shutdown():
    speak("Shutting down. Goodbye!")
    exit()

def main():
    speak("welcome sir!, How can i help you?")
    while True:
        command = listen()
        
        if "shutdown" in command or "go and sleep" in command:
            shutdown()
        
        if "open folder" in command:
            path = command.replace("open folder", "").strip()
            open_folder(path)
        if "open youtube" in command:
            you_tube()

        elif "close this window" in command:
            close_window()

        elif "search" in command:
            query = command.replace("search ", "").strip()
            google_search(query)

        elif "search on chatgpt" in command:
            query = command.replace("search on chatgpt", "").strip()
            chatgpt_search(query)

        elif "search on gemini" in command:
            query = command.replace("search on gemini", "").strip()
            gemini_search(query)

        elif "add task" in command:
            task = command.replace("add task", "").strip()
            add_task(task)

        elif "show tasks" in command:
            show_tasks()

        elif "show history" in command:
            show_history()

        elif "send email" in command:
            speak("To whom would you like to send an email?")
            recipient = listen()
            speak("What is the subject?")
            subject = listen()
            speak("What is the body of the email?")
            body = listen()
            send_email(recipient, subject, body)

        elif "tell weather" in command:
            speak("Which city would you like to check the weather for?")
            city = listen()
            check_weather(city)

        elif "make me happy" in command:
            like()

        elif "play music" in command:
            speak("What song would you like to play?")
            song_name = listen()
            play_music(song_name)

        elif "friday set timer" in command:
            seconds = int(command.split(" ")[-2])  # Assuming user says "set timer 10 minutes"
            set_timer(seconds)

        elif "friday check timer" in command:
            check_timer()
        elif "friday" in command:
            speak("yes sir")

        # elif "search on you tube for" in command:
        #     query = command.replace("search on youtube for", "").strip()
        #     search_you_tube(query)

        elif "let's talk" in command:
            speak("Sure! What would you like to talk about?")
            while True:
                user_message = listen()
                if "exit chat" in user_message:
                    speak("Exiting chat mode.")
                    break
                response = chat_with_ai(user_message)
                speak(response)

        elif "exit" in command or "quit" in command:
            # speak("Goodbye! Have a great day.")
                exit = random.randint(1,4)
                if exit == 1:
                    speak("Goodbye! Have a great day.")
                    break
                elif exit == 2:
                    speak("See you soon! Let me know whenever you need help.")
                    break
                elif exit == 3:
                    speak("Hope you have a fantastic day! See you soon.")
                    break
                elif exit == 4:
                    speak("Powering down. Until next time!")
                    break
        # else:
        #     query = command
        #     google_search(query)
if __name__ == "__main__":
    main()