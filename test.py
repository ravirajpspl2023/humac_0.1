# from utility.config import HumacConfig
from time import sleep,time
import json
# import threading
# import minimalmodbus

from storage.sqlite_event_storage import SQLiteEventStorage

Database = SQLiteEventStorage()

# Database.put(message=json.dumps({'v1':12,'ts':1213343}))

event = Database.get_event_pack()
if event !=[]:

    print(event)
Database.event_pack_processing_done()

# while True :
#     Database.put(json.dumps({"ts":int(time()*1000),"parameters":{'v1':2,'v2':1,'v3':0}}))
#     sleep(1)

# Database.event_pack_processing_done()

# try:
#     instrument = minimalmodbus.Instrument("COM3",1)
#     instrument.serial.baudrate = 9600  # Baudrate
#     instrument.serial.bytesize = 8     # Number of data bits
#     instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
#     instrument.serial.stopbits = 1     # Number of stop bits
#     instrument.serial.timeout  = 1 
# except Exception as e :
#     print(e)

# print (getattr(instrument,'read_register'))

# DEFAULT_CONNECTORS = {
#     "mqtt": "MqttConnector",
#     "modbus": "ModbusConnector",
#     "opcua": "OpcUaConnectorAsyncIO",
#     "opcua_asyncio": "OpcUaConnectorAsyncIO",
#     "ble": "BLEConnector",
#     "request": "RequestConnector",
#     "can": "CanConnector",
#     "bacnet": "BACnetConnector",
#     "odbc": "OdbcConnector",
#     "rest": "RESTConnector",
#     "snmp": "SNMPConnector",
#     "ftp": "FTPConnector",
#     "socket": "SocketConnector",
#     "xmpp": "XMPPConnector",
#     "ocpp": "OcppConnector",
#     "gpio":"GpioConnector"
# }


# try :
#     connectors = [{"type":"modbus"},
#                   {"type":"gpio"}]
    
#     for connector in connectors:
#         # print(connector["type"])
#         print(f"connectors.{connector['type']}.{DEFAULT_CONNECTORS.get(connector['type'])}")

#     # lock = threading.Lock()
#     # HumacConf = {}
#     # configration = HumacConfig('./config/config.json',HumacConf,lock)
#     # configration.start()


#     # configration.updateConfig({'Humac_client': {'broker': 'dev-broker.humac.live', 'port': 1883, 'baseTopic': 'pspl_iot/gateway', 'tenantid': 'Humac-01', 'machineid': 'HUM-011', 'edgeid': 'E40234'}, 'connectors': [{'type': 'modbus', 'configPath': ''}, {'type': 'gpio', 'configPath': ''}]})
#     # sleep(1)

# except KeyboardInterrupt as e :
#     print("close")
#     configration.stop()

# configration.stop()

# from storage.sqlite_event_storage import SQLiteEventStorage

# import json
# import paho.mqtt.client as mqtt
# from time import sleep,time

# def on_connect(client, userdata, flags, rc):
#      print(flags)


# def on_message(client, userdata, msg):
#     print(client,msg.topic)

# def on_disconnect(client, userdata, rc):
#      print("client is disconnected")

# client = mqtt.Client('HumacGateway')

# client.connect('dev-broker.humac.live',1883)
# client.loop_start()

# client.on_message = on_message
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect 

# client.loop_stop()

# while True :
#      if client.is_connected :
#           client.publish("humac/gateway/E4003",json.dumps({"name":"humac",
#                                                            "connector":[{"type":
#                                                                          "modbus"}]}))
          
#      sleep(1)



     
    
 


# import json
# from time import time , sleep

# from connectors.GpioPins import GPIOReader

# gpio = GPIOReader('noting ')

# # from connectors.modbusSerial import ModbusReader 

# # modbus =  ModbusReader() 

# # modbus.run

# # print(modbus)

# # for i in range(0,10):
# #     for i in range(0,10):
# #         if i == 5 :
# #             print("break")
# #             break
# #         print(i)
# #     if i == 5 :
# #         break

# # event = '{"ts":123453,"parameters":{"v1":230,"v2":240,"v3":235}}'
# # currentdata = json.loads(event)

# # print(currentdata['ts'], currentdata['parameters'])

# # database = SQLiteEventStorage()

# # event = database.get_event_pack()

# # for events in event :
# #     current = json.loads(events)
# #     if current['ts'] :
# #         ts = current['ts'];None
# #         print(ts)

# #     if current['parameters'] :
# #         for key ,value in current['parameters'].items():
# #             print(key,value)
#     # print(current['ts'])
#     # parameters = current['parameters']
#     # for ts, parameters in current.items():
#     #     print(ts,parameters)
     
#         # for param , value in parameters.items():
#         #     print(param,value)

# # while True:
# #     data = {'ts':int(time()*1000),'parameters':{"v1":1234,"v2": 121}}

# #     json_data = json.dumps(data)
# #     print(json_data)
# #     database.put(json_data)
# #     sleep(1)


# # event = database.get_event_pack()

# # database.event_pack_processing_done()

# # for events in event:
# #     current_data =json.loads(events)
# #     print(current_data['ts'])

# # i=0
# # while True :
# #     event = {"MaxOile": 0,
# #              "ts": int(time()*1000)}
# #     Database.put(json.dumps(event))
# #     i+=1
# #     print(i)
# #     sleep(1)