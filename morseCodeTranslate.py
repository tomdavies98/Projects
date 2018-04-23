#Importing winsound to create beeps ('as win' is used to shorten calls)
#Importing time to create delays when needed
import winsound as win
import speech_recognition as sr
import time
import pyaudio
import wave
import struct
import math

ls = []


def yes(res):
        #For loop used to parse through string
        #And beep respectively to what is found
        #Print statements used for debugging
        #For loop in the range of
        
        #Setting values for frequency and duration
        #to keep ratio needed between dots and dashes
        frequency = 1000
        duration = 100
        t = duration/1000
        for i in range(len(res)):
            if(res[i] == '.'):
                print("DOT")
                win.Beep(frequency,duration)
                time.sleep(t)
            elif(res[i] == '-'):
                print("DASH")
                win.Beep(frequency,(3*duration))
                time.sleep(t)
            elif(res[i] == '/'):
                print("NEW WORD")
                time.sleep(7*t)

        print("Finished.")
        print(len(res), 'is the length of the string in morse code.' )

def no():
    print("Finished.")
   # print(len(res), 'is the length of the string in morse code.' )

def trans():
    mes = input("Input string to translate: ")
    




    #For loop that changes all letters in a string to their
    #morse code counter-parts
    #added to list for ease of use
    for elem in mes:
        ls.append(mor[elem.upper()] + ' ')

    #Translated from list to string
    #so one for loop can be used later
    #for parsing
    res = ''.join(ls)
    print(res)
    return(res)

def trans2(mes):
    lit = []
    for elem in range(len(mes)):
        lit.append(mor[mes[elem].upper()] + ' ')

    result = ''.join(lit)
    print(result)
    k = input("Would you like to hear the audio version? (y/n)")

    if(k.lower() == "y"):
        yes(result)
    else:
        print("Finished.")


#Creating a list to associate certain letters with their counter-parts
mor = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W':  '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.', ' ': '/', "'": '',
        }

#Decided if reading or writing morse code
test = input("Would you like to record or write Morse Code (r,w) ").lower()

if(test == 'r'):
#Uses the Google API to take in
#words and translate them into morse code
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Talk now!')
        audio = r.listen(source)

    try:
        print('Google thinks you said:\n' + r.recognize_google(audio))
        

    except:
        print("\nSay again?")
        
    g =  r.recognize_google(audio)
    trans2(g)
        

    
    
elif(test == 'w'):
    work = trans()
    s1 = input("Would you like to hear the audio version?(y/n)")

    #If statement used to give choice of
    #playing audio or not

    if(s1.lower() == "y"):
        yes(work)
        
    else:
        no()
                 

















        
