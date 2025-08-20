#!/usr/bin/env python3
import subprocess
import sys
from collections import defaultdict
import time
import joblib
import pandas as pd
from colorama import Fore, Style
from datetime import datetime
import requests

class HybridDDoSDetector:
    def __init__(self, interface='eth0', model_path='model/ddos_model.pkl'):
        self.interface = interface
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load('model/label_encoder.pkl')

        self.thresholds = {
            'ICMP': 10,
            'UDP': 100,
            'TCP': 200,
            'OTHER': 100
        }
        self.counters = defaultdict(int)
        self.last_time = defaultdict(float)
        self.rates = defaultdict(float)

        self.batch_results = []
        self.last_send_time = time.time()
        self.api_url = "http://192.168.64.1:5000/api/detection"

    def run(self):
        print(f"{Fore.CYAN}# Starting hybrid DDoS detection on {self.interface}{Style.RESET_ALL}\n")

        header = (
            f"{'Datetime':<20} | {'Source IP':<15} | {'Proto':<7} | "
            f"{'Len':>6} | {'Rate(pps)':>10} | {'Count':>6} | {'TTL':>4} | "
            f"{'Thresh':>7} | {'Label':<12} | {'Conf':>5}"
        )
        print(Fore.YELLOW + header + Style.RESET_ALL)
        print(Fore.YELLOW + "-" * len(header) + Style.RESET_ALL)

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
                self.maybe_send_results()
        except KeyboardInterrupt:
            print(Fore.CYAN + "\n# Detection stopped" + Style.RESET_ALL)
            proc.terminate()

    def process_packet(self, packet_data):
        try:
            fields = packet_data.split('|')
            timestamp = float(fields[0])
            dt_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            src_ip = fields[1]
            protocol = fields[2].split()[0] if fields[2] else 'OTHER'
            pkt_len = int(fields[3]) if fields[3] else 0
            ip_proto = int(fields[4]) if fields[4] else 0

            if protocol == '':
                protocol = self._get_proto_name(ip_proto)

            time_diff = timestamp - self.last_time.get(src_ip, timestamp)
            self.last_time[src_ip] = timestamp
            current_rate = 1.0 / time_diff if time_diff > 0 else float('inf')
            self.rates[src_ip] = current_rate

            if time_diff > 1.0:
                self.counters[src_ip] = 0
            self.counters[src_ip] += 1

            data = {
                'protocol_ICMP': 1 if protocol == 'ICMP' else 0,
                'protocol_TCP': 1 if protocol == 'TCP' else 0,
                'protocol_UDP': 1 if protocol == 'UDP' else 0,
                'pkt_len': pkt_len,
                'pkt_rate': min(current_rate, 1000000),
                'pkt_count': self.counters[src_ip],
                'ip_ttl': 64
            }
            df = pd.DataFrame([data])[self.model.feature_names_in_]

            ml_pred = self.model.predict(df)
            ml_label_raw = self.label_encoder.inverse_transform(ml_pred)[0]
            ml_prob = self.model.predict_proba(df).max()

            label_map = {
                "DDOS-Attack": "DDOS-Attack",
                "DDoS Attack": "DDOS-Attack",
                "ddos_attack": "DDOS-Attack",
                "Attack": "DDOS-Attack",
                "Normal": "Normal",
                "normal": "Normal",
                "1": "Normal",
                "0": "DDOS-Attack"
            }
            ml_label = label_map.get(ml_label_raw, "Normal")

            threshold = self.thresholds.get(protocol, self.thresholds['OTHER'])
            threshold_label = "Normal"
            if self.counters[src_ip] > threshold:
                threshold_label = "DDOS-Attack"
            elif protocol == "ICMP" and current_rate > 1000:
                threshold_label = "DDOS-Attack"
            elif protocol == "UDP" and current_rate > 500:
                threshold_label = "DDOS-Attack"

            final_label = ml_label
            if ml_label == "DDOS-Attack" and threshold_label == "Normal":
                if ml_prob < 0.7:
                    final_label = "Normal"
            elif threshold_label == "DDOS-Attack" and ml_label == "Normal":
                final_label = "DDOS-Attack"

            label_color = Fore.GREEN if final_label == "Normal" else Fore.RED

            print(
                f"{dt_str:<20} | "
                f"{src_ip:<15} | "
                f"{protocol:<7} | "
                f"{pkt_len:>6} | "
                f"{current_rate:>10.1f} | "
                f"{self.counters[src_ip]:>6} | "
                f"{64:>4} | "
                f"{threshold:>7} | "
                f"{label_color}{final_label:<12}{Style.RESET_ALL} | "
                f"{ml_prob:>5.2f}"
            )
            sys.stdout.flush()

            safe_rate = 0 if current_rate == float("inf") else round(current_rate, 2)

            self.batch_results.append({
                "datetime": dt_str,
                "src_ip": src_ip,
                "protocol": protocol,
                "pkt_len": pkt_len,
                "pkt_rate": safe_rate,
                "pkt_count": self.counters[src_ip],
                "ttl": 64,
                "threshold": threshold,
                "label": final_label,
                "confidence": round(float(ml_prob), 2)
            })


        except Exception as e:
            print(Fore.RED + f"# Error: {str(e)}" + Style.RESET_ALL)

    def maybe_send_results(self):
        """Kirim hasil batch tiap 10 detik"""
        now = time.time()
        if now - self.last_send_time >= 10 and self.batch_results:
            try:
                response = requests.post(self.api_url, json=self.batch_results, timeout=5)
                if response.status_code == 200:
                    print(Fore.CYAN + f"# Sent {len(self.batch_results)} records to API" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"# API error: {response.status_code}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"# Failed to send data: {str(e)}" + Style.RESET_ALL)
            self.batch_results = []
            self.last_send_time = now

    def _get_proto_name(self, proto_num):
        proto_map = {
            1: "ICMP",
            6: "TCP",
            17: "UDP",
            2: "IGMP",
            88: "EIGRP"
        }
        return proto_map.get(proto_num, f"PROTO_{proto_num}")


if __name__ == '__main__':
    interface = sys.argv[1] if len(sys.argv) > 1 else 'eth0'
    detector = HybridDDoSDetector(interface=interface)
    detector.run()
