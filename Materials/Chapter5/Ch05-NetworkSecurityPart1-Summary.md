# Chapter 5 – Network Security (Part 1)

## 1. Introduction
- Purpose: Understand how systems are attacked and defended.
- Quote: “Attack is the secret of defense; defense is the planning of an attack.” — Sun Tzu

## 2. How Systems Are Hacked
- **Remotely:** Exploit network services, remote login, impersonate users.
- **Locally:** Social engineering, exploiting local vulnerabilities.

## 3. Network Fundamentals
- The Internet provides **best-effort** packet delivery (no guarantee).
- **Packet = Header + Payload.**
- **IP Address:** unique identifier of host.
- **Design principle:** simple, dumb network; complexity handled by endpoints.
    - The focus has been on simple and robust connectivity, **not security**

## 4. Protocols and Layers
- **Protocol:** defines message structure (syntax) and meaning (semantics) : what actions taken, when a timer expires.
- **Layering:** abstraction boundaries. Lower layers serve upper layers.
    - Lower : dont care what higher layer do
    - Higher : dont care how lower layer work

## 5. Threat Model
- Attacker can intercept, modify, and inject(send pocket) traffic.
- Cannot assume keeping all bad actors out. 
    - Attacker fully control their machine
    - Attacker can participate in protocol

## 6. Reconnaissance (Recon)
- **Passive:** sniffing (Wireshark, tcpdump). (monitoring)
- **Active:** WHOIS lookup, Nmap scanning, OS fingerprinting. -> Known more about victim

## 7. Link Layer Security
- Provides no confidentiality, integrity, or authentication. -> No security
- By ARP -> So the frame is actually send to others
- Attacks: 
    - Sniffing : Monitoring
    - MAC spoofing: attacker manually changes their own NIC’s MAC address. Other mechanisms (ARP, switching) behave normally but now treat the attacker as another host (possibly a trusted one).
    - ARP poisoning: broad term — attacker sends forged ARP replies to corrupt other hosts’ ARP tables (maps IP ↔ MAC wrong). -> Man In The Middle
        - ARP spoofing: a specific use of ARP poisoning where the attacker claims “IP X is at my MAC,” tricking others into sending traffic to the attacker.
- **Defense:** secure switching (ARP), static ARP (ARP), encryption (Sniffing). Mac addr randomization reduces tracking risk (MAC spoofing).
- New ARP -> ให้ Switch เป็น Trusted ARP Responder (Proxy-ARP) เพราะสวิตช์รู้ IP↔MAC↔Port จาก DHCP snooping อยู่แล้ว ดังนั้นเวลามีเครื่องใดถาม ARP ว่า “ใครคือ IP X?” → สวิตช์ตอบแทน โดยดึงข้อมูลจากตาราง snooping แทนไม่ให้เครื่องอื่นตอบเอง

## 8. Network Layer (IP)
- **Best-effort:** no ordering, retransmission, or security.
- Attacks: IP spoofing, sniffing, DHCP abuse.
    - Routing (BGP) 
        - Routers trust peers → BGP hijacks (e.g., Pakistan–YouTube 2008) -> การหลอกทำให้ packet ไปไม่ถึงเป้าหมาย(DoS ถ้าไม่ส่งต่อ)/ดังฟัง/แก้ไข/inject(MitM ถ้าส่งต่อ)
            - Problem : AS ข้าง ๆ พูดอะไรก็เชื่อ” คือจุดอ่อนหลักของ BGP — ไม่มี authentication, ไม่มี validation.
        - **Defense:** Secure BGP (cryptographic signing).
            - เพิ่ม “ลายเซ็นดิจิทัล (digital signature)”ลงไปในเส้นทางที่ประกาศเพื่อยืนยันว่า
                - แต่ละ AS ในเส้นทางมีตัวตนจริง (authenticated)
                - ลำดับของ AS ที่ส่งต่อ route ถูกต้อง ไม่ถูกแทรกหรือแก้
                - example : 
                    - `AS1 ลงนามว่า “ฉันส่ง route นี้ต่อให้ AS2”` -PrivateKeyAS1-> `Sig1`
                    - `AS2 ลงนามว่า “ฉันได้รับจาก AS1 และส่งต่อให้ AS3”`-PrivateKeyAS2-> `Sig2`
                    - `AS3 ลงนามว่า “ฉันคือผู้ถือ prefix จริง”`-PrivateKeyAS3-> `Sig3`

                What we get is `AS_PATH = [AS1, AS2, AS3]
                Signatures = [Sig1, Sig2, Sig3]` 
                
                Router check ครบทุก Sig -> ต่อให้ได้ AS2 ก็แก้ AS1 ไม่ได้
    - IP Fragmentation
        - Large packets split and reassembled.
        - Attacks: 
            - Ping-of-death : สร้าง ICMP packet ขนาดเกินขนาดที่ reassemble แล้วทำให้เกิด overflow หรือ crash ในระบบ
            - Fragmentation-based DoS (resource exhaustion) : ส่ง fragment จำนวนมาก กินคิวการรอ reassembly ในเครื่อง เปลืองหน่วยความจำ/CPU -> DoS
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
        - Risk: may trigger IDS alerts.

## 9. TCP/IP Insecurity Causes
- Legacy design lacked security. (Internet in 1989 was much friendlier place)
    - Most user known each other -> trusted
- Security now handled at higher layers (SSL/TLS, SSH, Kerberos). 
    - Add-on because its didnot been considered at start

## 10. Defenses
- **Firewall:** filters packets by IP/port.
- **IDS:** detects suspicious patterns and logs.
- **IPS:** blocks detected attacks.
- **Rule of thumb:** DROP first, then ACCEPT specific traffic.
- Education and awareness.
- Secure coding and patching.
- Privilege hardening.
- Encryption and monitoring.

## 11. Key Takeaway
Assume the network is untrusted.
