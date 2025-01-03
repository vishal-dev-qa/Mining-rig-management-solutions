import subprocess
import re
import ipaddress
import psutil

#MAC Address of Miners for filtering
MINERS_MAC_ADDRESSES = ["00:15:5d:ad:3f:a8", "00:15:5d:23:6e:e9"]

#get_arp_entries returns the arp entries with mac addresses.
def get_arp_entries():
    """Fetch ARP table entries and extract IP and MAC addresses."""
    print("Fetching ARP table...")
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        arp_entries = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]+)', result.stdout)
        return [(ip, mac.upper()) for ip, mac in arp_entries]
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch ARP table: {e}")
        return []

#get_subnet returns current subnet, currently we are not using it but added if need it.
def get_subnet():
    """Automatically detect the subnet of the current machine."""
    print("Detecting subnet...")
    interfaces = psutil.net_if_addrs()
    for _, addrs in interfaces.items():
        for addr in addrs:
            if addr.family.name == 'AF_INET':  # IPv4 address
                ip = addr.address
                netmask = addr.netmask
                if ip and netmask:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    print(f"Detected Subnet: {network}")
                    return str(network)
    raise ValueError("Could not detect subnet. Please check your network configuration.")

#filter_miners_by_mac filtering devices behalf of miner's mac addresses.
def filter_miners_by_mac(arp_entries):
    """Filter ARP entries by MAC address prefixes."""
    print("Filtering miners by MAC address prefixes...")
    miners = []
    for ip, mac in arp_entries:
        if mac.upper() in (addr.upper() for addr in MINERS_MAC_ADDRESSES):
            print(f"[Miner Found] IP: {ip}, MAC: {mac}")
            miners.append({"ip": ip, "mac": mac})
    return miners

#discover_miners discovering the miners
def discover_miners():
    """Main function to discover miners in the network."""
    arp_entries = get_arp_entries()
    if not arp_entries:
        print("No ARP entries found. Ensure the device is on the same network.")
        return []

    # Detect Subnet (if needed for future reference)
    # subnet = get_subnet() // commented as we are not using it

    miners = filter_miners_by_mac(arp_entries)
    
    print("\nFinal List of Miners:")
    for miner in miners:
        print(f" - IP: {miner['ip']}, MAC: {miner['mac']}")
    
    return miners

if __name__ == '__main__':
    miners = discover_miners()
    print("\n Miner Discovery Complete!")