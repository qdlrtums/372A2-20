import threading, time
from src.core.udpserver import UDPServer
from src.gbn.receiver_gbn import gbn_handler
from src.gbn.sender_gbn import sgbn



def run_once(path, loss, port=5000, payloadsize=8192, timeout=0.03, windowsize=4):
    handler = lambda s: gbn_handler(s, loss, 3)
    server = UDPServer("127.0.0.1", port, handler)
    t = threading.Thread(target=server.serve, daemon=True)
    t.start()
    time.sleep(0.2)
    elapsed, retransmits = sgbn(filename=path, payloadsize=payloadsize, timeout=timeout, windowsize=windowsize, dest=("127.0.0.1", port))
    server.stop()
    t.join(timeout=1)
    return elapsed, retransmits



