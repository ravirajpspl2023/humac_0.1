import threading
from utility.config import HumacConfig
import importlib
from Hum_Client import MQTTPublisher


DEFAULT_CONNECTORS = {
    "mqtt": "MqttConnector",
    "modbus": "ModbusConnector",
    "gpio":"GpioConnector",
    "opcua": "OpcuaConnector"
}

try :
    lock = threading.Lock()
    HumacConf = {}
    ConnecConf = {}
    modules = []
    configration = HumacConfig('./config/config.json',HumacConf,ConnecConf,lock)
    
    connectors = HumacConf['connectors']
    
    for connector in connectors:
        connector_path = f"connectors.{connector['type']}"
        module = importlib.import_module(connector_path)
        module_getter = getattr(module,DEFAULT_CONNECTORS.get(connector['type']),None)
        if module_getter:
            module= module_getter(ConnecConf)
            modules.append({connector['type']:module})
            print(f"connector is loaded {connector['type']}")
            module.start()
            print(f"connector is start {connector['type']}")

    mqtt_publisher = MQTTPublisher(HumacConf['Humac_client'],modules)
    mqtt_publisher.start()

    # for model in modules :
        # model.join()
    mqtt_publisher.join()
except KeyboardInterrupt as e:
    print(e)
print("main script is end")

