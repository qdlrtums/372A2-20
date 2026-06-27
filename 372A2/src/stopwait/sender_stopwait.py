import socket, time
from ..core import lib



def ssw(filename="input.txt", retrylimit = 20, payloadsize=1024, timeout=0.01, dest=("127.0.0.1", 5001)):
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
    sock.settimeout(timeout)

    start = time.time()
    for i in range(last_seq + 1):
        retries = 0
        while True:
            sock.sendto(packets[i], dest)
            try:
                data, _ = sock.recvfrom(65535)
                _, ack, ptype, _, _ = lib.deserialize(data)
                if ptype == lib.TYPE_ACK and ack == i: break
            except socket.timeout:
                retries += 1
                if retries >= retrylimit:
                    print(f"FAILED {i}")
                    break
    elapsed = time.time()- start
    print("done")
    sock.close()
    return elapsed
