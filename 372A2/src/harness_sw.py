import threading, time
from src.core.udpserver import UDPServer
from src.stopwait.receiver_stopwait import stopwait_handler
from src.stopwait.sender_stopwait import ssw



def run_once(path, loss, port=5000, payloadsize=8192, timeout=0.03, retrylimit=20):
    handler = lambda s: stopwait_handler(s, loss)
    server = UDPServer("127.0.0.1", port, handler)
    t = threading.Thread(target=server.serve, daemon=True)
    t.start()
    time.sleep(0.2)
    elapsed = ssw(filename=path, payloadsize=payloadsize, timeout=timeout, retrylimit=20, dest=("127.0.0.1", port))
    server.stop()
    t.join(timeout=1)
    return elapsed



