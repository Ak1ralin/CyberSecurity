# Secure Bit: Buffer Overflow Protection  

## 1. Overview  
Buffer overflow occurs when **data exceeds buffer limits and overwrites adjacent memory**, potentially altering control flow and executing malicious code.  
**Secure Bit** is a hardware-based mechanism designed to prevent such attacks by tracking whether input data is trusted.

---

## 2. History of Major Buffer Overflows  
- 1988 – Morris Worm
  - ลักษณะ: Worm ตัวแรกในประวัติศาสตร์อินเทอร์เน็ต
  - สาเหตุ: ช่องโหว่ buffer overflow ในโปรแกรม fingerd (UNIX) และใช้การเดารหัสผ่านร่วมด้วย
  - ผลกระทบ: ทำให้เครื่องกว่า 10% ของอินเทอร์เน็ตในขณะนั้นล่มหรือติดหนอน ทำให้ระบบช้าหรือไม่ตอบสนอง

- 2001 – Code Red
  - ลักษณะ: Worm โจมตีเซิร์ฟเวอร์ IIS (Internet Information Services) ของ Microsoft
  - สาเหตุ: ช่องโหว่ buffer overflow ใน idq.dll (Index Server ISAPI Extension)
  - ผลกระทบ: แพร่กระจายรวดเร็วทั่วโลก, โจมตีเว็บไซต์ทำ DDoS, โดยเฉพาะที่อยู่ IP ของทำเนียบขาว

- 2003 – Slammer (SQL Slammer)
  - ลักษณะ: Worm ขนาดเพียง 376 bytes แพร่กระจายผ่าน UDP
  - สาเหตุ: ช่องโหว่ buffer overflow ใน Microsoft SQL Server (msde.dll)
  - ผลกระทบ: ภายในไม่กี่นาทีทำให้เครือข่ายทั่วโลกช้าหรือหยุดชะงัก, ATM ของ Bank of America 13,000 เครื่องล่ม, ระบบโรงไฟฟ้านิวเคลียร์ Ohio ล่ม

- 2003 – Blaster & Welchia
  - ลักษณะ: Worm in Windows แพร่ผ่านช่องโหว่ RPC DCOM
  - สาเหตุ: Buffer overflow ในบริการ RPC ของ Windows XP/2000
  - ผลกระทบ: 
    - Blaster: สั่งให้เครื่องรีสตาร์ตเองและโจมตี Windows Update server
    - Welchia: Worm for “แก้แค้น” ที่พยายามลบ Blaster ออก แต่สร้างโหลดบนเครือข่ายมหาศาลจนระบบช้าลง

- 2004 – Witty Worm
  - ลักษณะ: Worm ที่โจมตีFirewall/IDS ของบริษัท Internet Security Systems (ISS)
  - สาเหตุ: ช่องโหว่ buffer overflow ในซอฟต์แวร์ความปลอดภัยของ ISS
  - ผลกระทบ: แพร่กระจายภายในหนึ่งวันหลังจากเผยแพร่ช่องโหว่ (“one-day worm”), เขียนข้อมูลสุ่มทับฮาร์ดดิสก์เหยื่อ

- 2004 – Sasser Worm
  - ลักษณะ: หนอน Windows ที่แพร่โดยไม่ต้องพึ่งอีเมลหรือผู้ใช้
  - สาเหตุ: ช่องโหว่ buffer overflow ใน LSASS (Local Security Authority Subsystem Service)
  - ผลกระทบ: เครื่องรีบูตอัตโนมัติ, ระบบเครือข่ายของสายการบินและโรงพยาบาลหยุดชะงัก

- 2006 – Mac Wireless Overflow
  - ลักษณะ: ช่องโหว่ buffer overflow ใน driver ของการ์ด Wi-Fi บน macOS
  - สาเหตุ: การจัดการ buffer ของ packet ใน wireless stack ไม่ปลอดภัย
  - ผลกระทบ: ผู้โจมตีสามารถส่ง packet เฉพาะเพื่อรันโค้ดบนเครื่อง Mac ได้ (remote code execution)
---

## 3. Buffer Overflow Works  
Example in C using `gets()` → overwrites stack memory. '1' = 0x31 = 49
**Attack types:**  
- Return address modification (stack smashing) = เราเขียนจนทับ Return Address ทำให้มันไปรันอะไรก็ได้, เราเอาโค้ดมาแปะก่อนให้มัน Return กลับมารันยังได้
  - Mandatory Condition
    - 1. Input แปลกเขียนได้ 
    - 2. Address สำคัญ (Return address) โดนแก้
  - Sol : ไม่ให้เกิด 2 conditions พร้อมกัน
    - Input Range/Value Validation : จองเท่าไหร่เขียนได้เท่านั้น
    - Critical Code Validation : ดูว่าถูกแก้หรือไม่ -> digital signature

