from tkinter import *
from auth import Auth
#from sensor import Sensor
#import schedule
from tkinter import messagebox
import time
from threading import *
#from pydub import AudioSegment
#from pydub.playback import play


# create root window
root=Tk()
# create authentication window
login_win = Toplevel()
# create an object from Authentication class and send root and authentication windo for it
authentication = Auth(login_win,root)
# call gui method for create login form
authentication.gui()
# create an object from sensor class
#sensor = Sensor(root)
# call gui method for create panel
#sensor.gui()
# hide root window
root.withdraw()
# Run jobs every 6th hour
# schedule.every(6).hours.at("00:00").do(job)
# for test program run job every 1 minutes


root.mainloop()
