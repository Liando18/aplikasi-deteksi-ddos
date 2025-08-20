import csv
import random
import time
from scapy.all import sniff, IP

# ====== CONFIG ======
REAL_CAPTURE_DURATION = 15   # durasi capture real traffic (detik)
REAL_CAPTURE_FILE = "real_normal.csv"
FINAL_DATASET_FILE = "ddos_dataset_mixed.csv"

NUM_DDOS_SYNTH = 5000        # jumlah paket DDOS sintetis
# ====================


# === Step 1: Capture real normal traffic ===
print(f"[1/3] Capture traffic normal selama {REAL_CAPTURE_DURATION} detik...")
real_data = []

start_time = time.time()
while time.time() - start_time < REAL_CAPTURE_DURATION:
    pkt = sniff(count=1, store=False)
    for p in pkt:
        if IP in p:
            ip_src = p[IP].src
            ip_dst = p[IP].dst
            frame_len = len(p)
            ip_ttl = p[IP].ttl
            ip_len = p[IP].len
            proto_num = p[IP].proto
            time_delta = round(random.uniform(0.001, 1.0), 9)  # jika mau hitung delta asli, bisa pakai variabel global
            proto_name = {1: "ICMP", 6: "TCP", 17: "UDP"}.get(proto_num, "Other")
            icmp_type = None
            label = "Normal"
            real_data.append([ip_src, ip_dst, icmp_type, time_delta, frame_len, ip_ttl, proto_name, ip_len, label])

# Simpan data normal real
with open(REAL_CAPTURE_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ip.src", "ip.dst", "icmp.type", "frame.time_delta", "frame.len", "ip.ttl", "protocol", "ip.len", "label"])
    writer.writerows(real_data)

print(f"✔ Data normal real tersimpan: {REAL_CAPTURE_FILE} ({len(real_data)} paket)")


# === Step 2: Generate synthetic DDOS data ===
print(f"[2/3] Generate {NUM_DDOS_SYNTH} paket DDOS sintetis...")
synthetic_ddos = []
for _ in range(NUM_DDOS_SYNTH):
    time_delta = round(random.uniform(0.00005, 0.005), 9)
    frame_len = random.randint(60, 800)
    ip_ttl = random.choice([32, 64, 128])
    ip_len = frame_len + random.randint(0, 10)
    proto = random.choice(["ICMP", "TCP", "UDP"])
    ip_src = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    ip_dst = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    icmp_type = 8 if proto == "ICMP" else None
    label = "DDOS-Attack"
    synthetic_ddos.append([ip_src, ip_dst, icmp_type, time_delta, frame_len, ip_ttl, proto, ip_len, label])

print("✔ Paket DDOS sintetis dibuat.")


# === Step 3: Gabungkan & simpan final dataset ===
print("[3/3] Gabungkan dataset...")
all_data = real_data + synthetic_ddos

with open(FINAL_DATASET_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ip.src", "ip.dst", "icmp.type", "frame.time_delta", "frame.len", "ip.ttl", "protocol", "ip.len", "label"])
    writer.writerows(all_data)

print(f"✔ Dataset final tersimpan: {FINAL_DATASET_FILE} (Total {len(all_data)} paket)")
