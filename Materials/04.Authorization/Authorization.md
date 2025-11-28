# Authorization 

## 1. Core Concepts

-   **Authorization**: "What can you do?" -> **Policy will tell you**
    - **Policy (Law) :** Help to decide 
        - App-specific decision-making based on policy : Samething action is different in different application -> No general AuthZ can use for every application
        - Type Enforcement (Police) : Enforce to follow policy
-   **Security Policy**: Clearly define what is secure or insecure, We cannot say something is "safe" unless we define what "safe/unsafe" looks like   
-   **Secure System**:  Start Secure + No Insecure Moves = Always Secure.
    1. Starts in a secure state 
    2. Cannot enter an insecure state.

## 2. Building a Security Policy

Policies often revolve around the **CIA triad**: Know about the system is key.
- **Confidentiality** -- Who can read data?
    - Only the right person can access the data.
- **Integrity** -- Who can modify data?
    - Data is not being altered by unauthorized user.
- **Availability** -- Data/services remain accessible when needed.
- Most **Hacking** is breaking one of these 
    - Break C : Monitoring/Hack into Database
    - Break I : Modify Data
    - Break A : DoS 

## 3. Access Control Models

- Mandatory Access Control (MAC)
    -   Admin-defined policies; users untrusted.
    -   Multilevel system : Higher Level is king.

- Discretionary Access Control (DAC)
    -   Owner-defined policies
    -   Common in personal computing/drive.

- Role-Based Access Control (RBAC)
    -   Who know about role defined policies
    -   Based on least privilege; access tied to job roles.
    -   No clear definition on how to define a role lead to **Role Explosion**
        - "Nurse" role. 
        - "Nurse who works night shift" role
        - "Nurse who works night shift and handles X-rays." 
        - Suddenly, you have 1,000 roles, and it's a mess.

- Attribute-Based Access Control (ABAC)
    -   Decisions use attributes to map access ability.
    -   Attributes : User att, Resource att, Environmental att

- Modern Access Control
    -   **OAuth 2.0 / OIDC**: Limit-Accessed Pass
    -   **Zero Trust Architecture**: Never Trust, Always Verify

## 5. Access Control Matrix

-   Table mapping subjects to objects and permissions from Policy.
-   Table is too big (150*20k ~ 3000k) to store in one place, so we need to break it.
-   Implemented via: 
    -   **Access Control Lists (ACL)** -- object-centric, **Popular**
        - Each user/role can do what to this resource, attached to Resource
        - ห้อง (resource) ที่มีแผ่นกระดาษแปะว่าใครทำอะไรกับห้องนี้ได้บ้าง
    -   **Capability-based System** -- subject-centric, like tokens/keys
        - This user/role can do what to each resource, attached to Subject
        - บุคคล (user/role) ที่มีกระดาษดูได้ว่าตัวเองทำอะไรกับห้องอะไรได้บ้าง
- ทำไม Capability ถึงแก้ปัญหาความปลอดภัยได้ดีกว่า?
    - **ACL:** เกิดปัญหา **"The Confused Deputy" (ผู้ช่วยสับสน)**
        - **ระบบ ACL:** เช็คแค่ว่า "โปรแกรมนี้คือใคร" (เช่น เป็นแอดมิน)
        - **ช่องโหว่:** หลอกโปรแกรมได้ โปรแกรมเผลอใช้อำนาจทำเรื่องไม่ดีได้ 
        - **Capability:** แก้ได้เพราะโปรแกรมไม่มีอำนาจในตัว ทำได้เมื่อ User ให้ key เท่านั้น
        - **Result:** ถึงหลอกโปรแกรมได้ ก็ทำอะไรไม่ได้เพราะไม่มี "key" ให้ program
    - Granularity 
        - Capability ยัง "ให้สิทธิ์แบบละเอียด" ได้คล้าย Limit-accessed key
- ทำไมเรายังใช้ Capability แทน ACL ทั้งหมดไม่ได้?
    ถึงจะดีกว่า แต่มีอุปสรรคใหญ่ 3 ข้อในโลกความจริง:
    1.  **การริบคืนสิทธิ์ (Revocation) - *ยากที่สุด***
        * **ACL:** แค่ลบชื่อออกจากบัญชี จบ! (ง่ายมาก)
        * **Capability:** ต้องตามไปขอ key และไม่รู้ key กระจายไปไหนบ้าง (track ไม่ได้)

    2.  **ระบบเก่า (Legacy Systems)**
        * Windows, Linux, macOS สร้างมา 30-40 ปีบนพื้นฐาน ACL
        * การเปลี่ยนเป็น Capability ต้องรื้อระบบโลกคอมพิวเตอร์ใหม่หมด (ต้นทุนมหาศาล)

    3.  **การตรวจสอบ (Auditing)**
        * **ACL:** ตอบได้ทันทีว่า "ใครเข้าห้องนี้ได้บ้าง" (ดูรายชื่อ)
        * **Capability:** ตอบไม่ได้ เพราะ attached to user
## 6. Security Models
Predefine Policy (Blueprint) -> GuideLine 
- Multilevel Security : Within Org, MAC
    - Bell-LaPadula (Confidentiality) : Focus = Secrets
        -   No Read Up (NRU), No Write Down (NWD)
        -   Prevents information leaks.
        -   หน่วยงานราชการ, กองทัพ ที่ "ความลับ" สำคัญที่สุด
    - Biba (Integrity) : Focus = Trust/Truth
        -   No Read Down, No Write Up
        -   Prevents corruption from lower-integrity sources.
        -   ธนาคาร, ระบบฐานข้อมูล ที่ "ความถูกต้อง" สำคัญที่สุด
- Multilateral Security : China Wall Model 
    -   Conflict of Interest : Dynamically blocking access to competitor data.
    -   สำนักงานกฎหมาย, บริษัทโฆษณา, ตลาดหลักทรัพย์ เพื่อป้องกันไม่ให้คนกลางเอาข้อมูลของลูกค้า A ไปขายให้ลูกค้า B 

## 7. Policy Development Steps
1.  Analyze security model (Bell-LaPadula, Biba, China Wall).
2.  Choose access control model (MAC, DAC, RBAC, ABAC).
3.  Convert policy → Access Control Matrix.
4.  Implement via Type Enforcement (ACLs, Capabilities).
