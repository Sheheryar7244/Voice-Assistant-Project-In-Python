import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import threading

# ---------------- Voice Engine ----------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- Greeting ----------------
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I help you?")

# ---------------- Voice Input ----------------
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except:
        speak("Sorry, I didn't catch that.")
        return "none"
    return query.lower()

# ---------------- Command Processing ----------------
def process_command(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        speak(result)

    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")

    elif 'open google' in query:
        webbrowser.open("https://google.com")

    elif 'play' in query:
        song = query.replace('play', '')
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'time' in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time}")

    elif 'date' in query:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")

    elif 'exit' in query or 'stop' in query:
        speak("Goodbye!")
        exit()

# ---------------- Main Loop ----------------
def run_jarvis():
    wish_me()
    while True:
        query = take_command()
        if query != "none":
            process_command(query)

# ---------------- Wake Word ----------------
def wake_word():
    while True:
        query = take_command()
        if "jarvis" in query:
            speak("Yes sir?")
            run_jarvis()

# Run assistant in background thread
thread = threading.Thread(target=wake_word)
thread.start()