from tkinter import *
from tkinter import PhotoImage
import datetime
from SensoBoardr import SensorBoard
import json
import requests
import datetime

from matplotlib.pyplot import close
from threading import Thread

import os
import mimetypes

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from tkinter import messagebox
from pydub import AudioSegment
from pydub.playback import play

import schedule
from tkinter import messagebox
import time
from threading import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
# create
class Sensor:
    def __init__(self,root):
        # get root window from main
        self.root = root
        # create  an object from sensorBoard class
        self.s=SensorBoard()
        self.timeSchedule = 1
        self.entry_exist=False
        self.json_name="flows.json"

        # thred for Run the program asynchronous 
        t1=Thread(target=self.check)
        t1.start()

    def gui(self):
            
        # Adjust size
        self.root.geometry("600x400")

        # Add image file
        self.bg = PhotoImage(file = "bg.png")

        # Create Canvas
        self.canvas1 = Canvas( self.root, width = 400,
                        height = 400)

        self.canvas1.pack(fill = "both", expand = True)

        # Display image
        self.canvas1.create_image( 0, 0, image = self.bg,
                            anchor = "nw")
        # create frame for display temprature,Humidity,Pressure
        frame= LabelFrame(self.root,relief=RIDGE,borderwidth=4)
        # put frame in window with canvas
        frame_canvas = self.canvas1.create_window( 200, 160, anchor = "nw",
        
                                            window = frame)
        # stringvar for change value in label
        self.temp=StringVar()
        # set default value in label
        self.temp.set("Temprature: _")
        # Temprature label
        temp_label = Label(frame, textvariable=self.temp, font=('',12),bg="lightgreen",width=20)
        temp_label.grid(row=0, column=0)

        # stringvar for change value in label
        self.humidity=StringVar()
        # set default value in label
        self.humidity.set("Humidity: _")
        # Humidity label
        humidity_label = Label(frame, textvariable=self.humidity, font=('',12),bg="lightgreen")
        humidity_label.grid(row=1, column=0,sticky="WE")

        # stringvar for change value in label
        self.pressure = StringVar()
        # set default value in label
        self.pressure.set("Pressure: _")
        # Pressure label
        pressure_label = Label(frame, textvariable=self.pressure, font=('',12),bg="lightgreen")
        pressure_label.grid(row=2, column=0,sticky="WE")

        # create buttons
        setting_btn = Button(self.canvas1, text = "Setting", width=5, command=self.settingGui)
        close_btn = Button(self.canvas1, text = "Close",width=5, command=self.root.destroy)

        
        # place buttons in canvas window
        setting_btn_convas = self.canvas1.create_window( 160, 80, anchor = "nw",
                                            window = setting_btn)
        
        close_btn_convas = self.canvas1.create_window( 360, 80, anchor = "nw",
                                            window = close_btn)
        
        
        # show time in top of window
        t=StringVar()
        date=datetime.datetime.now()
        time_str = f"{date.hour}:{date.minute}:{date.second}"
        t.set(time_str)
        time_label= Label(self.canvas1, textvariable=t, font=('',10))
        time_convas = self.canvas1.create_window( 270, 10, anchor = "nw",
    
                                                window = time_label)
    def settingGui(self):
        self.win = Toplevel()
        
        self.canvas2 = Canvas( self.win, width = 750,
                        height = 200)

        self.canvas2.pack(fill = "both", expand = True)

        # # Display image
        # self.canvas2.create_image( 0, 0, image = self.bg,
        #                     anchor = "nw")
        # create frame for display temprature,Humidity,Pressure
        frame= LabelFrame(self.win,relief=RIDGE,borderwidth=4)
        # put frame in window with canvas
        frame_canvas = self.canvas2.create_window( 200, 160, anchor = "nw",
        
                                            window = frame)
        tmp_frame= LabelFrame(self.canvas2, text="Temprature")
        time_type = ["Minute", "Hour"]
        time_lbl = Label(tmp_frame, text = "Time")
        self.time_entry = Entry(tmp_frame)
        self.time_entry.insert(0,6)
        self.time_set = StringVar()
        self.time_set.set("Hour")
        time_option = OptionMenu(tmp_frame, self.time_set, *time_type)

        time_lbl.grid(row= 0, column=0)
        self.time_entry.grid(row= 0, column=1)
        time_option.grid(row=0, column=2)

        tmp_high_lbl = Label(tmp_frame, text = "High Limit")
        self.tmp_high_entry = Entry(tmp_frame)
        self.tmp_high_entry.insert(0,38)
        tmp_high_lbl.grid(row= 1, column=0)
        self.tmp_high_entry.grid(row= 1, column=1)

        tmp_low_lbl = Label(tmp_frame, text = "Low Limit")
        self.tmp_low_entry = Entry(tmp_frame)
        self.tmp_low_entry.insert(0,-5)
        tmp_low_lbl.grid(row= 2, column=0)
        self.tmp_low_entry.grid(row= 2, column=1)

        pressure_frame= LabelFrame(self.canvas2, text="Pressure",height=200)


        pressure_high_lbl = Label(pressure_frame, text = "High Limit")
        self.pressure_high_entry = Entry(pressure_frame)
        self.pressure_high_entry.insert(0,150)
        pressure_high_lbl.grid(row= 0, column=0)
        self.pressure_high_entry.grid(row= 0, column=1)

        pressure_low_lbl = Label(pressure_frame, text = "Low Limit")
        self.pressure_low_entry = Entry(pressure_frame)
        self.pressure_low_entry.insert(0,0)
        pressure_low_lbl.grid(row= 1, column=0)
        self.pressure_low_entry.grid(row= 1, column=1)

        humidity_frame= LabelFrame(self.canvas2, text="Humidity")

        humidity_high_lbl = Label(humidity_frame, text = "High Limit")
        self.humidity_high_entry = Entry(humidity_frame)
        self.humidity_high_entry.insert(0,38)
        humidity_high_lbl.grid(row= 0, column=0)
        self.humidity_high_entry.grid(row= 0, column=1)

        humidity_low_lbl = Label(humidity_frame, text = "Low Limit")
        self.humidity_low_entry = Entry(humidity_frame)
        self.humidity_low_entry.insert(0,-5)
        humidity_low_lbl.grid(row= 1, column=0)
        self.humidity_low_entry.grid(row= 1, column=1)

        start_btn = Button(self.canvas2, text = "Start", width=5, command=lambda:self.calcSensor(call_from_start=True))
        # start_btn = Button(self.canvas2, text = "Start", width=5)
        json_btn = Button(self.canvas2, text = "Json",width=5, command=self.writeToJson)
        cloud_btn = Button(self.canvas2, text = "Cloud",width=5,command=lambda:self.sendToCloud("./", "flows.json",  "1TxLY0uJOZGHmacInMeDi8oK0v8RyMpuQ"))
        # cloud_btn = Button(self.canvas2, text = "Cloud",width=5)

        tmp_frame_convas = self.canvas2.create_window( 5, 0, anchor = "nw",
                                            window = tmp_frame)
        pressure_frame_convas = self.canvas2.create_window( 325, 0, anchor = "nw",
                                            window = pressure_frame)
        humidity_frame_convas = self.canvas2.create_window( 570, 0, anchor = "nw",
                                            window = humidity_frame)
        start_btn_convas = self.canvas2.create_window( 220, 110, anchor = "nw",
                                            window = start_btn)
        json_btn_convas = self.canvas2.create_window( 310, 110, anchor = "nw",
                                            window = json_btn)
        cloud_btn_convas = self.canvas2.create_window( 400, 110, anchor = "nw",
                                            window = cloud_btn)

        date_option_list = self.fetch_date()
        self.date_option_set = StringVar()
        self.date_option_set.set(date_option_list[0])
        date_option = OptionMenu(self.win, self.date_option_set, *date_option_list)
        date_option.place(x=190, y=150)

        type_option_list = ["temprature","pressure", "humidity"]
        self.type_option_set = StringVar()
        self.type_option_set.set("temprature")
        type_option = OptionMenu(self.win, self.type_option_set, *type_option_list)
        type_option.place(x=310, y=150)

        show_plot_btn = Button(self.win, text ="Show Plot", command=self.showPlot)
        show_plot_btn.place(x=430, y=150)
    # this method show temprature and humidity and pressure in frame
    def calcSensor(self, call_from_start=False):
        if call_from_start:
            self.entry_exist = True
            self.timeSchedule = int(self.time_entry.get())
            if self.time_set.get() == "Minute":
                schedule.every(self.timeSchedule).minutes.do(self.job)
            else:
                schedule.every(self.timeSchedule).hour.do(self.job)
            print(self.json_name,"===========================")
            if self.json_name == "flows.json":        
                self.create_json()
            else:
                schedule.every().day.do(self.create_json)
            self.win.withdraw()
        # call calculate method in sensorBoard Class
        self.result = self.s.calculate()
        print(self.result)
        # set data in labels
        self.temp.set(f"Temprature: {self.result['Temp']} °C")
        self.humidity.set(f"Humidity: {self.result['Humid']} %")
        self.pressure.set(f"Pressure: {self.result['Press']} milibar")
        self.monitor(self.result['Temp'],self.result['Humid'],self.result['Press'])
    # write informatin in json file
    def writeToJson(self,result="",auto=False):
        # open file
        # file=open('flows.json',)
        # load data in json file
        # data=json.load(file)
        # call sensor method for update data
        self.calcSensor()
        dic = self.load_data(self.json_name)
        d=datetime.datetime.now()
        key=f"flows-{d.year}/{d.month}/{d.day}--{d.hour}:{d.minute}:{d.second}.json"
        
        if result=="":
            data=self.result
        else:
            data = result
        # write data in json
        dic[key] = data
        
        with open(self.json_name, 'w') as output:
            json.dump(dic,output,indent=4)
            # show message
            if auto ==False:
                messagebox.showinfo("showinfo", "write to json successful")
        return self.json_name
        
    # send data to google drive
    # folder: codes folder
    # file_name: flows.json, we want upload it to google drive
    # parent_folder_id: iot (folder name in google drive)
    def sendToCloud(self,folder, file_name, parent_folder_id=None,auto=False):
        file_name = self.writeToJson(auto=True)
        # scope is api link
        scope = 'https://www.googleapis.com/auth/drive'
        scopes=[scope]
        # this file is contain authenticate key for login google drive
        key_file_location = 'iot-tgm-2022-358515-6f7da107e6ab.json'

        try:
            # Authenticate and construct service.
            credentials = service_account.Credentials.from_service_account_file(
            key_file_location)

            scoped_credentials = credentials.with_scopes(scopes)

            # Build the service object.
            # use google drive api v3
            service = build('drive', 'v3', credentials=scoped_credentials)
        except HttpError as error:
                # TODO(developer) - Handle errors from drive API.
                print(f'An error occurred: {error}')
                # show error message
                if auto==False:
                    messagebox.showerror("showerror", f'An error occurred: {error}')
        # search flows.json file (local json file) that exis in this folder
        file_path = os.path.join(folder, file_name)
        # type of file
        mime_type = mimetypes.guess_type(file_path)
        #create  file metadata
        file_metadata = {'name': file_name}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        # upload file to destination
        media = MediaFileUpload(file_path, mimetype=mime_type[0])
        results = service.files().list(q=f"name = '{self.json_name}'",
                                   pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
  
            file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
            # self.json_id=file.get('id')
        else:
            file = service.files().update(
                                    media_body=media,
                                    fileId=items[0]['id']).execute()

        if auto==False:
            # show message
            messagebox.showinfo("showinfo", "Upload successful")

        print('File ID: %s' % file.get('id'))
    def set_tim_sc(self):
        self.timeSchedule = int(self.time_entry.get())

    def check(self):
        while True:

            # Checks whether a scheduled task
            # is pending to run or not
            # self.set_tim_sc()
            schedule.run_pending()
            time.sleep(1)

            if self.entry_exist:
                self.set_tim_sc()

    #  every 6 houre this function is called  
    # this function call methods in other classes
    # calculate data and write it in json and send it to cloud
    # if  temperature bigger than 38 or less than -5 show alarm
    def job(self):
        print("test**************************************")
        result= self.s.calculate()
        name=self.writeToJson(result,True)
        print(name)
        self.sendToCloud("./", name,  "1TxLY0uJOZGHmacInMeDi8oK0v8RyMpuQ",True)
        temperature = int(result['Temp'])
        humidity = int(result['Humid'])
        pressure = int(result['Press'])
        self.monitor(temperature,humidity,pressure )

    def monitor(self,temperature,humidity,pressure):
        if temperature>=int(self.tmp_high_entry.get()):
            song = AudioSegment.from_wav("a.wav")
            play(song)
            t1 = Thread(target=play, args=(song,))
            t1.start()
            messagebox.showinfo("showerror", f"The temperature is above {self.tmp_high_entry.get()} degrees")
        elif temperature<=int(self.tmp_low_entry.get()):
            song = AudioSegment.from_wav("a.wav")
            play(song)
            t1 = Thread(target=play, args=(song,))
            t1.start()
            messagebox.showinfo("showerror", f"The temperature is less than {self.tmp_low_entry.get()} degrees")
        if humidity>=int(self.humidity_high_entry.get()):
            song = AudioSegment.from_wav("a.wav")
            play(song)
            t1 = Thread(target=play, args=(song,))
            t1.start()
            messagebox.showinfo("showerror", f"The Humidity is above {self.humidity_high_entry.get()}")
        elif humidity<=int(self.humidity_low_entry.get()):
            song = AudioSegment.from_wav("a.wav")
            play(song)
            t1 = Thread(target=play, args=(song,))
            t1.start()
            messagebox.showinfo("showerror", f"The humidity is less than {self.humidity_low_entry.get()}")
        if pressure>=int(self.pressure_high_entry.get()):
            song = AudioSegment.from_wav("a.wav")
            play(song)
            t1 = Thread(target=play, args=(song,))
            t1.start()
            messagebox.showinfo("showerror", f"The pressure is above {self.pressure_high_entry.get()} bar")
        elif pressure<=int(self.pressure_low_entry.get()):
            song = AudioSegment.from_wav("a.wav")
            play(song)
            t1 = Thread(target=play, args=(song,))
            t1.start()
            messagebox.showinfo("showerror", f"The pressure is less than {self.pressure_low_entry.get()} bar")


    def create_json(self):
        d=datetime.datetime.now()
        self.json_name=f"flows-{d.year}-{d.month}-{d.day}--{d.hour}-{d.minute}-{d.second}.json"
        with open(self.json_name, 'w') as output:
            json.dump({},output,indent=4)
        # return name
    def load_data(self,file_name):

        with open(file_name, "r") as f:
            dic = json.load(f)
            
            return dic
    def fetch_date(self):
        date_list=[]
        files= os.listdir("./")
        for x in files:
            if x !="__pycache__" and x!="install" and x!="iot-tgm-2022-358515-6f7da107e6ab.json" and x!="flows.json":
                print(x)
                file_name = x.split(".")
                if file_name[1] == "json":
                    date_list.append(file_name[0][6:15])
        # print(date_list)
        return date_list
    
    def create_plot(self,time_list,item_list,y_title,high,low):
        # num_list = np.arange(low, high, 2)
        plt.plot(time_list,item_list)
        plt.xlabel('Time', color='#1e8bc3')
        plt.ylabel(y_title, color='#e74c3c')
        plt.title('Temperature Monitoring', color='#34495e')
        plt.axhline(y=low-1, xmin=0, xmax= 12,linestyle="dotted",color="red")
        plt.axhline(y=high+1, xmin=0, xmax= 12,linestyle="dotted",color="red")
        # plt.xticks(np.arange(low, high, 5))
        plt.show()

    def createPlotInfo(self, date):
        times_list=[]
        tempratures_list=[]
        pressures_list=[]
        humidities_list = []
        files= os.listdir("./")
        for x in files:
            if x !="__pycache__" and x!="install" and x!="iot-tgm-2022-358515-6f7da107e6ab.json" and x!="flows.json":
                file_name = x.split(".")
                if file_name[1] == "json" and file_name[0][6:15] == date :
                    dic=self.load_data(x)
        if len(dic)!=0:
            for key, value in dic.items():
                t= key.split("--")
                times_list.append(t[1].strip(".json")) 
                tempratures_list.append(value["Temp"])
                pressures_list.append(value["Press"])
                humidities_list.append(value["Humid"])
        return times_list, tempratures_list, pressures_list, humidities_list

    def showPlot(self):
        date = self.date_option_set.get()
        type_plt  =  self.type_option_set.get()
        times_list, tempratures_list, pressures_list, humidities_list=self.createPlotInfo(date)
        if type_plt == "temprature":
            high = int(self.tmp_high_entry.get())
            low = int(self.tmp_low_entry.get())
            self.create_plot(times_list, tempratures_list, "Temperature (°C)", high,low )
        elif type_plt == "humidity":
            high = int(self.humidity_high_entry.get())
            low = int(self.humidity_low_entry.get())
            self.create_plot(times_list, humidities_list, "Humidity", high,low )
        elif type_plt == "pressure":
            high = int(self.pressure_high_entry.get())
            low = int(self.pressure_low_entry.get())
            self.create_plot(times_list, pressures_list, "Pressure (bar)", high,low )
        
        

