import rpyc
import time
from rpyc.utils.server import ThreadedServer
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
rpyc.core.protocol.DEFAULT_CONFIG['allow_setattr'] = True
rpyc.core.protocol.DEFAULT_CONFIG['allow_public_attrs'] = True


class PeerModule():
    class PeerService(rpyc.Service):
        exposed_mycount = 0
        hello = "Hello"
        def __init__(self):
            pass
        
        def on_connect(self, conn):
            # code that runs when a connection is created
            # (to init the service, if needed)
            print("Somebody connected to peer1")
            pass

        def on_disconnect(self, conn):
            # code that runs after the connection has already closed
            # (to finalize the service, if needed)
            print("Somebody disconnected from peer1")
            pass

        def exposed_check(self, port):
            return port
        
        def exposed_request_connect(self, port):
            import rpyc
            global connector_peer
            connector_peer =  rpyc.connect("localhost", port, config = rpyc.core.protocol.DEFAULT_CONFIG)
            # global count_peer
            # count_peer += 1

    def __init__(self, port, quality, server_port):
        self.port = port
        self.quality = quality
        self.is_leader = False
        self.count_peer = 0
        connection_server = rpyc.connect("localhost", server_port, config = rpyc.core.protocol.DEFAULT_CONFIG)
        connection_server.root.update(port)
        self_id = connection_server.root.get_id(port)
        self.list_of_peers = connection_server.root.get_network(self_id, quality)
        print("MY Port :",  self.port)
        t = ThreadedServer(self.PeerService, port=self.port, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
        t.start()
        # time.sleep(1)
        print("Hello")
        for peer in self.list_of_peers:
            peer_port = connection_server.root.get_port(peer)
            print(peer_port)
            connection_peer = rpyc.connect("localhost", peer_port, config = rpyc.core.protocol.DEFAULT_CONFIG)
            print("one down")
            connection_peer.root.request_connect(port)
            print("Hi there")
            self.count_peer += 1
        if(self.count_peer == 0):
            self.is_leader = True
    