import pyttsx3
import speech_recognition as sr
import time
import os
import subprocess
import re
import threading
import google.generativeai as genai


#wikipedia.set_lang("en")  
API_KEY = "AIzaSyBbWXlcGVvMTZ0F7IVhCijg5d0RGXM7vVY"
genai.configure(api_key = API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")



engine = pyttsx3.init()
sleep_mode = False
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0) #max volume




def speak(text):
    print(f"🤖 :: {text}")  # Debug print
    engine.say(text)
    engine.runAndWait()
    time.sleep(1.5)
    
'''def get_cleaned_prompt(prompt):
    prompt = prompt.lower()
    prompt = re.sub(r"\b(what is|who is|where is|tell me about|define|explain|can you explain|do you know what is|do u know)\b", "", prompt)                         
    return prompt.strip()'''

def set_timer(commend):
    global sleep_mode


    pattern = r"(\d+)\s*(second|seconds|minute|minutes)"
    match = re.search(pattern, commend.lower())
    if match:
        val = int(match.group(1))
        unit = match.group(2)
        unit = unit.lower()
        if unit in ['minute', 'minutes']:
            seconds = val * 60
        elif unit in ['second', 'seconds']:
            seconds = val
        else:
            return " Invalid time unit "
        speak(f"Timer set for {val}{unit}")
        #print(f"Timer set for {val} {unit}")

        def countdown():
            time.sleep(seconds)
            engine.say("Time's up!")
            engine.runAndWait()

        threading.Thread(target=countdown).start()
        speak("Timer started.")
        #print("Timer started.")
        
    else:
        speak("I could not understand the timer command. Please specify the time in seconds or minutes.")
        #print("I could not understand the timer command. Please specify the time in seconds or minutes.")
           

def close_app(prompt):
    app_keywords = {
        "calculator": "calculator",
        "notepad": "notepad.exe",
        "command prompt": "cmd.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "paint": "mspaint.exe",
        "camera": "WindowsCamera.exe",
        "vs code": "Code.exe",
        "visual studio code": "Code.exe",
    }


def get_smart_response(prompt):
    prompt = prompt.lower()
    #calculator
    if "open calculator" in prompt:
        if os.name == 'nt':  # Windows
            os.system("calc")
            return "Opening calculator."
    #notepad 
    elif "open notepad" in prompt:
        os.system("notepad")
        return "Opening Notepad."
    #ms paint
    elif "open paint" in prompt or "open ms paint" in prompt:
        if os.name == 'nt':
            os.system("mspaint")
            return "Opening MS Paint."
    #command prompt
    elif "open command prompt" in prompt.lower() or "open cmd" in prompt.lower():
        if os.name == 'nt':
           os.system("start cmd")
           return "Opening Command Prompt."

    #control panel
    elif "open command prompt" in prompt or "open cmd" in prompt:
        if os.name == 'nt':
           os.system("start cmd")
           return "Opening Command Prompt."

    #file explorer
    elif "open file explorer" in prompt or "open my computer" in prompt:    
        if os.name == 'nt':
            os.system("explorer")
            return "Opening File Explorer."     
    #camera
    elif "open camera" in prompt or "open webcam" in prompt:
        if os.name == 'nt':
            try:
                subprocess.run("start microsoft.windows.camera:", shell=True)
                return "Opening Camera."
            except Exception as e:
                print(f"Error opening camera: {e}")
                return "Failed to open camera."
    #excel
    elif "open excel" in prompt:
        if os.name == 'nt':
            try:
                os.system("start excel")
                return "Opening Excel."
            except Exception as e:
                print(f"Error opening Excel: {e}")
                return "Failed to open Excel."  
    #word
    elif "open word" in prompt or "open microsoft word" in prompt:
        if os.name == 'nt':
            try:
                os.system("start winword")
                return "Opening Microsoft Word."
            except Exception as e:
                print(f"Error opening Word: {e}")
                return "Failed to open Word." 
    #powerpoint
    elif "open powerpoint" in prompt or "open ms powerpoint" in prompt:         
        if os.name == 'nt':
            try:
                os.system("start powerpnt")
                return "Opening Microsoft PowerPoint."
            except Exception as e:
                print(f"Error opening PowerPoint: {e}")
                return "Failed to open PowerPoint."  
    elif "open vs code " in prompt or "open visual studio code" in prompt:         
        if os.name == 'nt':
            try:
                os.system("start code")
                return "Opening Visual Studio Code."
            except Exception as e:
                print(f"Error opening VS Code: {e}")
                return "Failed to open Visual Studio Code." 

    elif "set timer" in prompt or "start timer" in prompt:
        return set_timer(prompt)
    
    elif "close" in prompt:
        return close_app(prompt)


        # Handle basic math calculation using speech
    elif "calculate" in prompt or "what is" in prompt:
        # Remove unwanted words
        calc_prompt = prompt.replace("calculate", "").replace("what is", "")
        
        # Replace spoken operators with symbols
        calc_prompt = calc_prompt.replace("plus", "+")
        calc_prompt = calc_prompt.replace("minus", "-")
        calc_prompt = calc_prompt.replace("times", "*")
        calc_prompt = calc_prompt.replace("multiplied by", "*")
        calc_prompt = calc_prompt.replace("x", "*")
        calc_prompt = calc_prompt.replace("divided by", "/")
        calc_prompt = calc_prompt.replace("by", "/")
        
        # Remove extra spaces
        calc_prompt = calc_prompt.strip()
        
        try:
            result = eval(calc_prompt)
            return f"The result is {result}"
        except Exception as e:
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"
    
    return ask_gemini(prompt)


