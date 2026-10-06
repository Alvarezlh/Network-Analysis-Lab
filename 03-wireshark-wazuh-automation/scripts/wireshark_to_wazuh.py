#!/usr/bin/env python3
"""Wireshark to Wazuh automation.

Captures traffic with tshark, builds one event per sampled IP packet and appends
the events, one JSON object per line, to a log file monitored by the Wazuh Agent.
"""

import json
import os
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Load configuration (config.env lives in ../config relative to this script)
load_dotenv(Path(__file__).resolve().parent.parent / 'config' / 'config.env')

LOG_DIR = os.getenv('LOG_DIR', '/home/kali/wireshark_logs')
CAPTURE_DURATION = os.getenv('CAPTURE_DURATION', '60')
CAPTURE_INTERFACE = os.getenv('CAPTURE_INTERFACE', 'eth0')
MAX_EVENTS = int(os.getenv('MAX_EVENTS', '50'))

# Link and network layers: the protocol label is the highest layer above them
NETWORK_LAYERS = {'eth', 'ethertype', 'vlan', 'sll', 'ip', 'ipv6', 'ipv6.hopopts'}


def capture():
    """Run tshark for the configured duration and return the parsed packets."""
    print(f"📡 Capturing {CAPTURE_DURATION}s on {CAPTURE_INTERFACE} ...")
    result = subprocess.run(
        ['tshark', '-i', CAPTURE_INTERFACE, '-a', f'duration:{CAPTURE_DURATION}', '-T', 'json'],
        capture_output=True,
        text=True,
        timeout=int(CAPTURE_DURATION) + 10
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    packets = json.loads(result.stdout) if result.stdout.strip() else []
    print(f"✅ Capture finished ({len(packets)} packets)")
    return packets


def get_protocol(frame_protocols):
    """Return the highest-level protocol dissected by tshark (TLS, QUIC, DNS, ...)."""
    names = [p for p in frame_protocols.split(':') if p and p not in NETWORK_LAYERS]
    names = [p for p in names if p != 'data'] or names
    return names[-1].upper() if names else 'OTHER'


def build_event(packet):
    """Build an event from a packet, or return None if it has no IP layer."""
    layers = packet.get('_source', {}).get('layers', {})

    if 'ip' in layers:
        src_ip = layers['ip'].get('ip.src')
        dst_ip = layers['ip'].get('ip.dst')
    elif 'ipv6' in layers:
        src_ip = layers['ipv6'].get('ipv6.src')
        dst_ip = layers['ipv6'].get('ipv6.dst')
    else:
        return None  # ARP and other non-IP packets

    if not src_ip or not dst_ip:
        return None

    transport = layers.get('tcp') or layers.get('udp') or {}
    dst_port = transport.get('tcp.dstport') or transport.get('udp.dstport') or ''

    frame = layers.get('frame', {})
    epoch = float(frame.get('frame.time_epoch', 0) or 0)
    when = datetime.fromtimestamp(epoch, tz=timezone.utc) if epoch else datetime.now(timezone.utc)

    return {
        'timestamp': when.isoformat(),
        'event_type': 'network_traffic',
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'protocol': get_protocol(frame.get('frame.protocols', '')),
        'dst_port': dst_port,
        'frame_length': frame.get('frame.len', '0')
    }


def sample_events(packets):
    """Keep IP packets only and return a random sample, in time order."""
    candidates = []
    for packet in packets:
        try:
            event = build_event(packet)
        except Exception:
            continue
        if event:
            candidates.append(event)

    events = random.sample(candidates, min(MAX_EVENTS, len(candidates)))
    events.sort(key=lambda e: e['timestamp'])
    print(f"✅ {len(candidates)} IP packets found, {len(events)} sampled")
    return events


def save_events(events):
    """Append the events to the monitored log file, one JSON object per line."""
    os.makedirs(LOG_DIR, exist_ok=True)
    output_file = f"{LOG_DIR}/wireshark_events.json"

    with open(output_file, 'a') as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    print(f"✅ Saved to: {output_file}")


def print_summary(events):
    """Show a short summary of the sampled events."""
    print("\n📋 Event summary:")
    for i, event in enumerate(events[:5], 1):
        print(f"  {i}. {event['src_ip']} → {event['dst_ip']}:{event['dst_port']} ({event['protocol']})")
    if len(events) > 5:
        print(f"  ... and {len(events) - 5} more")


def main():
    print("=" * 50)
    print("🚀 Wireshark to Wazuh Automation")
    print("=" * 50)

    try:
        packets = capture()
        events = sample_events(packets)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    if not events:
        print("⚠️ No IP packets captured, nothing to save")
        sys.exit(0)

    print("💾 Saving events ...")
    try:
        save_events(events)
    except Exception as e:
        print(f"❌ Saving error: {e}")
        sys.exit(1)

    print_summary(events)
    print("=" * 50)
    print("✅ Process completed")
    print("=" * 50)


if __name__ == '__main__':
    main()