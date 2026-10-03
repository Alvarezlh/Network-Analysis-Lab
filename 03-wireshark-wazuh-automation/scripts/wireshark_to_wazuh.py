#!/usr/bin/env python3
"""Wireshark to Wazuh automation.

Captures traffic with tshark, extracts simple events and appends them, one JSON
object per line, to a log file monitored by the Wazuh Agent.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load configuration (config.env lives in ../config relative to this script)
load_dotenv(Path(__file__).resolve().parent.parent / 'config' / 'config.env')

LOG_DIR = os.getenv('LOG_DIR', '/home/kali/wireshark_logs')
CAPTURE_DURATION = os.getenv('CAPTURE_DURATION', '60')
CAPTURE_INTERFACE = os.getenv('CAPTURE_INTERFACE', 'eth0')

print("=" * 50)
print("🚀 Wireshark to Wazuh Automation")
print("=" * 50)

# Create the log directory if it does not exist
os.makedirs(LOG_DIR, exist_ok=True)

# STEP 1: Capture traffic
print(f"📡 Capturing {CAPTURE_DURATION}s on {CAPTURE_INTERFACE}...")
try:
    result = subprocess.run(
        ['tshark', '-i', CAPTURE_INTERFACE, '-a', f'duration:{CAPTURE_DURATION}', '-T', 'json'],
        capture_output=True,
        text=True,
        timeout=int(CAPTURE_DURATION) + 10
    )

    if result.returncode != 0:
        print(f"❌ Capture error: {result.stderr}")
        sys.exit(1)

    packet_count = result.stdout.count('"frame"')
    print(f"✅ Capture finished ({packet_count} packets)")
except Exception as e:
    print(f"❌ Capture error: {e}")
    sys.exit(1)

# STEP 2: Parse the capture and build events
print("📊 Analyzing packets...")
try:
    packets = json.loads(result.stdout)
    events = []

    for packet in packets[:50]:  # first 50 packets
        try:
            layers = packet.get('_source', {}).get('layers', {})
            ip_layer = layers.get('ip', {})
            tcp_layer = layers.get('tcp', {})
            frame_layer = layers.get('frame', {})

            src_ip = ip_layer.get('ip.src', 'N/A')
            dst_ip = ip_layer.get('ip.dst', 'N/A')
            dst_port = tcp_layer.get('tcp.dstport', '')
            protocol = 'HTTPS' if dst_port == '443' else 'TCP'

            event = {
                'timestamp': datetime.now().isoformat(),
                'event_type': 'network_traffic',
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'protocol': protocol,
                'dst_port': dst_port,
                'frame_length': frame_layer.get('frame.len', '0')
            }
            events.append(event)
        except Exception:
            continue

    print(f"✅ {len(events)} packets analyzed")
except Exception as e:
    print(f"❌ Parsing error: {e}")
    sys.exit(1)

# STEP 3: Append events to the monitored log file (one JSON object per line)
print("💾 Saving events...")
try:
    output_file = f"{LOG_DIR}/wireshark_events.json"

    with open(output_file, 'a') as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    print(f"✅ Saved to: {output_file}")
except Exception as e:
    print(f"❌ Saving error: {e}")
    sys.exit(1)

# STEP 4: Show a short summary
print("\n📋 Event summary:")
for i, event in enumerate(events[:5], 1):
    print(f"  {i}. {event['src_ip']} → {event['dst_ip']}:{event['dst_port']} ({event['protocol']})")

if len(events) > 5:
    print(f"  ... and {len(events) - 5} more")

print("=" * 50)
print("✅ Process completed")
print("=" * 50)