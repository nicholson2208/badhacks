# -*- coding: utf-8 -*-
import requests
import smtplib
import numpy as np
from datetime import datetime
from threading import Timer

def get_emails():
    emails= {};

    try:
        email_file=open('emails.txt','r');

        for line in email_file:
            (email,name,zipcode)=line.split(',')
            emails[email]= [name.strip(), zipcode.strip()]
            print(emails)
    except FileNotFoundError as err:
        print(err)
        
    return emails
def get_content():
    try:
        content_file=open('content.txt','r');
        content = content_file.readlines();
        
        which_quote=np.random.randint(1,29)
        quote=""
        start_reading=0
        # Skips text before the beginning of the interesting block:
        for line in content:
            if start_reading:
                if line.strip() == ('END'+str(which_quote)):
                    break
                quote+=line
            if line.strip() == str(which_quote):  # Or whatever test is needed
                 start_reading=1        
                 
    except FileNotFoundError as error:
        print(error)
    return quote


def get_weather(zipcode):
    #' + str(zipcode) + '
    try:
        url='http://api.openweathermap.org/data/2.5/weather?zip=' + str(zipcode) + ',us&units=imperial&appid=3f14068318795c9e76987df4ed83a0c5'
        weather_req=requests.get(url)
        weather_json=weather_req.json()
        description = weather_json['weather'][0]['description']
        current_temp = weather_json['main']['temp']
        temp_min = weather_json['main']['temp_min']
        temp_max = weather_json['main']['temp_max']
        city= weather_json['name']
        conditions=weather_json['weather'][0]['id']
        
        forecast=''
        if conditions<550:
            forecast +='Make sure to bring an umbrella, it is going to rain!\n\n'
            
        forecast += 'The current temperature in ' + city + ' is '
        forecast += str(int(current_temp)) + ' F.'
        forecast += ' The forecast for today is '
        forecast += description + ' with a high of '
        forecast += str(temp_max) + ' F, and a low of ' + str(temp_min) + ' F.'
        
        return forecast
    except:
        print('there was some issue with the weather')
        return 'Sorry, we were unable to retrieve your weather forecast'
        

def send_emails(emails, content):
    server = smtplib.SMTP('smtp.gmail.com','587')
    server.starttls()
    from_username= '<YOUR USERNAME HERE>'
    server.login(from_username,'<SOME KEY THAT I DONT KNOW HERE>')
    
    for to_username, (name, zipcode) in emails.items():
        message = 'Subject: Daily Weather and Motivational Quote\n'
        message += 'Hi ' + name+ ', \n\n'
        message += get_weather(zipcode) + '\n\n' + 'Here are some pretty inspiring words to get you through the day: \n\n'
        message += content + '\nI hope you found that really motivating! \n\nYours Truly,\nMatt'
        server.sendmail(from_username,to_username, message)
        print(message)

    server.quit()
    
def do_the_email_sending():
    emails=get_emails()
    content=get_content()
    send_emails(emails, content)

def main():
    x=datetime.today()
    print(x)
    y=x.replace(day=x.day+1, hour=7, minute=0, second=0, microsecond=0)
    print(y)
    delta_t=y-x
    print(delta_t)
    secs=delta_t.seconds+1
    t = Timer(secs, do_the_email_sending)
    t.start()


main()