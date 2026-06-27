import os, random
from ..core import lib, session, udpserver

def stopwait_handler(session, loss_rate=0, active_timeout=2, drain_timeout=15):
    expected_seq = 0
    out_file = None
    finished = False

    while True:
        data = session.recv(timeout= drain_timeout if finished else active_timeout)
        if data is None: break
        if random.random() < loss_rate: continue

        seq,ack,ptype, checksum, payload = lib.deserialize(data)

        if seq == expected_seq:
            if ptype == lib.TYPE_START:
                out_file = open("received_sw_" + os.path.basename(payload.decode()), "wb")
            elif ptype == lib.TYPE_DATA: out_file.write(payload)
            elif ptype == lib.TYPE_END:  
                out_file.close()
                finished = True
            session.send(lib.serialize(0, seq, lib.TYPE_ACK))
            expected_seq += 1
        
        elif expected_seq > 0:
            session.send(lib.serialize(0, expected_seq-1, lib.TYPE_ACK))


def rsw(LISTEN_IP, LISTEN_PORT, lr, at, dt):
    f = lambda s: stopwait_handler(s, lr, at, dt)
    u = udpserver.UDPServer(LISTEN_IP, LISTEN_PORT, f)
    u.serve()
