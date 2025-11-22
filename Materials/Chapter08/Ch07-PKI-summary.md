# Chapter 7 – Public Key Infrastructure (PKI)

## 1. Encryption Revisit
| Type | Strengths | Weaknesses |
|------|------------|-------------|
| **Hash/Digest** | Fastest, ensures integrity | No confidentiality |
| **Symmetric Encryption** | Fast, provides confidentiality | Poor scalability (n เลือก 2 keys needed), integrity uncertain, no non-repudiation |
| **Asymmetric Encryption** | Confidentiality, integrity, scalable (2n keys needed), non-repudiation | 100–1000× slower than symmetric encryption |

Combination of these methods can solve most issues **except authentication**.

---

## 2. Asymmetric Encryption
- Keep **private key** secret; share **public key** freely.  
- One key pair per person → good scalability.  
- Use cases:  
  - **Confidentiality** (encrypt with public key) -> only private key can read
  - **Integrity** (verify with public key) -> digital signature 
    - digital signature : hash(received message) ต้องเท่ากับ public(DigSig)

---

## 3. Missing Link – Authentication
Even with public keys, we cannot prove ownership without binding a key to an identity. -> ไม่รู้ว่า public key อันนี้เป็นของใครเพราะในตัว public key ไม่มี identity signature -> ทำให้ public key นี้น่าเชื่อถือผ่านคนกลางที่น่าเชือถือ (Certificate Authority)

---

## 4. Digital Certificate 
- Binds an entity’s **public key** to its identity attributes.  
- Issued and digitally signed by a trusted third party (CA).  
- A ส่ง publicKeyA ให้ CA แล้ว CA คืน Digital Certificate ให้ซึ่งคือ privateKeyC(Cert,publicKeyA)
- B ที่เชื่อ CA เหมือนกัน(มี publicKeyC) A ส่ง Digital Certificate ให้, B decrypt ก็จะเห็น publicKeyA และ Cert ที่ CA ออกให้ A -> น่าเชื่อถือ 

---

## 5. Trust Model – Web of Trust
If a trusted entity signs a certificate, you trust the certificate and its subject.

Example chain:  
**Digicert Inc (Root CA) → Thawte TLS RSA (CA) → www.chula.ac.th**

---

## 6. Anatomy of a Certificate
- Issuer : ใครออกให้
- Subject : เจ้าของใบรับรอง
- Subject Public Key : PublicKey
- Issuer Digital Signature : ลายเซ็น ที่ Issuer ใช้ private key เซ็น certificate ของ Subject -> ใช้ตรวจได้โดย Public Key ของ Issuer (chain ได้มาหรือ root store)

---

## 7. Self-Signed Certificates
Anyone can create and sign their own certificate.  
Trust depends on manual verification by the recipient.
> Root CA เซ็นให้ตัวเอง

---

## 8. Legal and Operational Issues
> ที่เรียกว่า Infrastructure เพราะมีการนำ real-world มาช่วยกำกับ ไม่ได้ทำทั้งหมดใน digital world

---

## 9. Public Key Infrastructure (PKI)
A system of roles, policies, and procedures to manage digital certificates.

Functions:
- Register, create, store, distribute, validate, revoke public keys  
- Bind public keys to identities organization or person  

Standards: **X509** defined by IETF (Internet Engineering Task Force)

---

## 10. PKI Parties and Roles
- **CA (Certificate Authority):** key generation, issuance, revocation, backup, cross-certification : ทำ Cert ให้ 
- **RA (Registration Authority):** verify identity (face-to-face or remote), revoke requests : ตรวจคุณสมบัติของผู้ขอก่อนจะส่งให้ CA ทำ
- **VA (Verification Authority):**  คนตรวจสอบ Cert ตอนใช้งาน 
- **Certificate Distribution System:** certificates + CRLs (typically via LDAP) : คลังเก็บและศูนย์กลางตรวจสอบสถานะใบรับรอง ในระบบ PKI.
  - ให้บริการดาวน์โหลด/ตรวจสอบใบรับรอง ของผู้ใช้หรือเว็บไซต์
  - เผยแพร่ CRL เพื่อให้ทุกคนรู้ว่าใบรับรองใดถูกยกเลิกแล้ว
- **Other components:** VA, policy database, PKI-enabled apps

---

## 11. PKI Lifecycle
1. Enrollment : ลงทะเบียนขอใบรับรอง
2. Issuance : ออกใบรับรอง
3. Validation : ตรวจสอบความถูกต้อง

---

## 12. Trust in CAs
- Hierarchical trust and cross-certification.  
- Legal liability defined by Certificate Policy (CP) and Certificate Practice Statement (CPS).

---

## 13. Root Certificates and Incidents
If a malicious root certificate is installed, the attacker can forge trust for any site.

**Example:** WoSign/StartCom (2016)  
- Unauthorized issuances  
- SHA-1 backdating  
- Concealment → root cert revoked by browsers  

---

## 14. Conclusion
- PKI is the infrastructure for managing digital certificates.  
- Validates identity of public key owners.  
- Policy and legal aspects exist but not covered in this chapter.
