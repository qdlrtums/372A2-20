import os, random
from ..core import lib, session, udpserver


def sr_handler(session, loss_rate=0, windowsize=4, active_timeout=2, drain_timeout=15):
    expected_seq = 0
    buffer = {}
    out_file = None
    finished = False

    while True:
        data = session.recv(timeout=drain_timeout if finished else active_timeout)
        if data is None: break
        if random.random() < loss_rate: continue

        seq, ack, ptype, checksum, payload = lib.deserialize(data)

        if seq < expected_seq:
            session.send(lib.serialize(0, seq, lib.TYPE_ACK))
            continue

        if seq >= expected_seq + windowsize: continue

        session.send(lib.serialize(0, seq, lib.TYPE_ACK))
        buffer[seq] = (ptype, payload)

        while expected_seq in buffer:
            ptype_d, payload_d = buffer.pop(expected_seq)
            if ptype_d == lib.TYPE_START:
                out_file = open("received_sr_" + os.path.basename(payload_d.decode()), "wb")
            elif ptype_d == lib.TYPE_DATA:
                out_file.write(payload_d)
            elif ptype_d == lib.TYPE_END:
                out_file.close()
                finished = True
            expected_seq += 1


def rsr(LISTEN_IP, LISTEN_PORT, lr, ws, at, dt):
    f = lambda s: sr_handler(s, lr, ws, at, dt)
    u = udpserver.UDPServer(LISTEN_IP, LISTEN_PORT, f)
    u.serve()
