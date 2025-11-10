# Secure By Design – Summary

## 1. Concept Overview
- **Security:** Who can do what and when.  
- **Privacy:** Control over personal information access.  
- **Core Components (AAA + Integrity):**
  - Authentication – verify identity  
  - Authorization – verify permissions  
  - Accounting (Auditing) – record actions  
  - Integrity – preserve data authenticity and wholeness  

## 2. Secure Design Principles
- Plan security from the start, not after implementation.  
- **Attack Surface Reduction (ASR):**
  - Attack Surface : Where attacker can entry or extract data from a system
  - Less code running = fewer vulnerabilities  
  - Defense in Depth – multiple layers of protection  ->  remove single point of failure
  - Least Privilege – limit permissions  
  - Secure Defaults – turn off unnecessary features -> less stuff to attack

## 3. Attack Surface Control Examples
- Disable unused ports/services.
- Turn off UDP (if your service does not need)  
- Restrict network ranges. (only allow for trusted network)
- Authenticate connections. 
- Harden ACL (Access Control Lists). (Admin = full access, Everyone = read only, Service = Read&Write) 
- Run services with least privilege.  

## 4. Threat Modeling (STRIDE)
> Predict & Plan -> predict how attacker might compromise a system.
Think Like a bad guys

Threat are not vulnerabilities(Bug), Its can only be mitigated

Process = Gather info → Model system → Identify threats → Resolve them.

Threat types:

| Threat | Mitigation |
| -- | -- |
| Spoofing (ปลอมตัว) | Authentication |
| Tampering (แปะเปื้อน/ปลอมแปลง) | Integrity |
| Repudiation (ปฏิเสธความรับผิดชอบ) | Non-repudiation |
| Information Disclosure (เปิดเผยข้อมูล) | Confidentiality |
| Denial of Service (ใช้งานไม่ได้)| Availability |
| Elevation of Privilege (เพิ่มสิทธิ)| Authorization |

Checklist: no design is complete without a threat model; trace data flows; test each threat.

## 5. Input Validation
“All input is evil until proven otherwise.” – M. Howard  
- Validate type, length, range, format.  
- Prevent SQL injection, XSS (Cross-Site Scripting), buffer overflow.  
- Example of bad SQL: `WHERE ID='1001' OR 1=1 --`  

## 6. Conclusion
Every system must be secure from the ground up by design—not as an afterthought.
