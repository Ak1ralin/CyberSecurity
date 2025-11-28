# Network Security (Part 1)

## Introduction
- Purpose: Understand how systems are attacked and defended.
- Quote: “Attack is the secret of defense; defense is the planning of an attack.” — Sun Tzu

## How Systems Are Hacked
- **Remotely:** Exploit network services, remote login, impersonate users.
- **Locally:** Social engineering, exploiting local vulnerabilities.

## Network Fundamentals
- The Internet provides **best-effort** packet delivery (no guarantee).
- **Packet = Header + Payload.**
- **IP Address:** unique identifier of host.
- **Design principle:** simple, dumb network; complexity handled by endpoints.
    - The focus has been on simple and robust connectivity, **not security**

## Protocols and Layers
- **Protocol:** defines message structure (syntax) and meaning (semantics) : what actions taken, when a timer expires.
- **Layering:** abstraction boundaries. Lower layers serve upper layers.
    - Lower : dont care what higher layer do
    - Higher : dont care how lower layer work

## Threat Model
- Attacker can intercept, modify, and inject (send pocket) traffic.
- Cannot assume keeping all bad actors out. 
    - Attacker fully control their machine
    - Attacker can participate in protocol

## Reconnaissance (Recon)
- **Passive:** sniffing (Wireshark, tcpdump). (monitoring)
- **Active:** WHOIS lookup, Nmap scanning, OS fingerprinting. -> Known more about victim

## Link Layer Security
- Provides no confidentiality, integrity, or authentication. -> No security
- Attacks: 
    - Sniffing : Monitoring
    - MAC spoofing: attacker manually changes their own MAC address. Other mechanisms (ARP, switching) behave normally but now treat the attacker as another host (possibly a trusted one).
        - Mainly attack ที่ MAC address table ของ switch อาศัย self-learning 
            - Self learning : Switch จะอัพเดท <MAC,port> ตาม port และ SrcMac ที่รับมาได้
            - การส่ง frame ที่ปลอม SrcMAC จึงทำให้ switch ส่งของมาหาเราแทนได้ 
    - ARP poisoning: broad term — attacker sends forged ARP replies to corrupt other hosts’ ARP tables (maps IP ↔ MAC wrong). -> Man In The Middle
        - ARP spoofing: a specific use of ARP poisoning where the attacker claims “IP X is at my MAC,” tricking others into sending traffic to the attacker.
        - Mainly attack ที่ ARP table  
            - ARP : เมื่อไม่มี <IP,MAC> ที่ต้องการก็จะส่งถามหา(ARP boardcast) แล้วรอ ARP response มาอัพเดท
            - การส่ง ARP Response ที่ปลอม IP addr 
                - Gratuitous ARP : จู่ๆ ก็ไปบอกว่าให้อัพเดท <IP,MAC>
                - ชิงตอบ ARP Response ก่อน, ส่งรัวๆ เพราะอันสุดท้ายจะถูกจำ 
- **Defense:** secure switching (ARP), static ARP (ARP), encryption (Sniffing). Mac addr randomization reduces tracking risk (MAC spoofing).
- New ARP -> ให้ Switch เป็น Trusted ARP Responder (Proxy-ARP) เพราะสวิตช์รู้ IP↔MAC↔Port จาก DHCP snooping อยู่แล้ว ดังนั้นเวลามีเครื่องใดถาม ARP ว่า “ใครคือ IP X?” → สวิตช์ตอบแทน โดยดึงข้อมูลจากตาราง snooping แทนไม่ให้เครื่องอื่นตอบเอง

