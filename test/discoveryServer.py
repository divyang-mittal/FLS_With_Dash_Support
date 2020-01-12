import serverModule
import time
import rpyc
from ipyparallel import Client
from rpyc.utils.server import ThreadedServer

if __name__ == "__main__":
	discovery = serverModule.ServerModule(11111, 10)  // start server with port number and quality consideration index as parameters
