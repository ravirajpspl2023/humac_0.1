import threading
from time import time,sleep
import minimalmodbus
from minimalmodbus import BYTEORDER_LITTLE_SWAP
import json
from storage.sqlite_event_storage import SQLiteEventStorage

API ={"bit":"read_bit",
      "bits":"read_bits",
      "16int":"read_register",
      "16uint":"read_register",
      "32int":"read_long",
      "32uint":"read_long",
      "64int":"read_long",
      "64uint":"read_long",
      "32float":"read_float",
      "64float":"read_float",
      "string":"read_string"
      }
SIGN={
    "16int":True,
    "32int":True,
    "64int":True,
}

class ModbusConnector(threading.Thread):
    def __init__(self,Connconfig):
        threading.Thread.__init__(self)
        self.running =  True
        self.ConneConfig = Connconfig
        self.Database = SQLiteEventStorage()


    def connect(self):
        try:
            minimalmodbus.BYTEORDER_LITTLE_SWAP
            self.instrument=minimalmodbus.Instrument(self.ConneConfig['modbus']['port'],self.ConneConfig['modbus']['unitId']
                                                     ,self.ConneConfig['modbus']['method'])
            self.instrument.serial.baudrate=self.ConneConfig['modbus']['baudrate']
            self.instrument.serial.parity = self.ConneConfig['modbus']['parity']
            self.instrument.serial.startbits=self.ConneConfig['modbus']['stopbits']
            self.instrument.serial.bytesize = self.ConneConfig['modbus']['bytesize']
            self.instrument.serial.timeout = self.ConneConfig['modbus']['timeout']
            self.instrument.clear_buffers_before_each_transaction = True
            self.instrument.close_port_after_each_call = True
            self.instrument
        except Exception as e :
            print(e)
            print("error to connecte modbus device")
            # self.connect()
            sleep(10)

    def read_register(self):
        for registerConfig in self.ConneConfig['modbus']['timeseries']:
            try:
                if (API.get(registerConfig['type'])):
                    api=API.get(registerConfig['type'])
                    method=getattr(self.instrument,api)
                    if api == "read_register":
                        signed=False
                        if SIGN.get(registerConfig['type'])  :
                            signed =  True
                        value=method(registeraddress=registerConfig['address'],functioncode=registerConfig['functionCode'],
                                      signed=signed,number_of_decimals=registerConfig['objectsCount'])
                    elif api == "read_float":
                        value=method(registeraddress=registerConfig['address'], functioncode =registerConfig['functionCode'], number_of_registers=registerConfig['objectsCount'], byteorder=self.ConneConfig['modbus']['byteorder'])
                    elif api == 'read_long':
                        signed =  False
                        if SIGN.get(registerConfig['type'])  :
                            signed =  True
                        value=method(registeraddress=registerConfig['address'],functioncode =registerConfig['functionCode'],signed=signed,byteorder=self.ConneConfig['modbus']['byteorder'],number_of_registers=registerConfig['objectsCount'])
                    elif api == 'read_bit':
                        value=method(registeraddress=registerConfig['address'], functioncode=registerConfig['functionCode'])

                    elif api == "read_bits":
                        value=method(registeraddress = registerConfig['address'], number_of_bits = registerConfig['objectsCount'] , functioncode = registerConfig['functionCode'])
                    elif api == "read_string":
                        value=method(registeraddress=registerConfig['address'],functioncode=registerConfig['functionCode'])

                    else:
                        print(f"{registerConfig['type']}.{API.get(registerConfig['type'])}()")
                    data={'parameters':{registerConfig['tag']:value},
                                                  "ts":int(time()*1000)}
                    self.Database.put(json.dumps(data))
                    sleep(0.1)
             
            except Exception as e :
                print(f"funaction is not {e}")
                sleep(0.1)
                self.connect()
                # self.stop()
                


    def run(self):
        self.connect()
        self.read_register()
        while self.running:
            try:
                self.read_register()
                
                sleep(self.ConneConfig['modbus']['timedelay'])
            except KeyboardInterrupt:
                print("Exiting program")
                print("Done")

    def stop(self):
        self.running = False




                