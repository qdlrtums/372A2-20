import os, random
from ..core import lib, udpserver, session

def gbn_handler(session: session.Session, loss_rate=0, timeout=10):
    expected_seq = 0
    out_file = None
    try:
        while True:
            data = session.recv(timeout=timeout)
            if data is None:
                break
            if random.random() < loss_rate:
                continue

            seq, ack, ptype, checksum, payload = lib.deserialize(data)

            if seq == expected_seq:
                if ptype == lib.TYPE_START:
                    name = "recieved_" + os.path.basename(payload.decode())
                    out_file = open(name, "wb")
                elif ptype == lib.TYPE_DATA:
                    out_file.write(payload)
                elif ptype == lib.TYPE_END:
                    out_file.close()

                session.send(lib.serialize(0, expected_seq, lib.TYPE_ACK))
                expected_seq += 1

                if ptype == lib.TYPE_END:
                    break
            else:
                if expected_seq > 0:
                    session.send(lib.serialize(0, expected_seq - 1, lib.TYPE_ACK))
    finally:
        if out_file is not None and not out_file.closed:
            out_file.close()


def rgbn(LISTEN_IP, LISTEN_PORT, lr, t):
    f = lambda g: gbn_handler(g, lr, t)
    u = udpserver.UDPServer(LISTEN_IP, LISTEN_PORT, f)
    u.serve()