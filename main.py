import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pywhatkit
import google.generativeai as genai
import os

os.environ['GOOGLE_API_KEY']="AIzaSyBNLi9jJ6XiX55zp_EGJvnCINB9IZeqrEU"
engine = pyttsx3.init()
newsapi = "8ee7df20a3e54f8193646540c46e5103"
url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=8ee7df20a3e54f8193646540c46e5103"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# for speaking by jarvis
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Process the command
def process(cmd):
    cmd = cmd.lower()
    print(cmd)
    c = cmd.split(" ")[1]
    song = cmd.split(" ")[1] 
    # print(c)
    if "open" in cmd:
        webbrowser.open(f"https://{c}.com")

    elif "talk" in cmd and "news" in cmd:
        r= requests.get(url)
        # Check if the request was successful
        if r.status_code == 200:
            data = r.json()
    
            # Extract the headlines
            headlines = [article['title'] for article in data['articles']]
            
            # Print each headline
            for i, headline in enumerate(headlines, 1):
                speak(f"{i}. {headline}")
        else:
            speak(f"Failed to fetch news: {r.status_code}")

    elif "play" in cmd or "song" in cmd:
        song = cmd.replace('play','')
        pywhatkit.playonyt(song)

    else:     
        response = model.generate_content(cmd)
        speak(response.text)



"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female  0 for male

""" RATE"""
engine.setProperty('rate', 150)     # setting up new voice rate

if __name__=="__main__":

    speak("Hello,I am Jarvis. How can I help you today?")

    while True:
        r=sr.Recognizer()
        print("Talk...")
        try:
            with sr.Microphone() as source:

                #  Recognizition
                audio_text = r.listen(source, timeout =2 ,phrase_time_limit=2)
                text = r.recognize_google(audio_text)
                print("Recognizing...")
                print("You said: ", text)

                # using google speech recognition
                word = r.recognize_google(audio_text)
                if(word.lower()=="jarvis"):
                    speak("Yes, how can I assist?")
                # Listening command
                    with sr.Microphone() as source:
                        print("Listening...")               
                        audio_text = r.listen(source, timeout =2 ,phrase_time_limit=4)
                        command = r.recognize_google(audio_text)

                # Execute the command
                        process(command)

        except:
            print("Sorry, I did not get response")