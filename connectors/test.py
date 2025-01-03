import asyncio
import logging

from asyncua import Client
from asyncua.tools import endpoint_to_strings

_logger = logging.getLogger(__name__)


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("New data change event",node, val)

    def event_notification(self, event):
        print("New event", event)


async def main():
    url = "opc.tcp://DESKTOP-V1DSN94:53530/OPCUA/SimulationServer"
    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        # _logger.info("Objects node is: %r", client.nodes.objects)
        # print(client.nodes.namespaces)
        # Node objects have methods to read and write node attributes as well as browse or populate address space
        # _logger.info("Children of root are: %r", await client.nodes.root.get_children())
        # _logger.info("Children of object are: %r", await client.nodes.objects.get_children())
        # chiled = await client.nodes.objects.get_referenced_nodes()
        # # print(f"get path {chiled}")
        # for i , v in enumerate(chiled,start=1):
        #     print(v)
            
        # await client.nodes.objects.get_children_by_path(chiled)

        # edps = client.connect_and_get_server_endpoints()
        # print(edps)
        # for i, ep in enumerate(edps, start=1):
        #     for (n, v) in endpoint_to_strings(ep):
        #         print(('  %s: %s', n, v))
        # uri = "http://www.prosysopc.com/OPCUA/SimulationServer/"
        # idx = await client.get_namespace_index(uri)
        # _logger.info("index of our namespace is %s", idx)

        # get a specific node knowing its node id
        # var = client.get_node(ua.NodeId(1002, 2))
        # var = client.get_node("ns=3;i=1007")
        # # print(var)
        # await var.read_data_value() # get value of node as a DataValue object
        # await var.read_value() # get value of node as a python builtin
    
        #await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #await var.write_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        # try:
        #     # Counter = await client.nodes.root.get_child("/Objects/3:Simulation/3:Counter")
        #     # Random = await client.nodes.root.get_child("/Objects/3:Simulation/3:Random")
        # except Exception as e :
        #     print('error')
            # print(e)
        # obj = await client.nodes.root.get_child("Objects/")
        # _logger.info("myvar is: %r", myvar)

        # # subscribing to a variable node
        handler = SubHandler()
        # sub = await client.create_subscription(10, handler)
        # handle = await sub.subscribe_data_change(Counter)
        # handle = await sub.subscribe_data_change(Random) 
        # await asyncio.sleep(0.1)

        # # we can also subscribe to events from server
        # await sub.subscribe_events()
        # await sub.unsubscribe(handle)
        # await sub.delete()
        # print(Counter)
        # print(Random)
        # # calling a method on server
        # res = await myvar.call_method("3:Counter", 3, "klk")
        # print(res)
        # _logger.info("method result is: %r", res)
        while True:
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())