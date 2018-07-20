#Audio file to text Program
import time
import wave
import os
import contextlib
import math
import speech_recognition as sr
import warnings
warnings.filterwarnings("ignore")
from pydub import AudioSegment

r = sr.Recognizer()
text_file = open("Output.txt", "w")
text_file.write("This is the output of your audio file:\n")
text_file.close()


ans = []
songList = []

n = input("Enter the exact name of your sound file with extension \n(Ensure .wav file)\nDeveloped by Tom Davies 18/07/18\n")

print("Processing.. This may take a few minutes")

audio = n
#finds out how long the sound file is
with contextlib.closing(wave.open(audio,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

count = 0

#duration is divided by 30 because thats the length of our
#audio files(30 seconds)
amount = duration/10

amount2 = amount
t = int(amount)
if((amount - t) is not amount):
    amount = math.ceil(amount)
    

#Now split up the file into files
newAudio = AudioSegment.from_wav(n)

#tslice refers to the lenth of the slices
#in this case 30 seconds
tslice = 10000

start = 0
finish = start + tslice

for i in range(amount):
    s1 = "song",i+1,".wav"
    s1 = ''.join(map(str,s1))
    
    sliced = newAudio[start:finish]
    sliced.export(s1,format="wav")
    start = finish
    finish = finish + tslice
    count+=1
    
#Below for loop translates the split
#files into text

for i in range(amount):
    res = "song",i+1,".wav"
    res = ''.join(map(str,res))
    
    with sr.AudioFile(res) as source:
        res = r.record(source)

    try:
        text = r.recognize_google(res)
        ans.append(text)
        

    
    except Exception as e:
        print(e)

fin = '\n'.join(ans)

text_file = open("Output.txt", "w")
text_file.write(fin)
text_file.close()

#This for loop will remove the extra files

for i in range(amount):
    u = "song",i+1,".wav"
    u = ''.join(map(str,u))
    print("Removing extra files",u,"...")
    os.remove(u)

print("Finished...")
time.sleep(3)







