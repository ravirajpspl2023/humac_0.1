import paho.mqtt.client as mqtt
from storage.sqlite_event_storage import SQLiteEventStorage
import threading
import json
from time import  sleep

class MQTTPublisher(threading.Thread):
    def __init__(self, HumacClient,modules):
        threading.Thread.__init__(self)
        self.running =  True
        self.HumacClient = HumacClient
        self.modules = modules
        self.type=HumacClient['type']
        self.broker = HumacClient['broker']
        self.port = HumacClient['port']
        self.topic = HumacClient['baseTopic']
        self.tenantid = HumacClient['tenantid']
        self.machineid = HumacClient['machineid']
        self.edgeid=str(HumacClient['edgeid']).lower()
        self.Database = SQLiteEventStorage()
        self.client = mqtt.Client(client_id="HumacGateway",clean_session=False,reconnect_on_failure=True)
        self.client.reconnect_delay_set(1,5)
        self.password = str(HumacClient['password']).lower()
        if self.password is not None:
            self.password = self.password.encode('utf-8')
        self.client.username_pw_set(username=str(HumacClient['username']).lower(), password=self.password)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message= self.on_message
        self.connected = False
    
    def setup(self,HumacClient=None):
        if HumacClient != None:
            print(HumacClient)
    def connect(self):
            try:
                
                self.client.connect(self.broker, self.port,keepalive=1)
                self.client.loop_start()
                print(f"Attempting to connect to {self.broker}...")
            except Exception as e:
                print(f"Failed to connect to MQTT broker: {e}")
                self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"{self.broker} is connected")
            self.client.subscribe(f"{self.topic}/{self.tenantid}/{self.machineid}/{self.edgeid}/update")


        else:
            print(f"Failed to connect, return code {rc}")
            

    def on_disconnect(self, client, userdata, rc):
        # self.client.loop_stop()
        print("Disconnected from MQTT broker")
        self.connected = False
        self.client.loop_stop()

    def on_message(self,client, userdata, msg):
            print(msg.topic)
            request = json.loads(msg.payload)
            try :
                if self.modules != [] and request['connector']:
                    connectorUpdate=list(request["connector"].keys())[0]
                    for connectors in self.modules :
                        for key ,data in connectors.items():
                            if key == connectorUpdate:
                                data.setup(request['connector'])
                            else:
                                print(f"connector is not present {connectorUpdate}")
                    
            except KeyError  as e:
                print(e)
                self.client.publish(f"{msg.topic}/response",json.dumps({"error":str(e)}))
        
                

    def run(self):
        try :
            self.connect()
            while self.running:
                if self.connected :
                    events = self.Database.get_event_pack()
                    if events != []:
                        for event in events:
                            cureent_data = json.loads(event)
                            if self.type == 'mqtt' and self.connected :
                                result=self.client.publish(f"{self.topic}/{self.edgeid}/telemetry",json.dumps(cureent_data),qos=1)
                                if result.rc != 0 : 
                                    print('client is disconnected')
                                    self.client.loop_stop()
                                    break 
                            elif cureent_data ['ts'] and cureent_data['parameters'] :
                                for key,value in cureent_data['parameters'].items():
                                    
                                    if self.connected :
                                        payload=json.dumps({
                                                        "name":key,
                                                        "ts":cureent_data ['ts'] ,
                                                        "Value":value})
                                        result=self.client.publish(f"{self.topic}/{self.edgeid}/telemetry",payload,qos=1)
                                        if result.rc != 0 : 
                                            print('client is disconnected')
                                            self.client.loop_stop()
                                            break 
                                if not self.connected :
                                    self.client.loop_stop()
                                    break
                        if self.connected:
                            self.Database.event_pack_processing_done()
                else:
                    self.client.loop_stop()
                    self.connect()
                    sleep(5)
        except KeyboardInterrupt as e:
            print(e)
            self.stop()
            

    def stop(self):
            self.running = False                    
# try :
#     mqtt_publisher = MQTTPublisher("dev-broker.humac.live", 1883, "gateway/humac")
#     mqtt_publisher.start() 
# except KeyboardInterrupt :
#     print("Exiting program")              
          



