# Authentication

## Definition
- Verifying identity of user (In computer system) or message origin (In communication system).
- Applies to people, documents, software, or systems.

## Authentication Methods
1. **What you know:** 
    - Prearrange question : What is your favorite football player
    - Passwords
    - One-time pad : 1-time pass, highest security password
    - Challenge-response : Car send something (always change), Key encrypt sendback -> Car check , prevent replay attack 
2. **What you have:** Token, ID, smart card, biometric devices.
3. **Who/What you trust:** Third-party (Google, ChulaSSO), proximity/trusted zone(dress like student in campus, security would not check your id).

### Desired Properties for Biomentric
- Universality: Every person should have it (everyone has fingerprints).
- Distinctiveness: No two people should have the same one.
- Permanence: It shouldn't change over time.
- Collectability: It must be easy to scan/measure.

## Authentication Protocols
- Combine multiple methods (e.g., password + token).
- Example: SSH login
    - Client → Server: request connection. (What do you trust : White list)
    - Server → Client: sends random challenge (nonce). (What do you know : Challenge&Response)
    - Client: uses private key or token to sign the challenge.(What do you have : Private key)
    - Server: verifies signature using the client’s public key.

## Zero-Knowledge Password Proof (ZKPP)
- Prove password knowledge without revealing it.
    - ทั้งผู้ใช้และเซิร์ฟเวอร์มี “ค่าลับร่วมกัน” (derived secret)
    - ผู้ใช้ตอบสนองต่อ challenge จากเซิร์ฟเวอร์ด้วยค่าที่คำนวณจากค่ารับ
    - เซิร์ฟเวอร์ตรวจสอบได้ว่าผู้ใช้นั้นรู้จริง โดยไม่เคยเห็นอีกฝ่ายแสดงเลย
- Goal
    - Prevent password theft during transmission.
    - Stop replay attacks (attackers can’t reuse captured data)

- Analogy: girl with key through tunnel -> prove she has a key, but never show the key.
- Difference with Encryption 
    - Difference goal 
        - Encrypt : Hide password
        - ZKPP : Prove we know, but not show
    - Difference transfer 
        - Encrypt : Encrypted Password
        - ZKPP : Anything just for proving
    - Difference Server behavior
        - Encrypt : Decrypt
        - ZKPP : Just check is it correct
- บางส่วนของ ZKPP ใช้หลักการเข้ารหัส (encryption) เป็นองค์ประกอบได้

## Password Security
- History : 
    - Plaintext : Nothing
    - Hashed : One-way function
    - Salted : Adding constant (difference for everyone)
    - Adaptive Hashing (bcrypt, scrypt, Argon2) : Hard to compute (designed for encrypt)
- Strength = function of length, charset, and guess limits.
- Weak passwords follow patterns (e.g., “Password1”).

## Password Hacking
- Dictionary : Use dict -> compute -> try
- Brute-force : Try every possible 
- Rainbow table : Precomputed hashes for instant lookup.
- Replay : ดักจับข้อมูล authentication ที่ valid แล้วเอามันมาใช้ซ้ำ
- Social Engineer : Phishing

## Defensive Measures
- Multi-factor authentication (SMS, authenticator apps).
- Strong password policies.
- Rate-limiting and lockouts.
- Use password managers.

## Implementation Issues
- Human factors, management cost, transferability, SSO, accuracy, communication security.