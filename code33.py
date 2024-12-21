import speech_recognition as sr
import pyttsx3
import requests
import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture audio input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("How can I assist you?")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            speak("Sorry, I didn't catch that. Can you repeat?")
            return None
        except sr.RequestError:
            print("Speech Recognition service is unavailable.")
            speak("I'm having trouble connecting. Please try again later.")
            return None

def get_weather(city):
    """Fetch weather details for a city using OpenWeatherMap API."""
    api_key = "your_openweather_api_key"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
    except requests.exceptions.RequestException:
        speak("Sorry, I couldn't fetch the weather details. Please check the city name.")

def read_news():
    """Fetch and read top news headlines."""
    news_api_key = "your_news_api_key"  # Replace with your API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])[:5]
        if articles:
            speak("Here are the top news headlines:")
            for i, article in enumerate(articles, 1):
                speak(f"Headline {i}: {article['title']}")
        else:
            speak("No news articles are available at the moment.")
    except requests.exceptions.RequestException:
        speak("Sorry, I couldn't fetch the news at the moment.")

def set_reminder(reminder):
    """Set a reminder."""
    with open("reminders.txt", "a") as file:
        file.write(f"{datetime.datetime.now()}: {reminder}\n")
    speak(f"Reminder set: {reminder}")

def personal_assistant():
    """Main function for the personal assistant."""
    while True:
        command = listen()
        if not command:
            continue

        if "weather" in command:
            speak("Which city's weather would you like to know?")
            city = listen()
            if city:
                get_weather(city)

        elif "news" in command:
            read_news()

        elif "set a reminder" in command:
            speak("What would you like me to remind you about?")
            reminder = listen()
            if reminder:
                set_reminder(reminder)

        elif "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("I'm sorry, I didn't understand that command. Please try again.")

if __name__ == "__main__":
    speak("Initializing personal assistant...")
    personal_assistant()
