import threading
import paho.mqtt.client as TargetClient
import json
from time import time,sleep
from storage.sqlite_event_storage import SQLiteEventStorage

class MqttConnector(threading.Thread):
    def __init__(self,Connconfig):
        threading.Thread.__init__(self)
        self.running =  True
        self.ConneConfig = Connconfig['mqtt']
        self.targetBroker = self.ConneConfig.get('targetBroker')
        self.port = self.ConneConfig.get('port')
        self.username=self.ConneConfig.get('username')
        self.password = self.ConneConfig.get('password')
        self.subscribeTopic=self.ConneConfig.get('subscribeTopic')
        self.client = TargetClient.Client()
        self.client.reconnect_delay_set(1,5)
        if self.password is not None:
            self.password = self.password.encode('utf-8')
        self.client.username_pw_set(username=str(self.username).lower(), password=self.password)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message= self.on_message
        self.connected = False
        # self.client.on_subscribe= self.on_subscribe
        self.Database = SQLiteEventStorage()

    def connect(self):
            try:
                self.client.connect(self.targetBroker, self.port,keepalive=30)
                self.client.loop_start()
                print(f"Attempting to connect to {self.targetBroker} ...")
            except Exception as e:
                print(f"Failed to connect to MQTT broker: {self.targetBroker} : {e}")
                self.client.loop_stop()

    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f" {self.targetBroker } is connected")
            self.client.subscribe(self.subscribeTopic)


        else:
            print(f"Failed to connect, {self.targetBroker}")
    
    # def on_subscribe(cself,lient, userdata, mid, reason_code_list, properties):
    # # Since we subscribed only for a single channel, reason_code_list contains
    # # a single entry
    #     if reason_code_list[0].is_failure:
    #         print(f"Broker rejected you subscription: {reason_code_list[0]}")
    #     else:
    #         print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_message(self,client, userdata, msg):
            print(f' Topic : {msg.topic}')
            try :
                payload_str = msg.payload.decode("utf-8")
                payload = json.loads(payload_str)
                self.Database.put(json.dumps(payload))
                # payload = json.loads(msg.payload.decode("utf-8"))
                print(payload)
                # self.Database.put(json.dumps(payload))
                sleep(0.1)
            except Exception as e:
                print(f"\njson decode error {e}")
                
    def on_disconnect(self, client, userdata, rc):
        # self.client.loop_stop()
        print(f"Disconnected from MQTT broker {self.targetBroker}")
        self.connected = False
        self.client.loop_stop()

    def run(self):
        self.connect()
        while True:
            if self.connected == False:
                try:
                    print('try to connected mqtt broker')
                    self.connect()
                    sleep(5)
                    if self.connected == False:
                        try:
                            self.client.loop_stop()
                        except Exception as e:
                            print('error to connecte mqtt target broker')
                except Exception as e:
                    print('error to connecte mqtt target broker')
            sleep(5)
        
    def stop(self):
        self.running=False
        self.client.disconnect()
        print('stop mqtt connecter ')






