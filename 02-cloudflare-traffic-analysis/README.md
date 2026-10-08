# Case 2: Cloudflare CDN Traffic Analysis

**Date:** September 14, 2026  
**Duration:** Network capture (24 hours monitoring)  
**Analyst:** Luis Enrique Alvarez

## 🔍 Executive Summary

Detected significant network traffic spike from local PC (192.168.0.x) to external IP 162.159.141.124, consuming 60.62% of total bandwidth. Investigation revealed legitimate Cloudflare CDN traffic from routine web browsing.

**Status:** ✅ **CLOSED - Legitimate Traffic**

---

## 📊 Findings

### Network Statistics
| Metric | Value |
|--------|-------|
| Total Packets | 2,811 |
| Top Destination IP | 162.159.141.124 (60.62%) |
| Protocol | TCP |
| Service | Content Delivery Network (CDN) |

### IP Breakdown
- **162.159.141.124** → 1,704 pkts (60.62%) - Cloudflare CDN
- **160.79.104.10** → 129 pkts (4.59%) - Anthropic CDN
- **212.166.132.96** → 119 pkts (4.23%) - Unknown
- Others → ~859 pkts (30.56%)

---

## 🔎 Investigation Process

### Step 1: Anomaly Detection 

Wireshark capture → IPv4 Statistics/Destinations and Ports
Result: 162.159.141.124 consuming 60.62% of traffic

### Step 2: IP Investigation

AbuseIPDB lookup: 162.159.141.124

**Results:**
- ISP: Cloudflare, Inc.
- Type: Content Delivery Network
- Domain: cloudflare.com
- Location: San Francisco, California, USA
- ASN: AS13335
- Abuse Confidence: 0%
- Reports: 1 (false positive)

### Step 3: Traffic Analysis

**Results:**
- ISP: Cloudflare, Inc.
- Type: Content Delivery Network
- Domain: cloudflare.com
- Location: San Francisco, California, USA
- ASN: AS13335
- Abuse Confidence: 0%
- Reports: 1 (false positive)

### Step 3: Traffic Analysis

Wireshark Filter: ip.dst == 162.159.141.124
Protocol: TCP (HTTPS)
Destination Port: 443 (TLS/SSL)
Behavior: Normal web browsing pattern

### Step 4: Root Cause

---

## ✅ Conclusion

**Classification:** Legitimate Traffic - Normal Web Browsing

The detected traffic spike is consistent with routine web browsing to websites protected by Cloudflare CDN. No indicators of compromise or unusual activity detected.

---

## 📊 Comparison with Case 1

| Aspect | Case 1 | Case 2 |
|--------|--------|--------|
| Date | Sep 13, 2026 | Sep 14, 2026 |
| Top IP | 160.79.104.10 | 162.159.141.124 |
| Service | Anthropic CDN | Cloudflare CDN |
| % Traffic | 36% | 60% |
| Classification | Legitimate | Legitimate |
| Pattern | AI web app | General web browsing |

**Pattern:** Different CDNs based on websites visited during each capture.

---

## 📝 Recommendations

1. ✅ **No action required** - Traffic is from known-good services
2. Add both CDNs to whitelist (160.79.104.10 and 162.159.141.124)
3. Monitor traffic patterns over time
4. Establish baseline for home network

---

## 📎 Artifacts

- Wireshark statistics screenshot
- WHOIS data for 162.159.141.124

