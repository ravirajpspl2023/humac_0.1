import json
import os 
# import threading
from time  import sleep

class HumacConfig():
    def __init__(self,configPath,HumacConf,ConneConf,lock):
        # threading.Thread.__init__(self) 
        self.running =  True
        self.configpath = configPath
        self.HumacConf = HumacConf
        self.ConneConf = ConneConf
        self.lock = lock
        self.HumacConfig()
        
    def updateConfig(self,mes):
        with self.lock:
            self.HumacConf.update(mes)
        try: 
            with open(self.configpath,'w') as file:
                json.dump(self.HumacConf,file,indent=4)
        except Exception as e:
            print(e)
        print(f"updated {mes['Humac_client']}")

    def HumacConfig(self):
        if os.path.exists(self.configpath):
            print('file is exist')
            try:
                with open(self.configpath,'r') as Humac_config :
                    with self.lock:
                        self.HumacConf.update(json.load(Humac_config))

                for connector in self.HumacConf['connectors']:
                    with open(connector['configPath'],"r") as configPath:
                       with self.lock :
                           self.ConneConf.update({connector['type']:json.load(configPath)})
            except Exception as e:
                    print(f"load config {e}")
        else:
            print("file is not exists")

    # def run(self) :
    #         while self.running :
    #             try:
    #                  sleep(1)
    #             except KeyboardInterrupt as e :
    #                 self.stop()

    # def stop(self):
    #     self.running=False

            
            
