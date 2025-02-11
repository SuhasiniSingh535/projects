import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia  # Make sure pyaudio is installed (pip install pyaudio)
import os
import cv2
import time


engine = pyttsx3.init('sapi5')  # Initialize pyttsx3 with the Windows voice engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio): # speak the string
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("hii I am Jarvis! How may I help you?")

def takeCommand():
    # Get user input from microphone
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Adjust pause threshold to avoid recognizing background noise
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Sorry, could you please repeat that?")
        return "None"
    return query

def open_camera():
      # Open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("Sorry, I cannot access the camera.")
        return

    speak("Opening camera...")
    ret, frame = cap.read()

    if ret:
        # Display the frame in a window
        cv2.imshow('Camera', frame)
        
        # Save the captured image
        img_name = "captured_photo.png"
        cv2.imwrite(img_name, frame)
        speak(f"Photo captured and saved as {img_name}.")
        print(f"Photo saved as {img_name}.")

        # Wait for any key to close the window
        cv2.waitKey(0)

    # Release the camera and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def set_reminder(reminder_message, reminder_time):
    # Normalize input to convert "a.m." and "p.m." to "AM" and "PM"
    reminder_time = reminder_time.replace("a.m.", "AM").replace("p.m.", "PM")
    
    try:
        # Try to parse time in 12-hour format with AM/PM
        reminder_time_obj = datetime.datetime.strptime(reminder_time, "%I:%M %p")
    except ValueError:
        try:
            # If that fails, try 24-hour format
            reminder_time_obj = datetime.datetime.strptime(reminder_time, "%H:%M")
        except ValueError:
            speak("Sorry, I couldn't understand the time format. Please try again.")
            return
    
    current_time = datetime.datetime.now()

    # If the reminder is for a time later today, keep it.
    # Otherwise, if the time has already passed today, set it for the next day.
    if reminder_time_obj.time() <= current_time.time():
        reminder_time_obj = reminder_time_obj + datetime.timedelta(days=1)

    speak(f"Reminder set for {reminder_time}. I will remind you to {reminder_message}.")
    
    while True:
        current_time = datetime.datetime.now()
        if current_time >= reminder_time_obj:
            speak(f"It's time to {reminder_message}!")
            break
        # Check the time every minute (60 seconds) to avoid high CPU usage.
        time.sleep(60)
        
    

if __name__ == "__main__":
    wishme()
    # while True:
    if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
 
        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open spotify' in query:
            webbrowser.open("spotify.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'C:\\songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))

        elif 'the time ' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'open camera' in query:
             open_camera()

        elif 'set reminder' in query:
             speak("What would you like to be reminded about?")
        reminder_message = takeCommand().lower()
    
        speak("At what time should I remind you? Please say the time in the format HH:MM, like 2:30 PM or 14:30.")
        reminder_time = takeCommand().lower()
    
    set_reminder(reminder_message, reminder_time)
       

          