---

## 4. Detection and Protection Techniques  

### 4.1 Static Analysis (Lexical/Semantic Analysis)
- ตรวจสอบจาก code อย่างคำแบบ strcpy มีโอกาสสูงทำให้เกิด buffer overflow
- Tools: ITS4(String Matching), FlawFinder, RATS, Splint, BOON (Semantic analysis)  
- Pros: Detects known issues pre-deployment  
- Cons: No runtime protection, false positives  

### 4.2 Dynamic Solutions  
Includes:
- **Address Protection:** 
  - Canary Words : มาจาก Canary Bird (นกขมิ้น->อ่อนแอ ตายง่าย) -> จะถูกแก้ก่อน RET โดนแก้
    - กั้นระหว่าง Buffer กับของสำคัญ ถ้า overflow Canary ต้องถูกแก้
    - **StackGuard:** Canary word before return address -> Detect Overwrite
    - ปัญหา : ถ้า hacker รู้ Canary Word ก็แค่เขียนให้ถูกก็พอ 

  - Address Encode : Encrypt Address ทำให้ถึง hacker แก้ได้ แต่เนื่องจากไม่รู้ว่า Encrypt อย่างไร เมื่อเรา Decrypt ก็จะไปที่ไหนไม่รู้ ซึ่งมีโอกาสสูงจะ Crash -> ทำให้เราไม่ไปรันโค้ดที่ hacker อยากให้รัน
    - **PointGuard：** Encrypts pointers  Protects function pointers
    - **SPEF:** Encrypted instruction execution  
    - **Instruction Set Randomization (ISR):** เข้ารหัส/สุ่มคำสั่งด้วย per-process key (เช่น XOR) ทำให้โค้ดที่โจมตีฉีดมาไม่ตรงกับ ISA ที่ถูกถอดรหัสจริง (Columbia / Drexel)
    - ปัญหา : Performance, Compatibility

  - Copy of Address : เก็บ return addr สองที่จริง, เวลาจะ ret จะเทียบสองค่าถ้าไม่ตรงคือถูกเขียนทับ
    - **Split Stack:** Separates control(ret)/data(buffer) stack, มี ret ที่เดียว แยกไว้อยู่
    - ปัญหา : ทับสองที่ก็โดนอยู่ดี

  - Tags :  บิตพิเศษ meta data ที่ติดไปกับแต่ละคำของหน่วยความจำ (memory word) เพื่อบอกว่า ให้แสดงว่า “ข้อมูลนี้มาจากที่มาใด” ถ้าจะใช้ค่านี้เป็น Addr แต่ดันมาจาก input -> ไม่อนุญาต 
    - **Input Protection:** Prevents untrusted data as control data -> secure bit 

- **Bounds Checking:** Validates memory access : จองเท่าไหร่เขียนเท่านั้น — ทางแก้ที่ถูกต้องแต่แพง
  - Array Bounds Checking : Software-level checks
  - Segmentation / hardware bounds : Hardware-level checks
  - **LibSafe / LibVerify:** ห่อ/แทน libc เพื่อตรวจ bounds และกรองการเรียก I/O/strcpy ก่อนเขียนจริง (Bell Labs)
  - ปัญหา : ช้าลงได้มาก (ตัวอย่างในเอกสารอ้างถึง ≈30x slowdown ในบางกรณี)

- **Obfuscation:** ASLR (Address Space Layout Randomization)  -> เดาไม่ได้ว่า RET อยู่ไหน, Hack ได้แต่ยากขึ้นเฉยๆ จากเมื่อก่อนแค่อ่าน Source Code ก็เดาได้แล้ว


### 4.3 Isolation
- Non-executable memory (NX), sandboxing  
  - Memory บางส่วนไม่อนุญาตให้ execute
  - ไม่แก้ root cause แต่ลดผลกระทบได้

### 4.4 Secure Boost
- hash เก็บ kernel code ไว้เป็น digital signature -> ถ้าไม่ตรงไม่ boost
---

## 5. Theory  

**Definition:** Buffer overflow happens when external input modifies addresses.  
**Theorem:** If an address cannot be modified (or modification can be detected), buffer-overflow attack is impossible.  
**Corollary:** Preserving address integrity prevents buffer overflow.

---

## 7. Secure Bit Concept  

**Idea:** Tag all data from untrusted domains with a “Secure Bit.”  
- When data crosses domain boundaries, the bit is set.  
- CPU disallows such data as jump/control targets.  
- Ensures “untrusted input ≠ executable control.”  

**Similar Concept:**
  - "All input is evil until proven otherwise"
  - "Data must be validated as it crosses the boundary between untrusted and trusted environemnts"

---

