import os, threading, time
from src.gbn.receiver_gbn import rgbn
from src.gbn.sender_gbn import sgbn

# with open("input.txt", "wb") as f: f.write(os.urandom(20000))
# threading.Thread(target=rgbn, args=("127.0.0.1", 5000, 0.0, 3), daemon=True).start()
# time.sleep(0.3)
# sgbn(filename="input.txt", dest=("127.0.0.1", 5000))
# time.sleep(0.3)
# print(open("received_input.txt", "rb").read() == open("input.txt", "rb").read())


for i, lr in enumerate((0.0, 0.1, 0.3)):
    port = 5000 + i
    threading.Thread(target=rgbn, args=("127.0.0.1", port, lr, 3), daemon=True).start()
    time.sleep(0.3)
    sgbn(filename="input.txt", dest=("127.0.0.1", port))
    time.sleep(0.3)
    ok = open("recieved_input.txt","rb").read() == open("input.txt","rb").read()
    print(f"loss={lr} match={ok}")
    os.remove("recieved_input.txt")