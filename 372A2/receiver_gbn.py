import socket
import random
import os
import lib

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 5000
LOSS_RATE = 0.3

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((LISTEN_IP, LISTEN_PORT))

expected_seq = 0
out_file = None

while True:
    data, addr = sock.recvfrom(65535)
    if random.random() < LOSS_RATE:
        continue

    seq, ack, ptype, checksum, payload = lib.deserialize(data)

    if seq == expected_seq:
        if ptype == lib.TYPE_START:
            name = "received_" + os.path.basename(payload.decode())
            out_file = open(name, "wb")
        elif ptype == lib.TYPE_DATA:
            out_file.write(payload)
        elif ptype == lib.TYPE_END:
            out_file.close()

        sock.sendto(lib.serialize(0, seq, lib.TYPE_ACK), addr)
        expected_seq += 1

        if ptype == lib.TYPE_END:
            break
    else:
        if expected_seq > 0:
            sock.sendto(lib.serialize(0, expected_seq - 1, lib.TYPE_ACK), addr)