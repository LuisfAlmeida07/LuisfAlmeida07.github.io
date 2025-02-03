import socket
import threading
import ipaddress
import requests
import time
from scapy.all import *
import logging
from queue import Queue
import dns.resolver
import dns.reversename

# Configure logging
logging.basicConfig(
    filename="network_scanner.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# PositionStack API Key (optional)
POSITIONSTACK_API_KEY = "YOUR_POSITIONSTACK_API_KEY"  # Replace with your PositionStack API key (if using)

# Function to resolve a DNS to a public IP
def resolve_dns_to_ip(dns_name):
    try:
        ip_address = socket.gethostbyname(dns_name)
        print(f"DNS {dns_name} resolved to IP: {ip_address}")
        logging.info(f"DNS {dns_name} resolved to IP: {ip_address}")
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving DNS {dns_name}: {e}")
        logging.error(f"Error resolving DNS {dns_name}: {e}")
        return None

# Geocoding: Nominatim (OpenStreetMap)
def reverse_geocode_nominatim(lat, lon):
    try:
        if lat is None or lon is None:
            return "Reverse geocoding not applicable"
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {"User-Agent": "network-scanner/1.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "address" in data:
                return data["display_name"]
            else:
                return "Address not found"
        else:
            return f"Failed to connect to Nominatim API (Status: {response.status_code})"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during Nominatim geocoding: {e}")
        return f"Error during Nominatim geocoding: {e}"

# Geocoding: PositionStack (if API Key available)
def reverse_geocode_positionstack(lat, lon):
    try:
        if lat is None or lon is None or not POSITIONSTACK_API_KEY:
            return "Reverse geocoding not applicable"
        url = f"http://api.positionstack.com/v1/reverse?access_key={POSITIONSTACK_API_KEY}&query={lat},{lon}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                return data["data"][0]["label"]
            else:
                return "Address not found"
        else:
            return f"Failed to connect to PositionStack API (Status: {response.status_code})"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during PositionStack geocoding: {e}")
        return f"Error during PositionStack geocoding: {e}"

# Geocoding: BigDataCloud
def reverse_geocode_bigdatacloud(lat, lon):
    try:
        if lat is None or lon is None:
            return "Reverse geocoding not applicable"
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "locality" in data and data["locality"]:
                return f"{data.get('locality', 'Unknown locality')}, {data.get('principalSubdivision', 'Unknown region')}, {data.get('countryName', 'Unknown country')}"
            else:
                return "Address not found"
        else:
            return f"Failed to connect to BigDataCloud API (Status: {response.status_code})"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during BigDataCloud geocoding: {e}")
        return f"Error during BigDataCloud geocoding: {e}"

# Unified reverse geocoding function with fallback
def reverse_geocode(lat, lon):
    for geocode_function in [reverse_geocode_nominatim, reverse_geocode_positionstack, reverse_geocode_bigdatacloud]:
        address = geocode_function(lat, lon)
        if "not found" not in address.lower() and "error" not in address.lower():
            return address
    return "Unable to determine address"

# Function to perform geolocation lookup
def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "fail":
                return {
                    "location": "Private IP or Unknown location",
                    "latitude": None,
                    "longitude": None,
                }
            location = f"{data.get('city', 'Unknown city')}, {data.get('regionName', 'Unknown region')}, {data.get('country', 'Unknown country')}"
            return {
                "location": location,
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
            }
        else:
            return {"location": "Error fetching location", "latitude": None, "longitude": None}
    except Exception as e:
        logging.error(f"Error fetching geolocation for {ip} - {e}")
        return {"location": "Error fetching location", "latitude": None, "longitude": None}

# Function to retrieve the NetBIOS name of a remote system
def query_netbios(ip):
    """
    Query the remote machine for its NetBIOS name.
    :param ip: Target IP address.
    :return: NetBIOS name or an error message.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)  # Increase timeout to 5 seconds
        netbios_request = b'\x81\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        s.sendto(netbios_request, (ip, 137))
        response, _ = s.recvfrom(1024)
        netbios_name = response[57:73].decode("ascii").strip()
        return f"NetBIOS Name: {netbios_name}"
    except socket.timeout:
        return "NetBIOS query timed out. UDP port 137 might be closed or blocked."
    except Exception as e:
        logging.error(f"NetBIOS query failed for {ip}: {e}")
        return f"NetBIOS query failed: {e}"

# Function to perform a single port scan
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    banner = s.recv(1024).decode("utf-8").strip()
                    logging.info(f"{ip}:{port} is open - Service: {banner}")
                    print(f"[OPEN] {ip}:{port} - Service: {banner}")
                except Exception:
                    logging.info(f"{ip}:{port} is open - Service: Unknown")
                    print(f"[OPEN] {ip}:{port} - Service: Unknown")
            else:
                logging.info(f"{ip}:{port} is closed")
    except Exception as e:
        logging.error(f"Error scanning {ip}:{port} - {e}")

# Function to scan all ports
def port_scanner(ip, delay=0.1):
    for port in range(1, 443):
        scan_port(ip, port)
        time.sleep(delay)

# Function for OS fingerprinting
def os_fingerprinting(ip):
    try:
        response = sr1(IP(dst=ip) / ICMP(), timeout=2, verbose=False)
        if response:
            ttl = response.ttl
            if ttl <= 64:
                os = "Linux/Unix or iOS"
            elif ttl <= 128:
                os = "Windows or iOS"
            else:
                os = "Unknown"
            logging.info(f"{ip} - OS: {os}")
            print(f"[INFO] {ip} - OS: {os}")
        else:
            logging.warning(f"No response from {ip} for OS fingerprinting.")
    except Exception as e:
        logging.error(f"Error fingerprinting OS for {ip} - {e}")

# Worker function
def worker(queue):
    while not queue.empty():
        target = queue.get()
        try:
            ip = target
            geo_data = get_geolocation(ip)
            location = geo_data["location"]
            lat = geo_data["latitude"]
            lon = geo_data["longitude"]


            # Get reverse geocoded address
            address = reverse_geocode(lat, lon) if lat and lon else location

            print(f"Scanning {ip} ({location})...")
            print(f"Approximate Address: {address}")
            logging.info(f"Starting scan on {ip} ({location}) - Address: {address}")

            start_time = time.time()
            port_scanner(ip, delay=0.1)
            os_fingerprinting(ip)
            end_time = time.time()

            duration = end_time - start_time
            print(f"Scan completed for {ip}. Duration: {format_duration(duration)}")
            logging.info(f"Scan completed for {ip}. Duration: {format_duration(duration)}")

        except Exception as e:
            logging.error(f"Error scanning {target} - {e}")
        finally:
            queue.task_done()

# Format duration into HH:MM:SS
def format_duration(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Main function
def main():
    print("Advanced Network Scanner with Free Geocoding APIs")
    target_input = input("Enter target IPs, DNS names (comma-separated), or CIDR range: ")

    # Parse input
    try:
        targets = []
        if '/' in target_input:
            targets = [str(ip) for ip in ipaddress.IPv4Network(target_input, strict=False)]
        else:
            raw_targets = [t.strip() for t in target_input.split(",")]
            for t in raw_targets:
                try:
                    ipaddress.ip_address(t)
                    targets.append(t)
                except ValueError:
                    resolved_ip = resolve_dns_to_ip(t)
                    if resolved_ip:
                        targets.append(resolved_ip)
    except Exception as e:
        print(f"Error parsing inputs: {e}")
        return

    # Prepare the queue
    queue = Queue()
    for ip in targets:
        queue.put(ip)

    # Start scanning
    overall_start_time = time.time()
    threads = []
    for _ in range(min(len(targets), 10)):        
        t = threading.Thread(target=worker, args=(queue,))
        t.start()
        threads.append(t)

    queue.join()
    for t in threads:
        t.join()

    overall_end_time = time.time()
    total_duration = overall_end_time - overall_start_time
    print(f"Scanning complete. Total Duration: {format_duration(total_duration)}")
    logging.info(f"Scanning complete. Total Duration: {format_duration(total_duration)}")

if __name__ == "__main__":
    main()

