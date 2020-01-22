import rpyc
import time
import threading
from rpyc.utils.server import ThreadedServer
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
rpyc.core.protocol.DEFAULT_CONFIG['allow_setattr'] = True
rpyc.core.protocol.DEFAULT_CONFIG['allow_public_attrs'] = True



class server (threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
    def run(self):
        t = ThreadedServer(PeerService, port=self.port, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
        t.start()


class RequestConnect(object):
    def __init__(self,port):
        self.conPort = port
        print("In request connect")

    def requestCon(self):
        global connection_peer;
        global count_peer;
        connection_peer.append(rpyc.connect("localhost", self.conPort, config = rpyc.core.protocol.DEFAULT_CONFIG))
        count_peer +=1
        print("Update Peer count",count_peer)

class PeerService(rpyc.Service):
        exposed_mycount = 0
        hello = "Hello"
        def __init__(self):
            pass
        
        def on_connect(self, conn):
            # code that runs when a connection is created
            # (to init the service, if needed)
            print("Somebody connected to me")
            time.sleep(5)
            pass

        def on_disconnect(self, conn):
            # code that runs after the connection has already closed
            # (to finalize the service, if needed)
            print("Somebody disconnected from me")
            pass

        def exposed_check(self, port):
            return port

        def exposed_get_object(self, port):
            obj = RequestConnect(port)
            return obj
        
class PeerModule():

    def __init__(self, port, quality, server_port):
        self.port = port
        self.quality = quality
        self.is_leader = False
        global count_peer
        count_peer = 0
        connection_server = rpyc.connect("localhost", server_port, config = rpyc.core.protocol.DEFAULT_CONFIG)
        connection_server.root.update(port)
        self_id = connection_server.root.get_id(port)
        self.list_of_peers = connection_server.root.get_network(self_id, quality)
        # time.sleep(1)
        thread = server(self.port)
        thread.start()
        print("Hello")
        print("My port", self.port)
        global connection
        global connection_peer 
        connection = []
        connection_peer = []
        for peer in self.list_of_peers:
            peer_port = connection_server.root.get_port(peer)
            print("Peer PORT",peer_port)
            connection_peer.append(rpyc.connect("localhost", peer_port, config = rpyc.core.protocol.DEFAULT_CONFIG))
            connection.append(connection_peer[count_peer].root.get_object(self.port))
            connection[count_peer].requestCon()
            count_peer += 1
        if(count_peer == 0):
            self.is_leader = True
        print("My Port :",  self.port)
        print("Is Leader?:", self.is_leader)
        print("Number of peers", count_peer)
        