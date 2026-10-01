# Network Analysis Lab - Wazuh SIEM Automation

**Cybersecurity Portfolio: Network Traffic Analysis and SIEM Integration**

Real-world network analysis and incident investigation using Wireshark, Wazuh, and OSINT techniques.

---

## 📋 Overview

This project demonstrates:
- **Network traffic capture** with Wireshark/tshark
- **Endpoint analysis** and communication pattern identification
- **SIEM automation** via Python and REST API
- **Threat detection** with custom Wazuh rules
- **Incident investigation** in SOC analyst style

---

## 📁 Project Structure

Network-Analysis-Lab/
├── 01-home-network-analysis/ # Case 1: Anthropic CDN
│ ├── README.md
│ ├── analysis/
│ │ ├── ip-endpoints.md
│ │ └── incident-report.md
│ ├── captures/
│ │ └── wireshark-screenshot.png
│ └── whois/
│ └── 160.79.104.10.txt
│
├── 02-cloudflare-traffic-analysis/ # Case 2: Cloudflare CDN
│ ├── README.md
│ ├── analysis/
│ │ ├── ip-endpoints.md
│ │ └── incident-report.md
│ ├── captures/
│ │ └── cloudflare-screenshot.png
│ └── whois/
│ └── 162.159.141.124.txt
│
├── 03-wireshark-wazuh-automation/ # Case 3: Wazuh Automation
│ ├── README.md
│ ├── scripts/
│ │ ├── wireshark_to_wazuh.py
│ │ └── storage_manager.sh
│ ├── config/
│ │ ├── config.env (not in GitHub)
│ │ ├── wazuh_rules.xml
│ │ └── log_rotation.conf
│ ├── docs/
│ │ ├── setup.md
│ │ └── automation_guide.md
│ └── .gitignore
│
└── README.md (this file)


---

## 🎯 Completed Cases

### Case 1: Anthropic CDN Analysis (13-09-2026)

**Objective:** Identify and classify external traffic

**Findings:**
- **IP:** 160.79.104.10 (Anthropic, San Francisco)
- **Traffic:** 39.32% bandwidth (192.168.0.x)
- **Protocol:** HTTPS (Port 443)
- **Classification:** ✅ **False Positive** - claude.ai browsing

**Methodology:**
1. 60s Wireshark capture
2. Network endpoint analysis
3. OSINT investigation (AbuseIPDB, WHOIS)
4. Incident report writing

**Location:** `/01-home-network-analysis/`

---

### Case 2: Cloudflare CDN Analysis (14-09-2026)

**Objective:** Detect CDN traffic patterns and data volume

**Findings:**
- **IP:** 162.159.141.124 (Cloudflare Inc., AS13335)
- **Traffic:** 60.62% bandwidth (1,704 packets)
- **Other sources:** Meta (~8%), Google (~3%), Anthropic (4.59%)
- **Classification:** ✅ **Legitimate** - web browsing via CDN

**Analysis Techniques:**
- Packet statistics by IP
- Protocol identification
- ASN lookup and geolocation
- Event timeline creation

**Location:** `/02-cloudflare-traffic-analysis/`

---

### Case 3: Wireshark-to-Wazuh Automation (25-09-2026)

**Objective:** Build automated pipeline for network traffic ingestion into SIEM

**Status:** Capture and parsing working ✅

#### Python Script (`wireshark_to_wazuh.py`)

**Flow:** Capture (tshark) → JSON → Parsing → Local storage

**Features:**
- ✅ Captures 60 seconds of traffic on eth0
- ✅ Exports to JSON format
- ✅ Parses first 50 packets
- ✅ Extracts: src_ip, dst_ip, protocol, dst_port, frame_length
- ✅ Saves to `/home/kali/wireshark_logs/`

**Example Event:**
```json
{
  "timestamp": "2026-09-30T22:55:32.123456",
  "event_type": "network_traffic",
  "src_ip": "192.168.0.20",
  "dst_ip": "172.67.157.37",
  "protocol": "HTTPS",
  "dst_port": "443",
  "frame_length": "1507"
}
```

#### Wazuh Detection Rules (`wazuh_rules.xml`)

| Rule ID | Name | Level | Description |
|---------|------|-------|-------------|
| 100000 | Parent Rule | 0 | Base network traffic events |
| 100001 | Cloudflare CDN | 3 | Detects traffic to 162.159.141.124 |
| 100002 | Anthropic CDN | 3 | Detects traffic to 160.79.104.10 |
| 100003 | HTTPS Traffic | 2 | Detects encrypted traffic port 443 |
| 100004 | Network Analysis | 5 | Network analysis alerts |

**Location:** `/03-wireshark-wazuh-automation/`

---

## 📊 Execution Results (30-09-2026)

**Status:** Capture and parsing working ✅

### Traffic Capture
- ✅ Duration: 60 seconds on eth0
- ✅ Packets captured: 1,291
- ✅ Format: JSON (tshark)

### Event Analysis
- ✅ Events analyzed: 50 packets
- ✅ Fields extracted: src_ip, dst_ip, protocol, dst_port, frame_length, timestamp
- ✅ Correctly parsed: HTTPS (port 443), TCP, other protocols

### Event Storage
- ✅ Location: `/home/kali/wireshark_logs/wireshark_events_YYYYMMDD_HHMMSS.json`
- ✅ Valid JSON format
- ✅ Coming soon: Automatic Wazuh ingestion

