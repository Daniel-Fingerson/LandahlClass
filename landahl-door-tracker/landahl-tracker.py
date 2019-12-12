#NEED TO HAVE THE SQLITE ACCESS THE VERY LAST ENTRY
from flask import Flask, request, render_template
import RPi.GPIO as GPIO
import sqlite3
import time
import datetime
import random
import _thread
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.setup(26,GPIO.OUT)
#GPIO.setup(20,GPIO.IN,pull_up_down = GPIO.PUD_UP) #pull up resistor, so attatch to 20 then ground
#this means the button will normally be set to high
#nevertheless I may need to change this

import smtplib

#eventually make this a function, to be able to choose between whether its email or text, the recipient, the message/subject, ect; will need to do so once it is actually used for error tracking
'''
def text():
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.ehlo()
    server.starttls()
    fromm='djfingerson@gmail.com'
    to='13124987605@vtext.com'
    #to='6085156502@vtext.com'
    #to='13129250274@tmomail.net'
    #to='7088906135@tmomail.net'
    subject='Shrimp Project Notification'
    body='hello world!'
    server.login( 'djfingerson@gmail.com', 'Yerba1998' )
    message = ("From: %s\r\n" % fromm
                 + "To: %s\r\n" % to
                 + "Subject: %s\r\n" % subject
                 + "\r\n"
                 + body)
             
    # Send text message through SMS gateway of destination number
    server.sendmail( fromm, to, message )
    #server.sendmail( fromm, 'carl@enertrex.com', message )
    #carls tmo


'''
app=Flask(__name__,static_url_path='/')
#get rid of post method, just have it constantly reupdate itself to reflow (use same concpet as the update page
'''
@app.route("/")
def input_handle():
    if(GPIO.input(20) == 0):
        GPIO.ouput(21,1)
    return render_template("input_handle.html")
'''

@app.route("/")
#maybe could add the ability to show door status, display if there are any recent requests
def input_handle():
    status=""
    door_status=GPIO.input(21)
    if door_status==1:
        status="out"
    else:
        status="in"
    return render_template("input_handle.html",status=status)

@app.route('/', methods=['POST'])
def input_handle_post():
    #global current_minute, time_needed
    currentDT = datetime.datetime.now()
    current_minute=currentDT.minute
    time_needed=request.form['time_needed']
    name = request.form['name']
    conn=sqlite3.connect('/home/pi/Desktop/landahl-door-tracker/LEDstate.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO LEDstate values((?), (?))""", (current_minute, time_needed)) #problem most likely here: check the log
    conn.commit()
    conn.close()
    #text()
    return render_template('output_handle.html', time=time_needed, first=name)

def background_check():
    #add an option on the else command that writes 0 and 0 (so that it wont randomly blink): have a and conditional that will check if both values arent 0
    while True:
        current_minute=0
        time_needed=0
        conn=sqlite3.connect('/home/pi/Desktop/landahl-door-tracker/LEDstate.db')
        curs=conn.cursor()
        curs.execute("SELECT * FROM LEDstate")
        for row in curs.fetchall():
            current_minute= row[0]
            time_needed=row[1]
        conn.close()
        #time_needed='database'
        #time_req='database'
        currentDT = datetime.datetime.now()
        time_now=currentDT.minute
        final_time=current_minute+time_needed
        #time needed =15; time then was 2:20, time now is 2:30
        if final_time>60: 
            time_req-=60
        if final_time>time_now: #this will eventually loop over so need to find a solution to this
            GPIO.output(26,1)
            time.sleep(1)
            GPIO.output(26,0)
            time.sleep(1)
        else:
            '''
            conn=sqlite3.connect('/home/pi/Desktop/landahl-door-tracker/LEDstate.db')
            curs=conn.cursor()
            curs.execute("""INSERT INTO LEDstate values((?), (?))""", (0, 0))
            conn.commit()
            conn.close()
            '''
            GPIO.output(26,0)
            #time.sleep(20)
        #time now 26; time then 20; need 12 min of tiem
        

if __name__ == "__main__":
    _thread.start_new_thread(background_check, ())
    app.run(debug=True)
#have a threading function that will actually turn the LED on or off by checking the database; call thread direclty above/bewlow the app.run


