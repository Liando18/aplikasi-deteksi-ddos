#!/usr/bin/env python3
import subprocess
import sys
from collections import defaultdict
import time
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

class HybridDDoSDetector:
    def __init__(self, interface='eth0', model_path='ddos_model.pkl'):
        self.interface = interface
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load('label_encoder.pkl')
        self.protocol_encoder = LabelEncoder()
        self.protocol_encoder.fit(['ICMP', 'TCP', 'UDP', 'OTHER'])
        
        # Threshold-based fallback
        self.thresholds = {
            'ICMP': 1000,  # packets/sec
            'UDP': 800,
            'TCP': 1500,
            'OTHER': 500
        }
        self.counters = defaultdict(int)
        self.last_time = defaultdict(float)

    def run(self):
        print(f"# Hybrid DDoS Detection started on {self.interface}", file=sys.stderr)
        print("# Using Naive Bayes model + Threshold fallback", file=sys.stderr)
        print("timestamp|src_ip|protocol|pkt_len|pkt_rate|count|method|label|confidence")

        tshark_cmd = [
            'sudo', 'tshark', '-i', self.interface, '-l', '-T', 'fields',
            '-e', 'frame.time_epoch',
            '-e', 'ip.src',
            '-e', '_ws.col.Protocol',
            '-e', 'frame.len',
            '-e', 'ip.proto',
            '-E', 'header=n', '-E', 'separator=|'
        ]

        proc = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        try:
            for line in iter(proc.stdout.readline, b''):
                line = line.decode().strip()
                if line:
                    self.process_packet(line)
        except KeyboardInterrupt:
            print("\n# Detection stopped", file=sys.stderr)
            proc.terminate()

    def process_packet(self, packet_data):
        try:
            fields = packet_data.split('|')
            timestamp = float(fields[0])
            src_ip = fields[1]
            protocol = fields[2].split()[0] if fields[2] else 'OTHER'
            pkt_len = int(fields[3]) if fields[3] else 0
            ip_proto = int(fields[4]) if fields[4] else 0

            # Calculate packet rate
            current_time = time.time()
            time_diff = current_time - self.last_time.get(src_ip, current_time)
            rate = 1.0 / time_diff if time_diff > 0 else float('inf')
            self.last_time[src_ip] = current_time
            self.counters[src_ip] += 1

            # Reset counter if window passed
            if time_diff > 1.0:  # 1-second window
                self.counters[src_ip] = 0

            # Prepare features for ML model
            features = {
                'protocol': protocol,
                'pkt_len': pkt_len,
                'pkt_rate': rate,
                'pkt_count': self.counters[src_ip],
                'ip_ttl': 64  # Default, bisa diganti dengan nilai aktual jika tersedia
            }

            # Convert to DataFrame
            df = pd.DataFrame([features])
            
            # Preprocess like training
            df['protocol'] = self.protocol_encoder.transform(
                df['protocol'].apply(lambda x: x if x in ['ICMP','TCP','UDP'] else 'OTHER')
            )
            
            # Predict with ML model
            ml_pred = self.model.predict(df.values)
            ml_label = self.label_encoder.inverse_transform(ml_pred)[0]
            ml_prob = self.model.predict_proba(df.values).max()

            # Threshold-based verification
            threshold = self.thresholds.get(protocol, self.thresholds['OTHER'])
            threshold_label = "Normal"
            if rate > threshold or self.counters[src_ip] > threshold:
                threshold_label = "DDOS-Attack"

            # Hybrid decision
            final_label = ml_label
            method = "ML"
            
            if ml_label == "DDOS-Attack" and threshold_label == "Normal":
                if ml_prob < 0.9:  # Low confidence
                    final_label = "Normal"
                    method = "ML_OVERRIDE"
            elif threshold_label == "DDOS-Attack" and ml_label == "Normal":
                final_label = "DDOS-Attack"
                method = "THRESHOLD"

            # Output
            print(f"{timestamp:.6f}|{src_ip}|{protocol}|{pkt_len}|"
                  f"{rate:.1f}|{self.counters[src_ip]}|{method}|"
                  f"{final_label}|{ml_prob:.2f}")
            
            sys.stdout.flush()

        except Exception as e:
            print(f"# Error: {e}", file=sys.stderr)

if __name__ == '__main__':
    interface = sys.argv[1] if len(sys.argv) > 1 else 'eth0'
    detector = HybridDDoSDetector(interface=interface)
    detector.run()