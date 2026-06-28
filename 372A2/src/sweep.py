import os, csv, time
from src.harness_gbn import run_once
# from src.harness_sw import run_once
# from src.harness_sr import run_once

SIZES = {
    "10K": 10*1024, 
    "50K": 50*1024, 
    "100K": 100*1024,
    "500K": 500*1024, 
    "1M": 1024**2, 
    "5M": 5*1024**2,
    "10M": 10*1024**2, 
    # "50M": 50*1024**2, 
    # "100M": 100*1024**2,
}
LOSSES = (0.0, 0.10, 0.20, 0.30)
RUNS = 5

def ensure_files(folder="testfiles"):

    os.makedirs(folder, exist_ok=True)
    paths = {}
    for label, nbytes in SIZES.items():
        p = os.path.join(folder, f"{label}.bin")
        if not os.path.exists(p) or os.path.getsize(p) != nbytes:
            with open(p, "wb") as f: f.write(os.urandom(nbytes))
        paths[label] = p
    return paths

def main(out="results.csv"):
    paths = ensure_files()


    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)

        w.writerow(["size_label", "size_bytes", "loss", "run", "seconds", "throughput_Bps", "retransmits"])
        for label in SIZES:
            for loss in LOSSES:
                for run in range(1, RUNS + 1):
                    secs, retransmits = run_once(paths[label], loss)
                    received = "recieved_" + os.path.basename(paths[label])


                    if os.path.exists(received): os.remove(received)

                    throughput = SIZES[label] / secs if secs > 0 else 0.0
                    w.writerow([label, SIZES[label], loss, run, f"{secs:.6f}", f"{throughput:.2f}", retransmits])
                    fh.flush()


                    print(f"{label} loss={loss} run={run} {secs:.3f}s tput={throughput/1e6:.2f}MB/s rtx={retransmits}")

if __name__ == "__main__":
    main()