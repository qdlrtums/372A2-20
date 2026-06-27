import socket
import time
from ..core import lib

def sgbn(filename = "input.txt", payloadsize=1024, timeout=0.01, windowsize=4, dest=("127.0.0.1",5000)):
    packets = []
    seq = 0
    packets.append(lib.serialize(seq, 0, lib.TYPE_START, filename.encode()))
    seq += 1
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(payloadsize)
            if not chunk:
                break
            packets.append(lib.serialize(seq, 0, lib.TYPE_DATA, chunk))
            seq += 1
    packets.append(lib.serialize(seq, 0, lib.TYPE_END))
    last_seq = seq

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.001)

    base = 0
    nextseqnum = 0
    timer_start = None
    
    start = time.time()
    while base <= last_seq:
        while nextseqnum < base + windowsize and nextseqnum <= last_seq:
            sock.sendto(packets[nextseqnum], dest)
            if base == nextseqnum:
                timer_start = time.time()
            nextseqnum += 1

        try:
            data, _ = sock.recvfrom(65535)
            _seq, ack, ptype, _checksum, _payload = lib.deserialize(data)
            if ptype == lib.TYPE_ACK and ack >= base:
                base = ack + 1
                timer_start = time.time() if base <= last_seq else None
        except socket.timeout:
            pass

        if timer_start is not None and time.time() - timer_start >= timeout:
            timer_start = time.time()
            for s in range(base, nextseqnum):
                sock.sendto(packets[s], dest)
    elapsed = time.time() - start

    print("done")
    sock.close()
    return elapsed