def listen_to_user():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 800  # Default value, can be adjusted based on environment

    with sr.Microphone() as source:
    

        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("👂 :: Listening...")
        
        try:
            audio = recognizer.listen(source, timeout = 5, phrase_time_limit = 12)
            print("🎧 Audio captured, processing...")
            
            
        except sr.WaitTimeoutError:   
            print("silence detected")
            speak("no input detected. ending session.")
            time.sleep(4)
            #engine.runAndWait()
            return "exit" 
                
        
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"🧠 You said: {text}")
        return text
        
    except sr.UnknownValueError:
        print("❌ Could not understand")
        speak("Sorry, I could not understand!.")
        return None
        
    except sr.RequestError:
        print("⚠️ Google service failed.")
        speak("Speech recognition service is down.")
        return None
    
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, Gemini could not respond: {e}"    
    

def run_voice_assistant():
    global sleep_mode
    first_time = True

    while True:
        if sleep_mode:
            engine.say("sleep mode active. waiting for wake-up command...")
            print("sleep mode active. waiting for wake-up command...")
            engine.runAndWait()
            user_input = listen_to_user()

            if user_input is None:
                continue

            if "hi" in user_input or "hello" in user_input:
                engine.say("I'm back! how can I assist you?")
                sleep_mode = False
            else:
                continue 

        else:
            
            if first_time:
                engine.say("Hello! I am your voice assistant. How can I assist you today?")
                print("🤖 :: Hello! I am your voice assistant. How can I assist you today?")
                first_time = False
            else:
                engine.say("Do you want to ask anything else?")
                print("🤖 :: Do you want to ask anything else?")
                time.sleep(1)

            user_input = listen_to_user()

            if user_input is None:
                continue

        if user_input in ["exit", "quit",'stop']:
          #print("👋 Ending session. Goodbye!")
          speak("Ending session.")
          break

        if user_input == "exit":
            break


        reply = get_smart_response(user_input)
        print(f"🤖 :: {reply}")
        speak(reply)

        time.sleep(1.5)
        

if __name__ == "__main__":
    print("==========================================================")
    speak("Welcome to the voice assistant!")
    time.sleep(0.5)
    print("==========================================================")
    print("This is a simple voice assistant that listens to your commands.\nYou can say 'exit' or 'quit' to stop the assistant.")
    time.sleep(0.5)
    run_voice_assistant()
    speak("Thank you for using the voice assistant!")
    print("===========================================================")
    time.sleep(3)    