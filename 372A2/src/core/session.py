import socket, threading, queue

class Session:
    sock: socket.socket
    done: threading.Event

    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.inbox = queue.Queue()
        self.done = threading.Event()

    def recv(self, timeout = 0.5):
        try: return self.inbox.get(timeout=timeout)
        except queue.Empty: return None
    
    def send(self, data): self.sock.sendto(data, self.addr)
    def deliver(self, data): self.inbox.put(data) 
    def finish(self): self.done.set()
    def isdone(self): return self.done.is_set()


