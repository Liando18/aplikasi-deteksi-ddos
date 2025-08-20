import os
import platform
import joblib
import pandas as pd
from scapy.all import sniff, IP
from sklearn.preprocessing import LabelEncoder

# ---- Load model ----
model_path = 'model/result/ddos_model.sav'
if not os.path.exists(model_path):
    print(f"Model {model_path} tidak ditemukan!")
    exit()

model = joblib.load(model_path)
print("Model berhasil dimuat.\n")

# ---- Setup label encoder untuk Protocol ----
protocol_le = LabelEncoder()
protocol_le.fit(['ICMP', 'TCP', 'UDP'])

last_time = None  

# ---- Fungsi konversi paket ke fitur ----
def packet_to_features(pkt):
    global last_time
    try:
        if IP in pkt:
            now = pkt.time
        delta = now - last_time if last_time else 0.0
        last_time = now

        frame_len = len(pkt)
        ip_ttl = pkt[IP].ttl
        ip_len = frame_len
        proto_map = {1:'ICMP', 6:'TCP', 17:'UDP'}
        proto_name = proto_map.get(pkt[IP].proto, 'Other')
        if proto_name not in protocol_le.classes_:
            return None
        proto_enc = protocol_le.transform([proto_name])[0]

        return [delta, frame_len, ip_ttl, ip_len, proto_enc, proto_name]

    except:
        return None

# ---- Fungsi callback sniff ----
def process_packet(pkt):
    features = packet_to_features(pkt)
    if features:
        df_features = pd.DataFrame([features[:5]], columns=['frame.time_delta','frame.len','ip.ttl','ip.len','Protocol'])
        pred = model.predict(df_features)[0]
        pred_label = 'Normal' if pred==0 else 'DDOS-Attack'

        # Tampilkan semua atribut + prediksi langsung
        print(f"frame.time_delta: {features[0]:.6f} | frame.len: {features[1]} | ip.ttl: {features[2]} | ip.len: {features[3]}")
        print(f"Protocol: {features[5]} | Prediksi: {pred_label}\n")

# ---- Main ----
if __name__ == "__main__":
    os_name = platform.system()
    print(f"Menjalankan sniffing pada OS: {os_name}")
    print("Tekan Ctrl+C untuk berhenti...")

    # Pilih interface default (Mac: en0, Windows: Ethernet/Wi-Fi, Linux: eth0/wlan0)
    iface = None
    if os_name == 'Darwin':
        iface = 'en0'
    elif os_name == 'Linux':
        iface = 'eth0'
    elif os_name == 'Windows':
        iface = 'Ethernet'  # sesuaikan nama interface Windows
    else:
        print("OS tidak dikenali, gunakan iface manual")
        exit()

    try:
        sniff(iface=iface, prn=process_packet, store=0)
    except PermissionError:
        print("Permission denied! Jalankan dengan sudo/Administrator atau gunakan ChmodBPF di Mac.")
    except KeyboardInterrupt:
        print("\nScript dihentikan.")
