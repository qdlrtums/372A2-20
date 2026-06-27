import socket
import time
import lib

DEST = ("127.0.0.1", 5000)
WINDOW_SIZE = 4
TIMEOUT = 0.5
PAYLOAD_SIZE = 1024
FILENAME = "input.txt"

packets = []
seq = 0
packets.append(lib.serialize(seq, 0, lib.TYPE_START, FILENAME.encode()))
seq += 1
with open(FILENAME, "rb") as f:
    while True:
        chunk = f.read(PAYLOAD_SIZE)
        if not chunk:
            break
        packets.append(lib.serialize(seq, 0, lib.TYPE_DATA, chunk))
        seq += 1
packets.append(lib.serialize(seq, 0, lib.TYPE_END))
last_seq = seq

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.05)

base = 0
nextseqnum = 0
timer_start = None

while base <= last_seq:
    while nextseqnum < base + WINDOW_SIZE and nextseqnum <= last_seq:
        sock.sendto(packets[nextseqnum], DEST)
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

    if timer_start is not None and time.time() - timer_start >= TIMEOUT:
        timer_start = time.time()
        for s in range(base, nextseqnum):
            sock.sendto(packets[s], DEST)

print("done")
sock.close()