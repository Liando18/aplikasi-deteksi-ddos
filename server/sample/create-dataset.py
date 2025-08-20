import csv
import random
from datetime import datetime, timedelta

# Konfigurasi Dataset
TOTAL_SAMPLES = 10_000  # Total sampel
DDoS_RATIO = 0.3        # 30% DDoS, 70% Normal

# Threshold DDoS
DDoS_RATE_THRESHOLD = 800  # packets/sec
DDoS_COUNT_THRESHOLD = 12  # packets/window

def generate_normal_traffic(num_samples):
    data = []
    for _ in range(num_samples):
        protocol = random.choices(
            ['TCP', 'UDP', 'ICMP'],
            weights=[0.6, 0.35, 0.05]  # ICMP jarang di traffic normal
        )[0]
        
        pkt_len = random.randint(64, 1500)
        rate = random.uniform(1, 500)  # Rate normal
        count = random.randint(1, 8)   # Count rendah
        ttl = random.choice([64, 128, 255])  # TTL bervariasi
        
        data.append([
            protocol,
            pkt_len,
            round(rate, 1),
            count,
            ttl,
            'Normal'
        ])
    return data

def generate_ddos_traffic(num_samples):
    data = []
    for _ in range(num_samples):
        protocol = random.choices(
            ['ICMP', 'UDP', 'TCP'],  # Jenis serangan
            weights=[0.7, 0.2, 0.1]  # Dominan ICMP Flood
        )[0]
        
        if protocol == 'ICMP':
            pkt_len = 60  # Paket kecil
            rate = random.uniform(DDoS_RATE_THRESHOLD, 30_000)
        elif protocol == 'UDP':
            pkt_len = random.choice([60, 512, 1024])
            rate = random.uniform(DDoS_RATE_THRESHOLD, 25_000)
        else:  # TCP SYN Flood
            pkt_len = 64
            rate = random.uniform(DDoS_RATE_THRESHOLD, 40_000)
        
        count = random.randint(DDoS_COUNT_THRESHOLD, 50)
        ttl = random.choice([64, 128])  # TTL seragam
        
        data.append([
            protocol,
            pkt_len,
            round(rate, 1),
            count,
            ttl,
            'DDOS-Attack'
        ])
    return data

# Generate dataset
normal_data = generate_normal_traffic(int(TOTAL_SAMPLES * (1 - DDoS_RATIO)))
ddos_data = generate_ddos_traffic(int(TOTAL_SAMPLES * DDoS_RATIO))

# Gabungkan dan acak
all_data = normal_data + ddos_data
random.shuffle(all_data)

# Header CSV (tanpa src_ip)
header = [
    'protocol', 'pkt_len', 'pkt_rate', 
    'pkt_count', 'ip_ttl', 'label'
]

# Simpan ke CSV
with open('ddos_dataset_model_training.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_data)

print(f"Dataset generated: {len(all_data)} samples")
print(f"Normal: {len(normal_data)} | DDoS: {len(ddos_data)}")
print("\n5 sampel acak:")
for row in random.sample(all_data, 5):
    print(row)