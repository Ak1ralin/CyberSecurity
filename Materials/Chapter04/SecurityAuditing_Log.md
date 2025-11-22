# Chapter 4: Security Auditing & Log Analysis

## 1. Information Security Goals: CIA Triad
- **Confidentiality:** Only authorized users can access data.  
- **Integrity:** Data must not be tampered or altered.  
- **Availability:** Systems and data must be available to authorized users.

## 2. Security Framework: AAA
- **Authentication:** Verify identity.  
- **Authorization:** Grant permissions.  
- **Accounting/Auditing:** Log and track user actions.

## 3. Auditing Concepts
- **Logging:** Record events or stats about system usage & perf.  
- **Auditing:** Analyze logs to interpret system status clearly.

## 4. Auditing Goals
- User accountability : Known who's action  
- Damage assessment : post-incident evaluation, analyze impact and improve future defenses
- Identify security violation causes : find root cause  
- Describe system’s security state : malware
    - Detect unauthorized system states
- Evaluate protection mechanisms  
    - Deter attacks via audit records : Make hacker feel fears

## 5. Logging Problems
- What to log: Focus on data relevant to policy violations.  
    - Important event | Everything?
        - Important -> might not see the problem
        - Everything -> something might useless
        - So choose everything that important instead -> policy violate (know exactly what going on)
    - States vs. events 
        - States : Dont know what happen after recover
        - Events : Know what happen
- What to audit: Not all data, only policy-relevant info.  

## 6. Orange Book (C2 Level) Requirements
Log must record:
- Use of identification and authentication 
- Object creation/deletion (e.g., file open)  
- Admin/system actions  
- Other security-related events  

Each record includes:
- Date/time : timestamp
- User : user accountability
- Event type 
- Success/failure  
- Terminal ID (for auth) -> ip,hostname : identifies where a login or authentication request originated
- Object name (for file ops) : what resource access

Selective auditing by user identity must be supported. -> special for suspected user

## 7. Log Analysis Workflow
1. **Collection:** Syslogs, event logs, app logs, firewall logs, etc. : 
    - No standard format : but at least -> timestamp & event
    - Time synchronization : log might come from multiple source 
2. **Event Management:** 
    - What to keep (all vs. filtered)  
    - How to store (centralized, backup/archived)
    - What format (parsed/raw) 
    - Preprocess the log -> index & summary 
    - Access control (role-based, dashboards)  
3. **Analysis:** Manual, rule-based, or automated (AI/ML). 
    - Analysis method
        - **Statistical analysis**  
        - **Anomaly detection**  
        - **Association analysis**  
        - **AI/Machine Learning**  
    - Timing :
        - **real-time** : most service impossible
        - **post-mortem** : mostly use this one
    - Rule-based example : 
        - 3 fail logins in a row -> disable acc & notify admin
4. **Response:** Alerts, reports, evidence preservation, lessons learned.
    - Alerts: automatic or manual notifications when suspicious activity is detected.

    - Reports: summaries of findings for admins, management, or compliance records.

    - Evidence preservation: securely store relevant logs for investigation or legal use.

    - Lessons learned: analyze incidents to improve future detection and defenses.
    
## 8. Protecting Audit Data
- User should not have any access to log.
- Existing log entry cannot be modify
- Limit access to log files (append-only, no read/delete rights).  
- Protect archived logs (MACs, encryption, physical security).  
- Logs are vulnerable if host is compromised — replicate to secure remote server or use write-once media.

## 9. Tamperproof Logs (Schneier & Kelsey, 1999)
- Prevent attacker from modifying past logs.  
- Uses **iterated hashing** to ensure integrity.  
    - Iterated hashing : ใช้ log เก่ามาคำนวณด้วย ทำให้สามารถพบได้ด้วยว่าถูกแก้ตรงไหน 
---
