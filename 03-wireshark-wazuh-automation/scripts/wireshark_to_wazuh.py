#!/usr/bin/env python3
"""
Wireshark to Wazuh Automation Script
Captura tráfico, exporta a JSON y envía a Wazuh
"""

import subprocess
import json
import os
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load configuration from .env file
load_dotenv('/home/kali/Network-Analysis-Lab/03-wireshark-wazuh-automation/config/config.env')

# Configuration from environment variables
WAZUH_API = os.getenv('WAZUH_API_URL', 'https://192.168.0.20:55000')
WAZUH_USER = os.getenv('WAZUH_USER', 'wazuh')
WAZUH_PASS = os.getenv('WAZUH_PASS', 'wazuh')
AGENT_ID = "000"
CAPTURE_DURATION = int(os.getenv('CAPTURE_DURATION', 60))
CAPTURE_FILE = "/tmp/network_capture.pcap"
JSON_FILE = "/tmp/network_capture.json"
LOG_DIR = os.getenv('LOG_DIR', '/home/kali/wireshark_logs')

Path(LOG_DIR).mkdir(exist_ok=True)

def get_wazuh_token():
    """Obtener token Wazuh"""
    try:
        response = requests.post(
            f"{WAZUH_API}/security/user/authenticate",
            auth=(WAZUH_USER, WAZUH_PASS),
            verify=False
        )
        return response.json()['data']['token']
    except Exception as e:
        print(f"❌ Error autenticando: {e}")
        return None

def capture_traffic(duration, output_file):
    """Capturar con tshark"""
    print(f"📡 Capturando {duration}s...")
    try:
        cmd = ["tshark", "-i", "eth0", "-a", f"duration:{duration}", "-w", output_file]
        subprocess.run(cmd, check=True)
        print(f"✅ Captura guardada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def export_to_json(pcap_file, json_file):
    """Exportar a JSON"""
    print(f"🔄 Exportando JSON...")
    try:
        cmd = ["tshark", "-r", pcap_file, "-T", "json"]
        with open(json_file, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        print(f"✅ JSON exportado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def parse_json_packets(json_file):
    """Parsear JSON"""
    print(f"📊 Analizando...")
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        events = []
        for packet in data[:50]:
            try:
                source = packet['_source']['layers'].get('ip', {}).get('ip.src', 'N/A')
                dest = packet['_source']['layers'].get('ip', {}).get('ip.dst', 'N/A')
                protocol = packet['_source']['layers'].get('highest_layer', 'N/A')
                
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "source_ip": source,
                    "dest_ip": dest,
                    "protocol": protocol,
                    "event_type": "network_traffic"
                }
                events.append(event)
            except:
                continue
        
        print(f"✅ {len(events)} paquetes analizados")
        return events
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def send_to_wazuh(events, token):
    """Enviar a Wazuh"""
    if not token:
        print("❌ Sin token")
        return False
    
    print(f"📤 Enviando {len(events)} eventos...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        for event in events:
            requests.post(f"{WAZUH_API}/events", json=event, headers=headers, verify=False)
        print(f"✅ Enviado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def cleanup():
    """Limpiar temporales"""
    print("🧹 Limpiando...")
    try:
        if os.path.exists(CAPTURE_FILE):
            os.remove(CAPTURE_FILE)
        if os.path.exists(JSON_FILE):
            os.remove(JSON_FILE)
        print("✅ Limpieza completa")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def main():
    """Flujo principal"""
    print("=" * 50)
    print("🚀 Wireshark to Wazuh Automation")
    print("=" * 50)
    
    if not capture_traffic(CAPTURE_DURATION, CAPTURE_FILE):
        return
    
    if not export_to_json(CAPTURE_FILE, JSON_FILE):
        return
    
    events = parse_json_packets(JSON_FILE)
    if not events:
        print("⚠️  No hay eventos")
        cleanup()
        return
    
    token = get_wazuh_token()
    send_to_wazuh(events, token)
    cleanup()
    
    print("=" * 50)
    print("✅ Proceso completado")
    print("=" * 50)

if __name__ == "__main__":
    main()