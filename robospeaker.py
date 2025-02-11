import pyttsx3

if __name__ == '__main__':
    print("Welcome to roboSpeaker 1.1. Created by Suhasini")
    while True:
        x = input("Enter what you want me to speak: ")
        if x == "q":
            # Say "bye bye" and exit
            engine.say("bye bye")
            engine.runAndWait()
            break
        # Initialize the TTS(text to speech) engine
        engine = pyttsx3.init()

        # Say the entered text
        engine.say(x)

        # Run the TTS engine
        engine.runAndWait()