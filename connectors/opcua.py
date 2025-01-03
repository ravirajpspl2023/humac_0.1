from asyncua import Client
from asyncua import crypto
from asyncua import tools
from asyncua import ua
import asyncua

import asyncio

def newpath(path:str="",idx=str,names=str):
     path = path + f"/{str(idx)}:{str(names)}"
     print(path)
     return path
def getnode(client,ns=0,i=0):
    node = client.get_node(f"ns={str(ns)};i={str(i)}")
    return node

async def main():
    print(f"Connecting to server .... ")

    url = "opc.tcp://DESKTOP-V1DSN94:48020"
    async with Client(url) as client : 
        parent = client.get_root_node()
        discription = await parent.get_children_descriptions()
        for disc in discription:
            # print(disc.NodeClass)
            if disc.NodeClass == 1 :
                # print(disc.BrowseName,disc.BrowseName.NamespaceIndex,disc.NodeClass.name)
                nodes=  getnode(client,disc.BrowseName.NamespaceIndex,disc.NodeId.Identifier)
                chiled = await nodes.get_children_descriptions()
                for chi in chiled :
                    # (print(chi.NodeId.NodeIdType))
                    if chi.NodeId.NodeIdType == 3:
                        new_chi = await nodes.get_child(chi.BrowseName)
                        value_node = await new_chi.get_children_descriptions()
                        for new_values_node in value_node:
                           stap1 = await new_chi.get_child(new_values_node.BrowseName)
                           stap1_disc = await stap1.get_children_descriptions()
                           for stap1_values in stap1_disc:
                               print(stap1_values)
                            #    stap2=stap1.get_child(stap1_values.BrowseName)

                        # print(chi.NodeId.NodeIdType)
                        # print(chi.BrowseName)
                    # if  chi.NodeClass.name == "Object" and chi.NodeId.:
                    #     try:
                    #         na = getnode(client,chi.BrowseName.NamespaceIndex,chi.NodeId.Identifier)
                    #     except Exception as e :
                    #         print(e)
                        
                    #     print(na)
        # node = getnode(client,i=84)
        
        # name = (await node.get_children())
        
        
    
        
    #    root =  await client.nodes.root.get_children_descriptions()
       
    #    children = await client.nodes.root.get_children_descriptions()

    #    objesnode = await client.nodes.objects.get_children_descriptions()

    #    for NOx in root:
    #           name = NOx.BrowseName.Name
    #           idx =  NOx.BrowseName.NamespaceIndex
    #           path = newpath(idx=idx,names=name)
    #         #   print(name,idx)
    #           if name == 'Objects':
    #                try:
    #                    node = await client.nodes.root.get_child(path)
    #                    discription = await node.get_children_descriptions()
    #                    for disc in discription :
    #                         node.get_path()
    #                         name= disc.BrowseName.Name
    #                         idx= disc.BrowseName.NamespaceIndex
    #                         path = newpath(idx=idx,names=name)
                       
    #                except Exception as e:
    #                     print("node have not children")
                    
        #    BrowseName = NOx.BrowseName
        #    print(NOx.NodeClass_,NOx.BrowseName.Name)
           
        #    if NOx.IsForward:
        #     #   print(f"/Objects/{str(BrowseName.NamespaceIndex)}:{str(BrowseName.Name)}")
        #       print()
        #       var = await client.nodes.root.get_child(
        #         f"/Objects/{str(BrowseName.NamespaceIndex)}:{str(BrowseName.Name)}"
        #         )
        #       chi = await var.get_children_descriptions()
        #       for noc in chi:
        #           if noc.NodeClass == 2 :
        #               print(noc)
    #    for reference_description in children:
    #        print()
    #        reference_type_id = reference_description.ReferenceTypeId
    #        is_forward = reference_description.IsForward
    #        print(reference_type_id,is_forward)
    


if __name__ == "__main__":
    asyncio.run(main())

        



    
