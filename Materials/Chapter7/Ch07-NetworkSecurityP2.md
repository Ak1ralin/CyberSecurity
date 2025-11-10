# Practical Network Security – Part 2  

## 2. Firewall, IDS, IPS
| System | Function | Limitation |
|---------|-----------|-------------|
| **Firewall** | Filters IP/port headers | Cannot inspect payloads |
| **IDS** | Detects and logs suspicious packets (header+payload) | logs/alert not block|
| **IPS** | Detects and blocks packets (header+payload) | Can drop legitimate traffic |

> TCP/IP’s design limits firewall accuracy (fragmentation, spoofed src/dst).

---

## 3. Network Threat Model
- Adversary can intercept, modify, and send packets.  
- Full control of their machines and can join protocols.  
- Impossible to keep all bad actors out.

---

## 4. UDP and DNS Security
- UDP = connectionless, unreliable, no authentication.  
- Common apps: DNS, QUIC, VoIP.  
- **DNS attacks:**   : Application-Layer protocol
    - Flow การทำงานคร่าวๆ  
        - ผู้ใช้ขอชื่อโดเมน ผู้ใช้พิมพ์ URL เช่น www.chula.ac.th ในเบราว์เซอร์ → เครื่องจะต้องหาว่าโดเมนนั้นมี IP Address อะไร
        - ระบบปฏิบัติการหรือเบราว์เซอร์จะเช็ก DNS cache ในเครื่อง (local) ก่อน
            - ถ้ามีข้อมูล (ยังไม่หมดอายุ TTL) จะใช้ IP นั้นทันที
            - else -> ถาม DNS Resolver (ของ ISP หรือองค์กร)
        - Resolver ตรวจสอบลำดับชั้นของ DNS
            - ตรวจสอบใน cache
            - ถ้ายังไม่รู้คำตอบ Resolver จะทำการค้นแบบ “recursive”
                - ถาม Root DNS Server → ได้ชื่อของ Top-Level Domain (TLD) เช่น .th
                - ถาม TLD Server (.th) → ได้ชื่อของ Authoritative Server ของ chula.ac.th
                - ถาม Authoritative Server (chula.ac.th) → ได้ IP ของ www.chula.ac.th
            - Resolver ส่งผลกลับให้เครื่องผู้ใช้
            - Resolver จะเก็บผลไว้ใน cache เพื่อใช้ในอนาคต
        - ผู้ใช้ได้รับ IP เช่น 161.200.192.4
        - นำ IP ที่ได้ไปเปิดการเชื่อมต่อผ่าน TCP หรือ HTTPS
    - ปัญหา : 
        - 1 web อาจจะมี Authority หลายแห่งที่ตอบได้ ทำให้ใน response เขียน Authority ได้หลายอัน
        - User เชื่อสิ่งที่ DNS resolver ส่งกลับมาให้ 100% -> แปลว่าถ้าเราแก้ user ก็จะไปผิดที่
  - Cache poisoning
    - ผู้โจมตีส่ง DNS response ปลอม ที่มี Additional Record แถมโดเมนอื่นเข้ามาด้วย
    - ตัวอย่าง: ผู้ใช้ถาม IP ของ a.com แต่ผู้โจมตีแนบข้อมูล b.com = 6.6.6.6 มาด้วย ซึ่งจริงๆ b.com = 1.1.1.1, 6.6.6.6 เป็น web ปลอมทำชั่ว
    - **Defense** : แก้โดยไม่ให้แถม แต่มันก็จะทำให้ Perf แย่ -> แถมได้เฉพาะ web ที่อยู่ใต้ domain เดียวกัน เช่น ns.a.com, mail.a.com  (Bailiwick Checking)
  - Spoofing (Kaminsky) : DNS Spoofing
    - ปลอมตัวเป็น DNS Server แล้ว response resolver เอง
    - ใน Response , port ส่วนใหญ่คงที่เป็น 53 ดังนั้นเดาแค่ queryId ก็พอ ซึ่งแค่ 16 bits เท่านั้น เหมือนอิงตาม birthday paradox โอกาส Q=256,R=256 แล้วถูกมีถึง 63 %
    - **Defense** : 
        - Increase QueryId Space (16 bits -> 32 bits) -> แต่ยากเพราะต้องแก้ Protocol
        - source-port randomization : เปลี่ยนจาก fixed ทำให้โอกาสเพิ่มเป็น 2^32 bits

  - Rebinding : เปลี่ยน IP ที่ผูกกับชื่อโดเมนให้เป็น Internal ณญ, TTL อันแรกน้อย รอบ 2 ส่งให้เป็น Internal IP แล้วให้ JS ที่ฝังไปขุดข้อมูล
    - **Defense** : 
    - ฝั่งเบราว์เซอร์: ปรับค่าป้องกัน DNS rebinding, refuse mid-session IP switch
    - ฝั่งเครือข่าย/Resolver: บล็อกการ resolve ชื่อสาธารณะให้เป็น private IP ranges
    - Firewall: ป้องกันการเข้าถึงพอร์ตจัดการจากเครือข่ายภายนอก
  - DNSSEC (auth & integrity, กำหนดคนตอบ DNS, แต่ไม่แก้ปัญหาใดๆ ที่กล่าวมา)

