from tkinter import *
from gtts import gTTS
import os
import re
import webbrowser
import random
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
import wikipedia
import pyowm
import  datetime
import sys
from time import strftime


def my_command():
    global command1
    global c2
    global c3
    global c4
    global c5
    global c6
    command = command1.get()
    str1 = c2.get()
    str2 = c3.get()
    str3 = c4.get()
    str4 = c5.get()
    str5 = c6.get()
    assistant(command, str1, str2, str3, str4, str5)
def speak(msg):
    for lines in msg.splitlines():
        tts = gTTS(text=lines , lang="en-uk", slow=False)
        tts.save("output.mp3")
        os.system("start output.mp3")

def assistant(command, str1, str2, str3, str4, str5):
    error_msgs = ["I don't know what you mean",
                  "Please repeat yourself",
                  "Incorrect command",
                  "I cannot do what you ask"
                  ]
    if "open website" in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print("The domain is {}".format(domain))
            website_url = 'https://' + str(domain)
            webbrowser.open(website_url)
            speak("The website you requested has been opened")
        else:
            pass
    elif "email" in command:
        #speak("What is the subject?")
        subject = str1
        #speak("Who is the recipient?")
        recipient = str2
        #speak("What do you want to say?")
        message = str3
        content = 'Subject: {}\n\n{}'.format(subject, message)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        #speak("Enter your id")
        user_id = str4
        #speak("Enter Password")
        user_pwrd = str5
        mail.login(user_id, user_pwrd)
        mail.sendmail(user_id, recipient, content)
        mail.close()
        speak("Email has been sent.")

    elif "google search" in command:
        reg_ex = re.search('google search (.*)', command)
        query = command.split("search", 1)[1]
        website_url = "https://www.google.com/"
        if reg_ex:
            domain = reg_ex.group(1)
            url = domain + "r/" + str(domain)
        driver = webdriver.Firefox(executable_path=r'C:\Users\hp\PycharmProjects\geckodriver')
        driver.get(website_url)
        search = driver.find_element_by_name("q")
        search.send_keys(str(query))
        search.send_keys(Keys.RETURN)
    elif "youtube" in command:
        reg_ex = re.search("youtube (.+)", command)
        if reg_ex:
            domain = command.split("youtube", 1)[1]
            query = urllib.parse.urlencode({"search query": domain})
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + str(query))
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html.read().decode())
            webbrowser.open("https://www.youtube.com/watch?v={}".format(search_results[0]))
            speak("The requested video is being played.")
            pass
    elif "wikipedia" in command:
        reg_ex = re.search("wikipedia (.*)", command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                search = wikipedia.page(topic)
                a = str(search.content[:500].encode('utf-8'))
                blank.insert(0, a[1:])
                speak(a[1:])
        except Exception as e:
            speak(e)

    elif "weather" in command:
        reg_ex = re.search("weather (.*)", command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = pyowm.OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature()
            temp = round(x["temp"] - 273.15, 2)
            max_temp = round(x["temp_max"] - 273.15, 2)
            min_temp = round(x["temp_min"] - 273.15, 2)
            f=("{} currently has a temperature of {}. The expected maximum temperature is {} and the minimum"
                  "temperature is {}. The city is currently experiencing {}".format(city, temp, max_temp, min_temp, k))
            speak(f)
            blank.insert(0, f)
    elif "time" in command:
        current_time = datetime.datetime.now()
        speak("The current time is {} hours and {} minutes".format(current_time.hour, current_time.minute))
    elif "shutdown" in command:
        speak("Until next time!")
        sys.exit()
    elif "Hello" in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            speak("Good Morning. Project Officium at your service.")
        elif day_time >= 12 and day_time < 18:
            speak("Good afternoon. Project Officium at your service.")
        else:
            speak("Good evening. Project Officium at your service.")
    else:
        error_msg = random.choice(error_msgs)
        speak(error_msg)



#Main
main = Tk()
main.title("Virtual Assistant Demo")
main.geometry("875x225")
Label(main, text = "Enter Command:").grid(row=0)
Label(main, text = "Start Guide:").grid(row=0, column=2)
Label(main, text = "Assistant says:").grid(row=1)
Label(main, text = "1. open website <website_name>.com").grid(row=1, column=2)
Label(main, text = "2. email - and then fill out the additional boxes").grid(row=2, column=2)
Label(main, text = "3. google search <query>").grid(row=3, column=2)
Label(main, text = "4. youtube <query>").grid(row=4, column=2)
Label(main, text = "5. wikipedia <query>").grid(row=5, column=2)
Label(main, text = "6. weather <location_name>").grid(row=6, column=2)
Label(main, text = "7. time").grid(row=7, column=2)
Label(main, text = "8. shutdown").grid(row=8, column=2)
Label(main, text = "9. Hello").grid(row=9, column=2)
Label(main, text = "----Additional Fields to fill if Email is command----").grid(row=2)
Label(main, text = "Enter Subject:").grid(row=3)
Label(main, text = "Enter Recipient id:").grid(row=4)
Label(main, text = "Enter Message:").grid(row=5)
Label(main, text = "Enter your id:").grid(row=6)
Label(main, text = "Enter your password:").grid(row=7)


command1 = Entry(main)
blank = Entry(main)
c2 = Entry(main)
c3 = Entry(main)
c4 = Entry(main)
c5 = Entry(main)
c6 = Entry(main)



command1.grid(row=0, column=1, ipadx = 75)
blank.grid(row=1, column=1,ipadx=75)
c2.grid(row=3, column=1, ipadx = 75)
c3.grid(row=4, column=1, ipadx = 75)
c4.grid(row=5, column=1, ipadx = 75)
c5.grid(row=6, column=1, ipadx = 75)
c6.grid(row=7, column=1, ipadx = 75)

Button(main, text='Quit', command=main.destroy).grid(row=9, column=0, sticky=W, pady=4)
Button(main, text='Execute', command=my_command).grid(row=9, column=1, sticky=W, pady=4)

mainloop()