import threading
from time import time,sleep
from storage.sqlite_event_storage import SQLiteEventStorage
import json
import RPi.GPIO as GPIO

class GpioConnector(threading.Thread):
    def __init__(self,ConnecConf):
        threading.Thread.__init__(self)
        self.ConnecConf = ConnecConf['gpio']
        self.running = True
        self.pin_status = {}
        self.Database = SQLiteEventStorage()
        self.setup()
        




    def setup(self,ConnecConf=None): 
        if ConnecConf is not None :
            self.ConnecConf=ConnecConf
        GPIO.setmode(GPIO.BCM)  
        for pin_information in self.ConnecConf['timeseries']:
            GPIO.setup(pin_information['pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            if pin_information['pin'] not in self.pin_status or self.pin_status[pin_information['pin']][0] != GPIO.input(pin_information['pin']):
                self.pin_status[pin_information['pin']] = [GPIO.input(pin_information['pin']),pin_information['tag'],int(time()*1000)]
                data={'parameters':{pin_information['tag']:GPIO.input(pin_information['pin'])},
                                                  "ts":int(time()*100)}
                self.Database.put(json.dumps(data))
                sleep(0.1)
                GPIO.add_event_detect(pin_information['pin'],GPIO.BOTH,callback=self.pin_status_callback,bouncetime=40)

                
            
    def pin_status_callback(self,pin):
        if pin not in self.pin_status or self.pin_status[pin][0] != GPIO.input(pin):
            self.pin_status[pin][0] = GPIO.input(pin)
            data = json.dumps({"parameters":{self.pin_status[pin][1]:GPIO.input(pin)},
                                           "ts":int(time()*1000)})
            self.Database.put(data)
            


    def run(self):
        self.setup()
        try:
            while self.running:
                # if not self.data_queue.empty():
                # print(self.data_queue.get())
                # self.data_queue.task_done()
                sleep(0.01)
        except KeyboardInterrupt :
            GPIO.cleanup()
            print("gpio reading stop")
    def stop(self):
        self.running = False
        GPIO.cleanup()


# class GpioConnector(threading.Thread):
#     def __init__(self, ConnecConf):
#         threading.Thread.__init__(self)
#         self.running = True
#         self.ConnecConf = ConnecConf
#         self.Database = SQLiteEventStorage

#         GPIO.setmode(GPIO.BCM)  
#         for pin_information in self.gpio_pins:
#             for pin,values in pin_information.items():
#                 GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#                 if pin not in self.pin_status or self.pin_status[pin][0] != GPIO.input(pin):
#                     self.pin_status[pin] = [GPIO.input(pin),values,int(time()*1000)]
#                     self.Database.put(json.dumps({self.pin_status[pin][1]:GPIO.input(pin),
#                                                   "ts":int(time()*100)}))
                    
#                     # print(self.data_queue.get())
#                 # print(f"pin status befor event{pin} {self.data_queue}")
#                 GPIO.add_event_detect(pin,GPIO.BOTH,callback=self.pin_status_callback,bouncetime=40)
#     def pin_status_callback(self,pin):
#          if pin not in self.pin_status or self.pin_status[pin][0] != GPIO.input(pin):
#              self.pin_status[pin][0] = GPIO.input(pin)
#              self.Database.put(json.dumps({self.pin_status[pin][1]:GPIO.input(pin),
#                                            "ts":int(time()*1000)}))
#             #  self.data_queue.put([GPIO.input(pin),self.pin_status[pin][1],int(time()*1000)])
#             #  print(self.data_queue.get())
#             #  print(f"pin event detect {pin} {self.pin_status[pin]}") 

#     def run(self):
#         try:
#             while self.running:
#                 # if not self.data_queue.empty():
#                 # print(self.data_queue.get())
#                 # self.data_queue.task_done()
#                 sleep(0.01)
#         except KeyboardInterrupt :
#             # GPIO.cleanup()
#             print("gpio reading stop")
#     def stop(self):
#         self.running = False
        # GPIO.cleanup()



    
