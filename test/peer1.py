import rpyc
import time
from ipyparallel import Client
from rpyc.utils.server import ThreadedServer

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
        connector_peer =  rpyc.connect("localhost", port)
        global count_peer
        count_peer += 1

def foo(PeerService):
    import rpyc
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(PeerService, port=10061, protocol_config={	# for each peer make changes here to set it's port
    'allow_setattr': True, 'allow_public_attrs': True,
})
    t.start()
    return 'bar'

if __name__ == "__main__":
	port = 10061												 # for each peer make changes here to set it's port
	quality = 5
	is_leader = False
	global connector_peer
	count_peer = 0
	rc = Client()
	lb_view = rc.load_balanced_view()
	print("Profile: %s" % rc.profile)
	print("Engines: %s" % len(lb_view))
	connection_server = rpyc.connect("localhost", 11111)
	connection_server.root.update(port)
	self_id = connection_server.root.get_id(port)
	list_of_peers = connection_server.root.get_network(self_id, quality)
	rc[1].apply(fimport rpyc
import time
from ipyparallel import Client
from rpyc.utils.server import ThreadedServer

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
        connector_peer =  rpyc.connect("localhost", port)
        global count_peer
        count_peer += 1

def foo(PeerService):
    import rpyc
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(PeerService, port=10061, protocol_config={	# for each peer make changes here to set it's port
    'allow_setattr': True, 'allow_public_attrs': True,
})
    t.start()
    return 'bar'

if __name__ == "__main__":
	port = 10061												 # for each peer make changes here to set it's port
	quality = 5
	is_leader = False
	global connector_peer
	count_peer = 0
	rc = Client()
	lb_view = rc.load_balanced_view()
	print("Profile: %s" % rc.profile)
	print("Engines: %s" % len(lb_view))
	connection_server = rpyc.connect("localhost", 11111)
	connection_server.root.update(port)
	self_id = connection_server.root.get_id(port)
	list_of_peers = connection_server.root.get_network(self_id, quality)
	rc[1].apply(foo, PeerService)
	time.sleep(1)
	for peer in list_of_peers:
	    peer_port = connection_server.root.get_port(peer)
	    connection_peer = rpyc.connect("localhost", peer_port)
	    connection_peer.root.request_connect(port)
	    count_peer += 1
	if(count_peer == 0):
	    is_leader = Trueoo, PeerService)
	time.sleep(1)
	for peer in list_of_peers:
	    peer_port = connection_server.root.get_port(peer)
	    connection_peer = rpyc.connect("localhost", peer_port)
	    connection_peer.root.request_connect(port)
	    count_peer += 1
	if(count_peer == 0):
	    is_leader = True
