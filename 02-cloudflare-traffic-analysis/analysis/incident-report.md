# Incident Response Report - Case 2

**Case ID:** INCIDENT-2026-0914-002  
**Analyst:** Luis Enrique Alvarez Hernandez  
**Date:** September 14, 2026  
**Status:** ✅ CLOSED  
**Severity:** LOW  

---

## 📋 Executive Summary

A significant network traffic spike was detected during routine monitoring of home network activity using Wireshark. Investigation identified the primary destination as IP address 162.159.141.124, consuming 60.62% of total network bandwidth. OSINT investigation determined the destination to be Cloudflare, Inc., a major content delivery network (CDN). The incident was classified as **Legitimate Traffic** and requires no remediation.

---

## 🚨 Incident Details

### Timeline
| Time | Event | Details |
|------|-------|---------|
| Day 2 (14-09-2026) | Capture Start | Wireshark began monitoring home network |
| During Capture | Anomaly Detected | IPv4 Statistics showed 162.159.141.124 consuming 60.62% of traffic |
| End of Capture | Traffic Analysis | 2,811 packets analyzed |
| Investigation | OSINT Lookup | AbuseIPDB and WHOIS queries performed |
| Completion | Resolution | Incident classified and closed |

---

## 📊 Incident Metrics

### Network Capture Details
| Metric | Value |
|--------|-------|
| Total Packets | 2,811 |
| Capture Status | Complete |
| Protocols Detected | TCP, UDP, DNS, ICMP |
| Unique Destination IPs | 25+ |
| CDN Services Identified | 2 (Cloudflare, Anthropic) |

### Anomalous Activity
| Indicator | Finding |
|-----------|---------|
| Primary Destination IP | 162.159.141.124 (Cloudflare) |
| Traffic Volume | 1,704 packets (60.62%) |
| Protocol | TCP (HTTPS/443) |
| Secondary CDN | 160.79.104.10 (Anthropic) - 4.59% |
| Other Services | Meta, Google, Microsoft, and others |

---

## 🔍 Investigation Findings

### Finding 1: Primary IP Identification
**Status:** ✅ Confirmed Legitimate

**IP Details:**

IP Address: 162.159.141.124
ISP: Cloudflare, Inc.
ASN: AS13335
Domain: cloudflare.com
Location: San Francisco, California, USA
Usage Type: Content Delivery Network
Abuse Reports: 1 (false positive)
Confidence of Abuse: 0%


**Assessment:** This is a legitimate, well-known CDN operated by Cloudflare, Inc.

---

### Finding 2: Service Purpose
**Status:** ✅ Verified

**Cloudflare CDN:**
- Cloudflare operates one of the world's largest CDN networks
- Serves content for thousands of major websites
- Primary users: Netflix, Reddit, Twitch, WordPress, and many others
- Standard HTTPS port usage (443)

**Conclusion:** Traffic pattern is consistent with accessing websites that use Cloudflare CDN.

---

### Finding 3: Traffic Pattern Analysis
**Status:** ✅ Normal Activity

**Traffic Characteristics:**

Protocol: TCP (HTTPS/443)
Behavior: Standard web browsing patterns
Packet Distribution: Normal for CDN traffic
No Retransmissions: No signs of network issues
Encryption: All traffic uses TLS/SSL


**Pattern Recognition:**
- Consistent with normal web browsing
- No data exfiltration indicators
- No unusual port scanning
- No malicious payload signatures detected

---

### Finding 4: Comparative Analysis with Case 1
**Status:** ✅ Patterns Identified

**Differences Between Cases:**

| Aspect | Case 1 (13-09) | Case 2 (14-09) | Analysis |
|--------|--------------|--------------|----------|
| Primary CDN | Anthropic (36%) | Cloudflare (60%) | Different websites visited |
| Secondary Services | Minimal | Meta, Google, Microsoft | More diverse browsing |
| Anthropic | High (36%) | Low (4.59%) | Less time on AI apps |
| Total Packets | 12,147 | 2,811 | Shorter capture period |

**Conclusion:** Different websites were accessed on different days, resulting in different CDN distributions.

---

### Finding 5: Secondary Destinations
**Status:** ✅ Identified and Verified

**Other Services Detected:**

