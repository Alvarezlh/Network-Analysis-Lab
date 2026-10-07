# Network Analysis Lab

**Cybersecurity portfolio: network traffic analysis and SIEM integration**

Real-world network analysis and incident investigation using Wireshark, Wazuh and OSINT techniques.

## Overview

- Network traffic capture with Wireshark and tshark
- Endpoint analysis and communication pattern identification
- OSINT investigation of external IPs
- SIEM automation with Python and the Wazuh Agent
- Custom Wazuh detection rules
- Incident reports written in SOC analyst style

## Project structure

```
Network-Analysis-Lab/
├── 01-home-network-analysis/ Case 1: Anthropic CDN
│ ├── README.md
│ ├── analysis/ (ip-endpoints.md, incident-report.md)
│ ├── captures/ (wireshark-screenshot.png)
│ └── whois/ (160.79.104.10.txt)
├── 02-cloudflare-traffic-analysis/ Case 2: Cloudflare CDN
│ ├── README.md
│ ├── analysis/ (ip-endpoints.md, incident-report.md)
│ ├── captures/ (cloudflare-screenshot.png)
│ └── whois/ (162.159.141.124.txt)
├── 03-wireshark-wazuh-automation/ Case 3: Wireshark-to-Wazuh pipeline
│ ├── README.md
│ ├── scripts/ (wireshark_to_wazuh.py)
│ ├── config/ (wazuh_rules.xml)
│ ├── docs/ (fixed-ip-setup.md)
│ └── images/
└── README.md
```


## Completed cases

### Case 1: Anthropic CDN analysis (13-09-2026)

**Objective:** identify and classify external traffic.

- **IP:** 160.79.104.10 (Anthropic, San Francisco)
- **Traffic:** 39.32% of the captured bandwidth
- **Protocol:** HTTPS (port 443)
- **Classification:** false positive, claude.ai browsing
- **Method:** 60 s Wireshark capture, endpoint analysis, OSINT (AbuseIPDB, WHOIS), incident report

Details: [`01-home-network-analysis/`](01-home-network-analysis/)

### Case 2: Cloudflare CDN analysis (14-09-2026)

**Objective:** detect CDN traffic patterns and data volume.

- **IP:** 162.159.141.124 (Cloudflare Inc., AS13335)
- **Traffic:** 60.62% of the captured bandwidth (1,704 packets)
- **Other sources:** Meta (~8%), Google (~3%), Anthropic (4.59%)
- **Classification:** legitimate, web browsing through a CDN
- **Method:** packet statistics by IP, protocol identification, ASN lookup, event timeline

Details: [`02-cloudflare-traffic-analysis/`](02-cloudflare-traffic-analysis/)

### Case 3: Wireshark-to-Wazuh automation (03-10-2026 to 07-10-2026)

**Objective:** build an automated pipeline that brings network traffic into the Wazuh SIEM as alerts.

```
tshark capture -> Python parser -> JSON lines file -> Wazuh Agent -> Wazuh Manager (custom rules) -> Dashboard
```


- 50 events per capture ingested and decoded in the Dashboard
- Five custom rules (100000-100004) in a parent and child structure
- Rules validated with controlled test events and against live traffic (a 50-event capture: 17 encrypted, 32 generic, 1 Anthropic CDN)
- Main lessons: one JSON object per line, append mode for the monitored file, parent and child rules instead of a catch-all sibling, never assuming a tool's exact output format, and writing raw-text rules that tolerate whitespace differences
- Status: ingestion and detection rules validated; custom dashboard pending

Details: [`03-wireshark-wazuh-automation/`](03-wireshark-wazuh-automation/)

## Demonstrated skills

**Network security:** traffic capture and analysis, endpoint and pattern identification, OSINT and IP investigation.

**SIEM and log management:** event ingestion into Wazuh, custom detection rules, alert validation and troubleshooting.

**Automation and scripting:** Python, subprocess and tshark, structured JSON logging.

**Blue team and SOC:** incident reports, alert classification (true and false positives), documentation of findings.

## Tools

Wireshark and tshark, Wazuh (Manager, Agent and Dashboard), Python 3, Kali Linux, VirtualBox, AbuseIPDB, WHOIS.

## Security and privacy

- Private IPs in the documentation use the generic format `192.168.0.x`
- SSIDs, hostnames and credentials are never published
- Public IPs of CDNs (Cloudflare, Anthropic) are already public in WHOIS
- Packet captures are not committed

## Author

**Luis Enrique Alvarez Hernandez**, aspiring SOC analyst (Blue Team), Barcelona, Spain

LinkedIn: [linkedin.com/in/luis-enrique-alvarez](https://linkedin.com/in/luis-enrique-alvarez/)

This project is open source for educational and portfolio purposes.
