# importing required libraries.
import pyttsx3 
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import requests
from pprint import pprint
import pyautogui 
import pyjokes

engine = pyttsx3.init()
voices = engine.getProperty('voices')       # getting details of current voice
engine.setProperty('voice', voices[1].id)   # For Female Voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    print(Time)
    speak("The current Time is")
    speak(Time)    

def date():
    year  = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    dates = int(datetime.datetime.now().day)
    speak("The current date is")
    print(dates)
    print(month)
    print(year)
    speak(dates)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome!")
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning Sir")
    elif hour >=12 and hour < 18:
        speak("Good Afternoon Sir")
    elif hour >=18 and hour < 24:
        speak("Good Evening Sir")
    else:
        speak("I hope you are enjoying your Night Sir")
    speak("Friday at your service. Please tell me how can i help you ")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    
    except Exception as e:
        print(e)
        print("Sorry Sir, Say that again")
        speak("Sorry Sir, Say that again")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('Senders@gmail.com', 'Password')
    server.sendmail('Senders@gmail.com', to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save('C:/Users/Amandeep/Desktop/Friday/screenshot.png')

def jokes():
    haha = pyjokes.get_joke()
    print(haha)
    speak(haha)

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        if 'the time' in query:
            time()

        if 'the date' in query:
            date()

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                to = 'Receivers@gmail.com'
                sendEmail(to, content)
                speak("Email has been sent successfully.")
            except Exception as e:
                print(e)
                speak("Sorry Sir, Unable to send the email")

        elif 'chrome' in query:
            speak("What should i search?")
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            try:
                search = takeCommand().lower()
                print('I think you said:\n' +search +'.com')
                wb.get(chrome_path).open_new_tab(search+'.com')
            except Exception as e:
                print(e)
  
        elif 'logout' in query:
            os.system("shutdown -l")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")

        elif 'how is the weather' and 'weather' in query:
            url = 'https://api.openweathermap.org/data/2.5/weather?q=<PLACE_NAME>&appid=<YOUR API KEY>'
            res = requests.get(url)
            data = res.json()
            weather = data['weather'] [0] ['main'] 
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            description = data['weather'][0]['description']
            speak('Temperature : {} degree celcius'.format(temp))
            print('Wind Speed : {} m/s'.format(wind_speed))
            print('Latitude : {}'.format(latitude))
            print('Longitude : {}'.format(longitude))
            print('Description : {}'.format(description))
            print('weather is: {} '.format(weather))
            speak('weather is : {} '.format(weather))

        elif 'open' in query:
            os.system('explorer C://{}'.format(query.replace('Open','')))

        elif 'play song' in query:
            songs_dir = 'E:/MUSICS/Hindi Fav' 
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
            
        elif 'remember' in query:
            speak("what should i remember?")
            data = takeCommand()
            speak("You said me to remember that"+data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
        elif 'do you know anything' in query:
            remember = open('data.txt', 'r')
            speak("You said me to remember that"+remember.read())

        elif 'take screenshot'in query:
            screenshot()
            speak("Screenshot Saved")

        elif 'joke' in query:
            jokes()

        elif 'who made you' in query or 'who created you' in query:
            speak("i am created by Amandeep")

        elif "how are you" in query:
            speak("I am Boombastic, How are You?")
        
        elif 'i am fine' in query or 'I am good' in query:
            speak("it is good to hear that you are fine")

        elif "search for me" in query:
            speak("What sir?")
            a = takeCommand().lower()
            print("Searching \n"+a)
            wb.open(f"https://www.google.com/search?q={a}")

        elif 'my location' in query:
            try:
                response = requests.get('https://ipinfo.io?token=<TOKEN>')
                locInfo =  response.json()
                print(30*"-")
                print(locInfo['city'])
                print(locInfo['region'])
                if locInfo['country'] == 'IN':
                    locInfo['country'] = 'India'
                print(locInfo['country'])
                speak(f"Sir, you are currently in {locInfo['city']} in {locInfo['region']}.")
                print(30*"-")
            except Exception as e:
                print("Sorry, sir. I am having issues gathering your location")

        

        elif 'offline' in query:
            speak("Shutting Down Sir")
            quit()
        