1. **160.79.104.10** (Anthropic CDN) - 4.59%
   - ✅ Known-good service
   - Cloud AI platform

2. **Meta/Facebook IPs** (~8% total)
   - ✅ Legitimate social media
   - Multiple IP blocks detected

3. **Google IPs** (~3% total)
   - ✅ Google services (Gmail, YouTube, Search)
   - Standard CDN infrastructure

4. **Microsoft IPs** (~1% total)
   - ✅ Microsoft services (Office 365, etc.)
   - Expected traffic

**All identified services are legitimate major tech companies with excellent reputation.**

---

## ✅ Root Cause Analysis

**Question:** Why is 162.159.141.124 consuming 60.62% of network bandwidth?

**Answer:** 
The analyst's local PC (192.168.0.x) accessed multiple websites that use Cloudflare CDN for content delivery. Cloudflare handles caching, security, and content distribution for thousands of popular websites.

**Supporting Evidence:**
1. ✅ Cloudflare is a legitimate, well-known CDN
2. ✅ Traffic patterns match normal web browsing
3. ✅ HTTPS encryption used (secure connection)
4. ✅ No malicious indicators detected
5. ✅ Secondary CDN (Anthropic) still active (consistent with Case 1)

---

## 📋 Classification

| Category | Assessment |
|----------|-----------|
| **Incident Type** | Legitimate Traffic |
| **Severity** | LOW (no risk) |
| **Risk Level** | None |
| **Threat Status** | Not a threat |
| **Action Required** | None |
| **Escalation** | Not required |

---

## 📊 Network Behavior Baseline

**Findings from Case 1 & Case 2 Combined:**

1. **CDN Usage:** Network regularly accesses major CDNs (Anthropic, Cloudflare)
2. **Service Pattern:** Social media, search, cloud services, and AI tools
3. **Traffic Distribution:** Varies based on browsing activity
4. **Security Posture:** All traffic encrypted (HTTPS)
5. **Threat Status:** No anomalies or security concerns

---

## 🎯 Recommendations

### Immediate Actions
- ✅ **Close incident** - No threat identified
- ✅ **No remediation needed** - Traffic is legitimate
- ✅ **Resume normal monitoring** - Continue baseline tracking

### Prevention & Monitoring
1. **Update Whitelist**

162.159.141.124 (Cloudflare CDN)
160.79.104.10 (Anthropic CDN)
Meta IP ranges
Google IP ranges
Microsoft IP ranges


2. **Establish Network Baseline**
   - Document CDN usage patterns
   - Track peak traffic times
   - Monitor for sudden changes

3. **Create Detection Rules**
   - Alert on unknown CDNs (non-whitelisted)
   - Monitor for data exfiltration patterns
   - Track ports outside expected ranges (port 443 for HTTPS is normal)

4. **Documentation**
   - Add Cloudflare to known-good services list
   - Cross-reference Cases 1 & 2 for pattern recognition
   - Update network asset inventory

---

## 📝 Key Lessons Learned

### What Worked Well ✅
1. Wireshark captured complete traffic picture
2. Statistics/Destinations view quickly identified issue
3. OSINT investigation confirmed legitimacy
4. Comparative analysis between cases shows normal patterns

### Areas for Improvement
1. Could use automated WHOIS lookup tools
2. Could implement SIEM rules for CDN traffic
3. Could create automated whitelisting

---

## 🔐 Incident Sign-Off

**Analyst:** Luis Enrique Alvarez Hernandez  
**Investigation Start:** September 14, 2026  
**Investigation End:** September 14, 2026  
**Investigation Time:** < 1 hour  
**Status:** ✅ RESOLVED - Legitimate Traffic  

---

## 📎 Attachments

- [Wireshark Capture Screenshot](../captures/cloudflare-screenshot.png)
- [IP Endpoints Analysis](ip-endpoints.md)
- [WHOIS Data - 162.159.141.124](../whois/162.159.141.124.txt)
- [Case 1 Reference](../../01-home-network-analysis/)

---

## 📝 Summary

Two network traffic analyses (Case 1 & Case 2) demonstrate consistent, legitimate patterns of web browsing using major CDN services. Different websites accessed on different days result in different CDN usage. All identified services are legitimate and carry no security risk. Network is operating normally with no indicators of compromise.