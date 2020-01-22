import rpyc
import time
from rpyc.utils.server import ThreadedServer
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
rpyc.core.protocol.DEFAULT_CONFIG['allow_setattr'] = True
rpyc.core.protocol.DEFAULT_CONFIG['allow_public_attrs'] = True


class DiscoveryService(rpyc.Service):
    def __init__(self) :
        pass        
    
    def on_connect(self, conn):
        # code that runs when a connection is created
        print("Connected to server")
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        print("Someone Disconnected")
        pass
    
    def exposed_get_network(self, peer_id, quality):
        global dict_leader_quality 
        global list_of_leaders
        global dict_of_networks
        global quality_index
        for leader in list_of_leaders:
            leader_quality = dict_leader_quality[leader]
            print("leader_quality ", leader_quality)
            print("peer_quality ", quality)
            print("quality_index", quality_index)
            if( abs(leader_quality - quality) <= quality_index ) :   # add it to this network
                list_of_ids = dict_of_networks[leader]
                copy_of_ids = list_of_ids.copy()
                copy_of_ids.append(leader)
                list_of_ids.append(peer_id)
                dict_of_networks.update({leader : list_of_ids})
                return copy_of_ids
        list_of_ids = [peer_id]
        list_of_leaders.append(peer_id)
        dict_leader_quality.update({peer_id : quality})
        dict_of_networks.update({peer_id : list_of_ids})
        list_of_ids.clear()
        return list_of_ids
    
    def exposed_update(self, port):                               
        global dict_get_id
        global dict_get_port
        global peercount
        peercount += 1
        dict_get_id.update({port : peercount})
        dict_get_port.update({peercount : port})
        
    def exposed_get_id(self, port):
        global dict_get_id
        return dict_get_id[port]
    
    def exposed_get_port(self, port_id):
        global dict_get_port
        return dict_get_port[port_id]

class ServerModule():
    def __init__(self, serverPort, quality) :
        global dict_get_id
        global dict_get_port
        global peercount
        global dict_leader_quality 
        global list_of_leaders
        global dict_of_networks
        global quality_index
        port = serverPort
        peercount = 0
        quality_index = quality
        dict_get_id = {}          # key is port
        dict_get_port = {}        # key is id
        dict_leader_quality = {}  # key is id
        dict_of_networks = {}     # key is id
        list_of_leaders = []
        t=ThreadedServer(DiscoveryService, port=port, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
        print("Starting the server")
        t.start()


