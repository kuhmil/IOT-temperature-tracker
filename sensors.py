#!/usr/bin/env python3

from tkinter import *
import os
import glob
import time
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
#from time import sleep
import datetime 
import time
import sqlite3
#import Adafruit_DHT
dbname='/home/pi/interbrew_data/interbrew.db'
sampleFreq = 2 # time in seconds
# get data from DHT sensor


os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#Sensors
relay_cold = 15
relay_hot = 16
#temp_probe = 13


def blink(pin):
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    #while True: # Run forever
    GPIO.output(pin, GPIO.HIGH) # Turn on
    sleep(1)                  # Sleep for 1 second
    GPIO.output(pin, GPIO.LOW)  # Turn off
    sleep(1)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return str(round(temp_c, 2)), str(round(temp_f, 2))

#Relays
def relays(relay_change, state):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay_change, GPIO.OUT)
    GPIO.output(relay_change, state)

now = datetime.datetime.now().replace(second=0, microsecond=0)

def logData (temp_c, temp_f):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print("reading log")
    #curs.execute("INSERT INTO TEMP (date('now','localtime'),time('now','localtime'),temp_c,temp_f) VALUES (?,?,?,?)" (date, time, temp_c, temp_f))
    curs.execute("INSERT INTO TEMP values(date('now','localtime'),time('now','localtime'), (?), (?))", (temp_c, temp_f))
    #curs.execute(INSERT INTO DATA(id, date('now','localtime'), time('now','localtime'), temp_c, temp_f) VALUES ((?), (?),  (?), (?), (?)))
    conn.commit()
    conn.close()
# display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    #print ("\nEntire database contents:\n")
    #for row in curs.execute("SELECT * FROM TEMP_data"):
     #   print (row)
    conn.close()
# main function
def main():
    for i in range (0,3):
        read_temp()
        time.sleep(sampleFreq)
    displayData()


def toggle():
	if GPIO.input(temp_c):
		GPIO.output(24, GPIO.LOW)
		toggleButton["text"] = "Turn LED On"
	else:
		GPIO.output(24, GPIO.HIGH)
		toggleButton["text"] = "Turn LED Off"



temp_c, temp_f = read_temp()
logData(float(temp_c), float(temp_f))
main()
print(f"{temp_c}, {temp_f} writing temp data to database")

# gui = Tk(className='Python Examples - Button')
# gui.geometry("500x200")

window = Tk()
window.title("Start/Stop Button")
window.geometry('500x200')
# window.configure(bg='white')
temp_c=str(23.2)


def temp_button():
    if tmp_btn['text'] == temp_c+"°C":
        tmp_btn.configure(text=temp_f+"°F")
    else:
        tmp_btn.configure(text=temp_c+"°C")

# + "°C")

tmp_btn = Button(window, text=temp_c+"°C", command=temp_button, width=70, height=7, bg='black', fg='white', activebackground='grey', activeforeground='white', 
    justify=CENTER, font=('Audiowide', '48'))
# tmp_btn.grid(column=1, row=1)
tmp_btn.pack(side=TOP, expand=YES)

# tmp_button = Button(window, text=temp_c,command=temp_button, width=70, height=7, bg='black', fg='white', activebackground='white', activeforeground='blue')


window.mainloop()



