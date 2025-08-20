import psutil

def cek_interface():
    interfaces = psutil.net_if_addrs()
    aktif_interfaces = []

    print("Daftar interface jaringan:")
    for iface_name, addrs in interfaces.items():
        ipv4 = None
        status = "Inactive"
        for addr in addrs:
            if addr.family.name == 'AF_INET':  # IPv4
                ipv4 = addr.address
                status = "Active"
        print(f"- {iface_name} | Status: {status} | IPv4: {ipv4}")
        if status == "Active":
            aktif_interfaces.append(iface_name)

    if aktif_interfaces:
        print("\nInterface aktif yang bisa digunakan:")
        for iface in aktif_interfaces:
            print(f"- {iface}")
    else:
        print("Tidak ada interface aktif.")

if __name__ == "__main__":
    cek_interface()
