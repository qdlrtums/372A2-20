import socket
import time
from ..core import lib


def ssr(filename="input.txt", payloadsize=1024, timeout=0.03, windowsize=4, dest=("127.0.0.1", 5000)):
    packets = []
    seq = 0
    packets.append(lib.serialize(seq, 0, lib.TYPE_START, filename.encode()))
    seq += 1
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(payloadsize)
            if not chunk: break
            packets.append(lib.serialize(seq, 0, lib.TYPE_DATA, chunk))
            seq += 1
    packets.append(lib.serialize(seq, 0, lib.TYPE_END))
    last_seq = seq

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.001)

    base = 0
    nextseqnum = 0
    send_time = {}
    acked = set()
    retransmits = 0

    start = time.time()
    while base <= last_seq:
        while nextseqnum < base + windowsize and nextseqnum <= last_seq:
            sock.sendto(packets[nextseqnum], dest)
            send_time[nextseqnum] = time.time()
            nextseqnum += 1

        try:
            data, _ = sock.recvfrom(65535)
            _seq, ack, ptype, _checksum, _payload = lib.deserialize(data)
            if ptype == lib.TYPE_ACK and base <= ack < nextseqnum:
                acked.add(ack)
                send_time.pop(ack, None)
                while base in acked:
                    acked.discard(base)
                    base += 1
        except socket.timeout:
            pass

        now = time.time()
        for s in range(base, nextseqnum):
            if s in acked: continue
            t = send_time.get(s)
            if t is not None and now - t >= timeout:
                sock.sendto(packets[s], dest)
                send_time[s] = now
                retransmits += 1
    elapsed = time.time() - start

    print("done")
    sock.close()
    return elapsed, retransmits
