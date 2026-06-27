import socket, time, lib

DEST = ("127.0.0.1", 5001)
TIMEOUT = 0.5
PAYLOAD_SIZE = 1024
FILENAME = "input.txt"
RETRY_LIMIT = 20

packets = []
seq = 0
packets.append(lib.serialize(seq, 0, lib.TYPE_START, FILENAME.encode()))
seq += 1
with open(FILENAME, "rb") as f:
    while True:
        chunk = f.read(PAYLOAD_SIZE)
        if not chunk: break

        packets.append(lib.serialize(seq, 0, lib.TYPE_DATA, chunk))
        seq += 1
packets.append(lib.serialize(seq, 0, lib.TYPE_END))
last_seq = seq 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

for i in range(last_seq + 1):
    retries = 0
    while True:
        sock.sendto(packets[i], DEST)
        try:
            data, _ = sock.recvfrom(65535)
            _, ack, ptype, _, _ = lib.deserialize(data)
            if ptype == lib.TYPE_ACK and ack == i: break
        except socket.timeout:
            retries += 1
            if retries >= RETRY_LIMIT:
                print(f"FAILED {i}")
                break

print("done")
sock.close()