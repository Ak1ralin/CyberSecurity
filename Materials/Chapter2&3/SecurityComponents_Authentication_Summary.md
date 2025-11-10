# Security Components and Authentication Summary

## Chapter 2 — Security Components

### Security vs Privacy
- **Security:** Controls :  *who can do what when*.
    - Security protects information from unauthorized access, modification, or destruction.
- **Privacy:** Freedom to control access to one’s personal information.
    - Privacy concerns how personal information is collected, used, and shared.
    - Privacy is depending on intent
    - In reality, we always trade privacy for service -> Medical, Social media
- Security enables privacy, but a secure system can still violate privacy if data is used without consent.

### Examples
- Hacker able to compromise a computer (unauthorized access -> Its Security break) but if he seen some information owner dont want you to see then hacker break privacy (depend on owner mind)

### Security Component 
- A security component is any mechanism that make security.

### AAA Security Model : Security Component
1. **Authentication:** Identify the user (“Who are you?”)
2. **Authorization:** Verify permission (“What can you do?”)
3. **Accounting/Auditing:** Track actions (“What did you do?”)
→ Known as the “AAA” or “Three-headed Kerberos”.
- BTW every security have 3A, but having 3A not mean its secure.

### Supporting Concepts
- **Integrity:** Consistency and wholeness of data.  (Should considered)
- **Input Validation:** “All input is evil until proven otherwise.”
- **Threat Modeling:** Identify and mitigate system risks.

### Conclusion
- Secure system needs all 3 components and 2 supporting concepts， but Having all doesn’t guarantee total security.


## Chapter 3 — Authentication

### Definition
- Verifying identity of user (In computer system) or message origin (In communication system).
- Applies to people, documents, software, or systems.

### Authentication Methods
1. **What you know:** 
    - Prearrange question : What is your favorite football player
    - Passwords
    - One-time pad : 1-time pass, highest security password
    - Challenge-response : Car send something (always change), Key encrypt sendback -> Car check , prevent replay attack 
2. **What you have:** Token, ID, smart card, biometric devices.
3. **Who/What you trust:** Third-party (Google, ChulaSSO), proximity/trusted zone(dress like student in campus, security would not check your id).

### Authentication Protocols
- Combine multiple methods (e.g., password + token).
- Example: SSH login
    - Client → Server: request connection. (What do you trust : White list)
    - Server → Client: sends random challenge (nonce). (What do you know : Challenge&Response)
    - Client: uses private key or token to sign the challenge.(What do you have : Private key)
    - Server: verifies signature using the client’s public key.

### Zero-Knowledge Password Proof (ZKPP)
- Prove password knowledge without revealing it.
    - ทั้งผู้ใช้และเซิร์ฟเวอร์มี “ค่าลับร่วมกัน” (derived secret)
    - ผู้ใช้ตอบสนองต่อ challenge จากเซิร์ฟเวอร์ด้วยค่าที่คำนวณจากรหัสผ่าน
    - เซิร์ฟเวอร์ตรวจสอบได้ว่าผู้ใช้นั้นรู้รหัสจริง โดยไม่เห็นรหัสเลย
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

### Password Security
- History : 
    - Plaintext : Nothing
    - Hashed : One-way function
    - Salted : Adding constant (difference for everyone)
    - Adaptive Hashing (bcrypt, scrypt, Argon2) : Hard to compute (designed for encrypt)
- Strength = function of length, charset, and guess limits.
- Weak passwords follow patterns (e.g., “Password1”).

### Password Hacking
- Dictionary : Use dict -> compute -> try
- Brute-force : Try every possible 
- Rainbow table : Precomputed hashes for instant lookup.
- Replay : 
- Social Engineer : Phishing

### Defensive Measures
- Multi-factor authentication (SMS, authenticator apps).
- Strong password policies.
- Rate-limiting and lockouts.
- Use password managers.

### Implementation Issues
- Human factors, management cost, transferability, SSO, accuracy, communication security.
