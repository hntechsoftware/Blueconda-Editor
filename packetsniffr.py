# Credit where its due:
from nicegui import ui
import ipaddress
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP, sr1
import requests
from scapy.all import os
from scapy.utils import chexdump
import threading
import binascii
import socket

packet_list = []

ui.query('body').style(f'background-color: #ddeeff')
with ui.row():
    ui.label("NetWatch").style("font-size: 50px; color: #2e6c9e; font-weight: bold; ")
    ui.spinner('radio', size='50px', color='green')

continueupdate = False

def onswitchchange(value):
    global continueupdate
    continueupdate = value.value

with ui.row():
    ui.button("Search By Time", icon="schedule")
    ui.button("Search By Location", icon="room")
    switch = ui.switch("Enable Logging", on_change=onswitchchange)



def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text


def get_ip_location(ip_address): # TODO add dict to store all ips recorded (save on api calls)
    if ipaddress.ip_address(ip_address).is_private:
        return "Private IP"

    url = f"https://api.db-ip.com/v2/free/{ip_address}"
    headers = {
        'User-Agent': 'YourAppName/1.0 (your-email@example.com)'  # Custom User-Agent
    }

    try:
        # Send the request
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', 'Unknown')
            region = data.get('region', 'Unknown')
            country = data.get('country', 'Unknown')
            return f"Location: {city}" ## Reigion and country causes unknown stuff
        else:
            return f"Error: Unable to fetch location. Status Code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        protocol = ip_layer.proto
        src_ip = get_public_ip()
        dst_ip = ip_layer.dst
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(packet.time))
        # Determine the protocol
        protocol_name = ""
        if protocol == 1:
            protocol_name = "ICMP"
        elif protocol == 6:
            protocol_name = "TCP"
        elif protocol == 17:
            protocol_name = "UDP"
        else:
            protocol_name = "Unknown Protocol"

        raw_data = "" # Initialize in case there is no value in packet

        # Print packet details
        #print(f"Protocol: {protocol_name}")
        #print(f"Source IP: {src_ip}")
        #print(f"Destination IP: {dst_ip}")
        #print(packet.show())
        if Raw in packet:
            raw_data = packet[Raw].load
            #try:
                # Attempt to decode it as HTTP
                #print("HTTP Data: ", raw_data.decode('utf-8', errors='ignore'))
            #except UnicodeDecodeError:
                #print("Raw Data (non-UTF-8): ", raw_data)

        

        # TCP or UDP or ICMP Layer Details
        protocol_details = ""

        if protocol == 6:  # TCP protocol
            if TCP in packet:
                tcp_layer = packet[TCP]
                protocol_details = f"TCP Source Port: {tcp_layer.sport}, " \
                                   f"Destination Port: {tcp_layer.dport}, " \
                                   f"Seq: {tcp_layer.seq}, Ack: {tcp_layer.ack}, " \
                                   f"Flags: {tcp_layer.flags}, Window Size: {tcp_layer.window}"

                # Add raw data if it exists
                if Raw in packet:
                    raw_data = packet[Raw].load


        elif protocol == 17:  # UDP protocol
            if UDP in packet:
                udp_layer = packet[UDP]
                protocol_details = f"UDP Source Port: {udp_layer.sport}, " \
                                   f"Destination Port: {udp_layer.dport}"

                # Add raw data if it exists
                if Raw in packet:
                    raw_data = packet[Raw].load

        elif protocol == 1:  # ICMP protocol
            if ICMP in packet:
                icmp_layer = packet[ICMP]
                protocol_details = f"ICMP Type: {icmp_layer.type}, " \
                                   f"Code: {icmp_layer.code}, Checksum: {icmp_layer.chksum}"

        packet_list.append({
            'src_ip': f'{src_ip}, {get_ip_location(src_ip)}',
            'dst_ip': f'{dst_ip}, {get_ip_location(dst_ip)}',
            'protocol': protocol_name,
            'timestamp': timestamp,
            'payload': chexdump(packet.lastlayer(), dump=True),
            'rawdata': raw_data,
            'protocoldetails': protocol_details,

        })

        # Uncomment for testing
        #print(packet_list[len(packet_list) - 1])

packetcontainer = ui.column()


def getOS(target_ip):
    # Send a TCP SYN packet to the target
    try:
        target_ip = socket.gethostbyaddr(target_ip)
    except Exception:
        pass

    pkt = IP(dst=target_ip) / TCP(dport=80, flags="S")
    response = sr1(pkt, timeout=1, verbose=0)

    if response:
        
        # Basic OS detection based on TTL value
        ttl = response.ttl
        if ttl <= 64:
            return "Linux/Unix (likely)"
        elif ttl > 64 and ttl <= 128:
            return "Windows (likely)"
        elif ttl > 128:
            return "Cisco/Router or Other OS"
        else:
            return "Unidentified OS"
    else:
        return "No response received or target unreachable"


def displayinfo():
    if continueupdate:
        packetcontainer.clear()
        for item in packet_list:
            with ui.expansion(f'Packet Scanned: {item["timestamp"]}', icon='router').classes('w-full'):
                with ui.row():
                    columns = [
                        {'name': 'Property', 'label': 'Property', 'field': 'Property', 'required': True, 'align': 'left'},
                        {'name': 'Value', 'label': 'Value', 'field': 'Value'},
                    ]
                    rows = [
                        {'Property': 'Source', 'Value': item['src_ip']},
                        {'Property': 'Destination', 'Value': item['dst_ip']},
                        {'Property': 'Timestamp', 'Value': item['timestamp']},
                        {'Property': 'Protocol', 'Value': item['protocol']},
                        {'Property': 'ProtocolDetails', 'Value': item['protocoldetails']},
                        #{'Property': 'OS', 'Value': getOS(item['src_ip'])},

                    ]
                    ui.table(columns=columns, rows=rows, row_key='Property')
                    with ui.expansion('See HEX Data', caption='Likely Encrypted under TLS'):
                        #for line in item['payload']:
                            #ui.label(line)
                        ui.label(item['payload'])
                        with ui.row():
                            ui.button("Attempt Decode")
                            hexstring = ''.join(part.strip().replace('0x', '') for part in item['payload'].split(','))
                            byte_string = binascii.unhexlify(hexstring)  
                            ascii_string = ascii_string = byte_string.decode("utf-8", errors="ignore")
                            ui.label(ascii_string)
                
                ui.update()

ui.timer(5.0, callback=lambda: displayinfo())



def main():
    # Capture packets on the default network interface
    sniff(prn=packet_callback, filter="ip", store=0)
    time.sleep(5)
    
sniffer_thread = threading.Thread(target=lambda: main())
sniffer_thread.start()


ui.run(title="NetWatch")
