# Case 1: Home Network Traffic Analysis

**Date:** September 13, 2026  
**Duration:** ~8.77 seconds capture  
**Analyst:** Luis Enrique Alvarez

## 🔍 Executive Summary

Detected unusual network traffic from local IP 192.168.0.13 consuming 39.32% 
of total bandwidth. Investigation revealed legitimate Anthropic CDN traffic.

**Status:** ✅ **CLOSED - False Positive**

---

## 📊 Findings

### Network Statistics
| Metric | Value |
|--------|-------|
| Total Packets | 12,147 |
| Top Source IP | 192.168.0.13 (39.32%) |
| Top Destination IP | 160.79.104.10 (36.21%) |
| Protocol | TCP |
| Duration | 8.77 seconds |

### IP Breakdown
- **192.168.0.13** → 4,776 pkts (39.32%) - Local PC (WiFi)
- **160.79.104.10** → 4,398 pkts (36.21%) - Anthropic CDN
- **192.168.0.12** → 832 pkts (6.85%)
- **192.168.0.1** → 509 pkts (4.19%) - Router
- Others → ~632 pkts (13.63%)

---

## 🔎 Investigation Process

### Step 1: Anomaly Detection


### Step 2: IP Identification (Local)
```bash
ipconfig
# IPv4: 192.168.0.13
# Adapter: Intel Wi-Fi 6 AX201
# SSID: vodafone56D3
```

### Step 3: IP Investigation (Remote)

**Results:**
- ISP: Anthropic, PBC
- Domain: anthropic.com
- Location: San Francisco, California, USA
- Abuse Confidence: 0%
- Reports: 0

### Step 4: Traffic Analysis


---

## ✅ Conclusion

**Classification:** False Positive - Legitimate Traffic

The detected traffic spike is consistent with normal web browsing activity to 
claude.ai (Anthropic's web interface). No indicators of compromise or data 
exfiltration detected.

---

## 📝 Recommendations

1. ✅ **No action required** - Traffic is from known-good service
2. Create whitelist rule for Anthropic CDN in SIEM
3. Establish baseline traffic patterns for future anomaly detection

---

## 📎 Artifacts

- Raw PCAPNG capture
- Wireshark statistics screenshot
- WHOIS data
