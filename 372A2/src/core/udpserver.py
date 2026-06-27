
import socket, threading
from . import session


class UDPServer:
    #pylance type hinting
    sessions: dict[tuple[str, int] | tuple[str, int, int, int], session.Session]

    def __init__(self, ip, port, handler):
        self.handler = handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.sock.bind((ip, port))
        self.sessions = {}
        self.lock = threading.Lock()

    def run_handler(self, sess: session.Session):
        try: self.handler(sess)
        finally: 
            sess.finish()
            with self.lock:
                if self.sessions.get(sess.addr) is sess:
                    del self.sessions[sess.addr]

    def route(self, addr, data):
        with self.lock:
            sess = self.sessions.get(addr)
            if sess is None or sess.isdone():
                sess = session.Session(self.sock, addr)
                self.sessions[addr] = sess
                threading.Thread(target = self.run_handler, args =(sess,), daemon=True).start()
            sess.deliver(data)
            
    def serve(self):
        while True:
            try: data, addr = self.sock.recvfrom(65535)
            except OSError: break
            self.route(addr,data)
    
    def stop(self):
        self.sock.close()