### Top 5 Events Captured

1. 20.215.74.200 → 192.168.0.100:12845 (TCP)
2. 192.168.0.100 → 20.215.74.200:443 (HTTPS) ← CDN Traffic
3. 192.168.0.10 → 224.0.0.251 (TCP)
4. 192.168.0.100 → 20.215.74.200:443 (HTTPS)
5. 20.215.74.200 → 192.168.0.100:12845 (TCP)
... and 45 more

---

## 🛠️ Setup and Usage

### Requirements

Kali Linux 2023.x+
Python 3.10+
Wireshark/tshark
Wazuh Manager 4.14.6+ (OVA on VirtualBox)
Wazuh Agent
curl, git, nano


### Installation

1. **Clone repository:**
```bash
git clone https://github.com/Alvarezlh/Network-Analysis-Lab.git
cd Network-Analysis-Lab/03-wireshark-wazuh-automation
```

2. **Install Python dependencies:**
```bash
pip install requests python-dotenv
```

3. **Configure environment variables:**
```bash
cp config/config.env.example config/config.env
nano config/config.env
```

**config.env:**

WAZUH_API_URL=https://192.168.0.20:55000
WAZUH_USER=wazuh
WAZUH_PASS=wazuh
CAPTURE_DURATION=60
CAPTURE_INTERFACE=eth0
LOG_DIR=/home/kali/wireshark_logs
RETENTION_DAYS=7


4. **Load Wazuh rules:**
   - Dashboard → Management → Rules → Custom rules
   - Create: `0100-wireshark_network_analysis.xml`
   - Copy content from `config/wazuh_rules.xml`
   - Save and restart: `sudo systemctl restart wazuh-manager`

### Execution

```bash
cd scripts/
sudo python3 wireshark_to_wazuh.py
```

**Expected output:**

==================================================
🚀 Wireshark to Wazuh Automation

📡 Capturing 60s...
✅ Capture saved (XXXX packets)
📊 Analyzing...
✅ 50 packets analyzed
💾 Saving events...
✅ Saved to: /home/kali/wireshark_logs/wireshark_events_*.json

📋 Event Summary:

20.215.74.200 → 192.168.0.100:12845 (TCP)
192.168.0.100 → 20.215.74.200:443 (HTTPS)
...
==================================================
✅ Process completed


### Verification in Dashboard

1. Access: `https://192.168.0.20`
2. **Security Events** → Filter `rule.id: 100001-100004`
3. Review captured events and analysis

---

## 🐛 Known Issues

### Issue 1: DHCP and changing IPs

Symptom: Kali and Wazuh IPs change each session
Solution: Run 'ip addr' before starting
Update WAZUH_API_URL in config.env if changed


### Issue 2: IPv6 instead of IPv4

Symptom: Wazuh receives IPv6/MAC instead of 192.168.x.x
Solution: Disable IPv6 in /etc/netplan/00-installer-config.yaml (dhcp6: false)
Then: sudo netplan apply


### Issue 3: Wazuh Dashboard won't load

Symptom: Blank page after boot
Solution: Wait 10-15 min (OpenSearch is slow)
sudo systemctl restart elasticsearch wazuh-manager wazuh-dashboard
Clear browser cache (Ctrl + Shift + Delete)


### Issue 4: tshark permission timeout

Symptom: "tshark timed out after 70 seconds"
Solution: Run with sudo: sudo python3 wireshark_to_wazuh.py


---

## 🔐 Security and Privacy

**Redacted before publishing:**
- SSID: `Home-Network` (not specific)
- Private IPs: `192.168.0.x` (generic format)
- Hostnames: Not published

**Safe to publish:**
- Public IPs: Cloudflare, Anthropic (already public in WHOIS)
- Wazuh rules: Detection methods
- Analysis reports: Methodology

---

## 📈 Demonstrated Skills

✅ **Network Security**
- Traffic capture and analysis
- Endpoint and pattern identification
- OSINT and IP investigation

✅ **SIEM & Log Management**
- Event ingestion into Wazuh
- Custom detection rule writing
- Security event analysis

✅ **Automation & Scripting**
- Python with requests and subprocess
- REST API integration
- File and logging management

✅ **Blue Team / SOC Analyst**
- Incident report writing
- Alert classification (True/False Positive)
- False positive remediation

---

## 📚 References

- [Wazuh Official Documentation](https://documentation.wazuh.com/)
- [Wireshark User Guide](https://www.wireshark.org/docs/)
- [AbuseIPDB](https://www.abuseipdb.com/)
- [WHOIS Lookup](https://www.whois.com/)

---

## 📝 Next Steps

- [ ] Complete Wazuh Agent ingestion integration
- [ ] Create visual dashboard in Wazuh
- [ ] Automate with cron job (hourly execution)
- [ ] Add machine learning anomaly detection
- [ ] Slack integration for real-time alerts

---

## 👤 Author

**Luis Enrique Alvarez Hernandez**
- Portfolio: SOC Analyst | Blue Team
- LinkedIn: [linkedin.com/in/luis-enrique-alvarez/](https://linkedin.com/in/luis-enrique-alvarez/)
- Location: Barcelona, Spain

---

## 📄 License

This project is open source for educational and portfolio purposes.

Last updated: 01-10-2026
Status: v1.0 - Capture and Analysis
Next: Wazuh Agent Integration


