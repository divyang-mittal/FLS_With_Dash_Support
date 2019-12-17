import rpyc
from ipyparallel import Client
from rpyc.utils.server import ThreadedServer

class DiscoveryService(rpyc.Service):
    def __init__(self) :
        pass
        
    exposed_my_port = 11111
    ALIASES = ["Discovery"]
    
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
        global peercount
        peercount += 1
        global dict_get_id
        global dict_get_port
        dict_get_id.update({port : peercount})
        dict_get_port.update({peercount : port})
        
    def exposed_get_id(self, port):
        global dict_get_id
        return dict_get_id[port]
    
    def exposed_get_port(self, port_id):
        global dict_get_port
        return dict_get_port[port_id]

if __name__ == "__main__":
	port = 11111
	peercount = 0
	quality_index = 10
	dict_get_id = {}          # key is port
	dict_get_port = {}        # key is id
	dict_leader_quality = {}  # key is id
	dict_of_networks = {}     # key is id
	list_of_leaders = []
	t=ThreadedServer(DiscoveryService,port=port,protocol_config={'allow_setattr':True,'allow_public_attrs':True})
	print("Starting the server")
	t.start()