## Network Layer (IP)
- **Best-effort:** no ordering, retransmission, or security.
- Attacks: IP spoofing, sniffing, DHCP abuse.
    - Routing (BGP) 
        - Routers trust peers → BGP hijacks (e.g., Pakistan–YouTube 2008) -> การหลอกทำให้ packet ไปไม่ถึงเป้าหมาย(DoS ถ้าไม่ส่งต่อ)/ดังฟัง/แก้ไข/inject(MitM ถ้าส่งต่อ)
            - Problem : AS ข้าง ๆ พูดอะไรก็เชื่อ” คือจุดอ่อนหลักของ BGP — ไม่มี authentication, ไม่มี validation.
        - **Defense:** Secure BGP (BGPsec)
            - **Concept:** ใช้ Cryptography ล็อกเส้นทางแบบ "ลูกโซ่ (Chain)" เพื่อป้องกันการสวมรอย
            - **1. Chain of Trust (กุญแจมาจากไหน? - The Hierarchy):**
                - Router ไม่ได้เก็บกุญแจของทุก AS (60,000+) โดยตรง
                - Router เก็บแค่ **Public Key ของ "ผู้คุมกฎ" (Trust Anchors - TA)** เช่น IANA/APNIC ไว้เท่านั้น
                - **Logic:**
                    - Router เชื่อใจ `APNIC` (มี PubKey_APNIC)
                    - `APNIC` เซ็นรับรอง `Certificate_AS1` (ข้างในมี PubKey_AS1)

            - **2. Example Scenario:** (ส่งข้อมูลจาก AS1 -> AS2 -> AS3)
                
                - **Step 1: AS1 (Origin) เริ่มส่ง**
                    - **Goal:** ประกาศว่า "ฉันเป็นเจ้าของ Prefix นี้ และฉันส่งต่อให้ AS2"
                    - `Msg1 = "Prefix: 10.0.0.0/24, Target: AS2"`
                    - `Sig1 = PriKey_AS1(hash(Msg1))`
                    - **Packet Sent to AS2:** `[ Msg1, Sig1, Certificate_AS1 ]`

                - **Step 2: AS2 (Transit) รับของและตรวจสอบ**
                    - **Action 1: ตรวจสอบตัวตน (Identity Check - Chain of Trust)**
                        - เห็น `Certificate_AS1` 
                        - *Check:* หยิบ **PubKey_APNIC** (ที่ตัวเองมี) มาตรวจสอบ `Certificate_AS1` -> **ดึง PubKey_AS1 ออกมาจากใบรับรอง**
                        - ใช้ **PubKey_AS1** แกะ `Sig1` ได้ `RcvHash`
                        - True if `RcvHash` == `hash(Msg)`
                        - *Result:* ข้อความถูกส่งจาก AS1 จริงและระบุ Target เป็น AS2 จริง

                    - **Action 3: ส่งต่อ (Signing)**
                        - `Msg2 = "Target: AS3"`
                        - `Sig2 = PriKey_AS2(hash(concat(Sig1,Msg2)))`
                    - **Packet Sent:** `[ Msg1, Msg2, Sig1, Sig2, Certificate_AS1, Certificate_AS2 ]`

                - **Step 3: AS3 (Validator) ปลายทาง**
                    - **Action:** ต้องตรวจสอบย้อนกลับ 
                    
                    - **Layer 2 (เช็ค AS2):**
                        1. **Check Identity:** ใช้ **PubKey_APNIC** เช็ค `Certificate_AS2` -> ได้ **PubKey_AS2** 
                        2. **Check Sig:** ใช้ **PubKey_AS2** เช็ค `Sig2` -> ยืนยันว่า AS2 ส่งให้ AS3 
                    
                    - **Layer 1 (เช็ค AS1):**
                        1. **Check Identity:** ใช้ **PubKey_APNIC** เช็ค `Certificate_AS1` -> ได้ **PubKey_AS1** 
                        2. **Check Sig:** ใช้ **PubKey_AS1** เช็ค `Sig1` -> ยืนยันว่า AS1 ส่งให้ AS2
                
                - **CuriosityCorner :** 
                    - 1. **Why Encrypt Hash?** Encrypt(hash(Msg)) faster than Encrypt(Msg)  
                    - 2. **Why `concat(Sig1, Msg2)`?** 
                        - *If missing:* Hacker can do a **Cut-and-Paste Attack** (เอา `Sig2` ที่ถูกต้องไปแปะต่อท้าย Route อื่นที่ปลอมขึ้นมา).
                        - *With Sig1:* เหมือนการ "เย็บแม็ก" เอกสารติดกัน ถ้า `Sig1` (หน้าแรก) ถูกฉีกออกหรือเปลี่ยน ค่า Hash จะเปลี่ยน ส่งผลให้ `Sig2` (หน้าสอง) พังทันที -> ยืนยันว่าเส้นทางต่อเนื่องกันจริง (Unbroken Chain).

            - **Comparison: ทำไม BGP Hijack ถึงทำไม่ได้แล้ว?**
                - **Scenario:** Hacker (AS_Evil) พยายามแทรกกลาง
                - **Attack:** Hacker รับ `[Msg1, Sig1]` จาก AS1 มา แล้วอยากเปลี่ยนทางส่งให้ AS3
                - **Problem:**
                    - Hacker ต้องสร้าง `Sig_Evil = PriKey_Evil(Sig1 + "Target: AS3")`
                    - แต่ตอน AS3 ตรวจสอบ AS3 จะเห็นว่าใน `Sig1` (ของ AS1) ระบุ Target เป็น **AS2** (ไม่ใช่ AS_Evil)
                    - **Result:** Chain ขาด! AS3 รู้ทันทีว่า Hacker ไม่ได้รับอนุญาตจาก AS1 -> **Drop Packet!** 
    - IP Fragmentation
        - Large packets split and reassembled.
        - Attacks: 
            - Ping-of-death : สร้าง ICMP packet โม้บอกเกินขนาดที่ reassemble แล้วทำให้เกิด overflow หรือ crash ในระบบ
            - Fragmentation-based DoS (resource exhaustion) : ส่ง fragment จำนวนมาก กินคิวแต่ไม่ส่งอันท้าย -> รอ reassembly ในเครื่อง เปลือง RAM/CPU -> DoS
            - Teardrop / Overlapping-fragment exploit : ส่ง fragment ที่มี offset ทับซ้อนกันอย่างผิดปกติ ทำให้การรวมข้อมูลชนกัน เกิด buffer overwrite หรือ crash ในระบบที่มีการตรวจสอบไม่ดี → อาจทำให้เครื่องล่มหรือรันโค้ดได้
        - **Defense:** packet validation, avoid fragmentation.
    - ICMP Abuse
        - Can be used for redirection or reflection.
        - Smurf attack : ส่ง ICMP echo ไปยัง broadcast address พร้อมปลอม source IP ให้เป็นของเหยื่อ
            ผลลัพธ์ : ทุกเครื่องตอบกลับ (ICMP Reply) ไปหาเหยื่อ → Amplified DoS
        - **Defense:** block directed broadcast packets.
    - Network Scanning and Fingerprinting
        - Tools: Nmap for port/OS detection. 
            - OS fingerprinting : OS แต่ละแบบมีการตอบกลับที่แตกต่างกัน ดูจากการตอบรับมาเช็คว่าเหยื่อเป็น OS อะไร
        - จะได้เลือกอาวุธมาแฮกถูก

## TCP/IP Insecurity Causes
- Legacy design lacked security. (Internet in 1989 was much friendlier place)
    - Most user known each other -> trusted
- Security now handled at higher layers (SSL/TLS, SSH, Kerberos). 
    - Add-on because its didnot been considered at start

## Defenses
- **Firewall:** filters packets by IP/port.
- **IDS:** detects suspicious patterns and logs.
- **IPS:** blocks detected attacks.
- **Rule of thumb:** DROP first, then ACCEPT specific traffic.
- Education and awareness.
- Secure coding and patching.
- Privilege hardening.
- Encryption and monitoring.

## Key Takeaway
Assume the network is untrusted.