---

## 5. Denial-of-Service (DoS/DDoS)
- Goal: exhaust victim resources using asymmetric workloads.  
- **Amplifiers:** 
    - One -> Many : Smurf, Fraggle
    - Loop : UDP Ping-Pong
    - Amplification : 
- Possible at every layer
    - Application layer : Process ไม่ทัน mostly ทำกันชั้นนี้
    - TCP/UDP (Transport layer): Maintain large number of connection -> queue ไม่พอ client connect server ไม่ได้
    - Link layer : too much traffic
- ทำผ่าน DNS : DDoS Amplification + Reflector Attack
    - สร้างคำขอที่จะได้ response ขนาดใหญ่ (Authority เยอะหรือ web ใต้ domain เยอะ) 
    - ซึ่งคำขอนี้มี Src IP เป็นของ Target ทำให้ victim จะได้รับของกลับไป ซึ่งทำหลายๆ อันยัดไปก็พัง
- **Defenses:** filtering spoofed IPs, rate limiting, patch misconfigured servers.

---

## 6. TCP Vulnerabilities
- **Spoofing:** Guess sequence number (1/2³² chance). ผู้โจมตีส่งแพ็กเก็ตปลอมที่แสดงตัวเป็นฝั่งหนึ่งของการเชื่อมต่อ เพื่อแทรกข้อมูลหรือ hijack stream.   
- **Reset attack:** Inject TCP RST to terminate connection. ส่งแพ็กเก็ตที่มีธง RST เพื่อสั่งให้เครื่องฝั่งรับปิดการเชื่อมต่อทันที. 
ต้องรู้ 4-tuple (srcIP, srcPort, dstIP, dstPort) และ sequence number ที่อยู่ใน window
- **SYN flood:** ส่ง SYN จำนวนมาก (มัก spoof source IP) ทำให้เซิร์ฟเวอร์สร้าง state (half-open) รอ ACK ที่จะไม่มา → คิว backlog เต็ม ไม่รับการเชื่อมต่อใหม่จากผู้ใช้จริง  
  - **Good fixes:** SYN cookies, ไม่ใช่ backlog แต่ encrypt แล้วให้อีกฝ่ายส่งกลับด้วย.
    - With SYN cookies, server does not store state. Instead, it encodes connection info (client IP, port, timestamp, etc.) inside the SYN-ACK’s sequence number.
    - If the client is real, it replies with an ACK that includes this value.  
  - **Bad fixes:** Increasing queue or shortening timeout.

---

## 7. TLS/SSL
- ใช้ “asymmetric encryption” แค่ตอนตั้งต้น เพื่อส่งหรือสร้าง “symmetric key” ที่จะใช้เข้ารหัส session ต่อไปทั้งหมด.
- Provides encryption, integrity, and authentication.  
- **Handshake:** negotiate algorithm, exchange keys, create session key.  
- **HTTPS:** HTTP over TLS.  
- **Heartbleed:** buffer over-read in OpenSSL → data leak.

---

## 8. Overall Defense Strategy
- Combine **patching**, **secure coding**, **education**, and **encryption**.  
- **Firewalls:** partial protection.  
- **Cryptographic protocols:** TLS, SSH, Kerberos.  
- **Unsolved areas:** DoS resistance, routing security.  
- Replacement protocols: **SBGP**, **DNSSEC**.

---

## 9. Key Takeaways
- Security issues often stem from **protocol design**, not bugs.  
- Must assume the network is hostile.  
- Layered defense: firewall + IDS/IPS + TLS + user awareness.  
- “No perfect defense, only improvement.”

