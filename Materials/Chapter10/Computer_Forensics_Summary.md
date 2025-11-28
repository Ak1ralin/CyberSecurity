# Computer Forensics Summary

## 1. Definition
- **Digital Forensics** combines **law** and **computer science** to collect and analyze data from:
  - Computer systems  
  - Networks (Network Forensics)  
  - Wireless communications  
  - Storage devices  
  - Code analysis  
- Goal: make data **admissible as evidence** in court.

---

## 2. Forensic Process
1. **Acquisition / Imaging**
   - Tools: `dd`, `dc3dd`, `FTK Imager` -> exact bit-for-bit copy of original storage device -> It copies every byte — including deleted files, unallocated space, and file system metadata — into a single file called a forensic image (.dd)
   - imaging = “make a safe, verifiable clone”, while analysis (e.g. with Autopsy) = “examine that clone.”
   - Must be **hashed (ใช้เป็น digital fingerprint)** and **write-blocked** to prevent modification.
2. **Analysis**
   - Visible: folders, images, user files  
   - Hidden: encrypted or deleted files  -> using tool like autopsy
3. **Reporting**
   - Document findings clearly for legal use.

---

## 3. Evidence and Destruction
- Digital evidence can be **altered or destroyed** easily.  
- Solution : Use write blockers and controlled environments.

---

## 4. Data Hiding Techniques : Disguises information from normal view
- **Rename:** Changing name and extension -> make it look harmless/irrelevant
   - Weakness : Forensic tool check file header can compare the extension 
- **Attributes hiding:** Mark as Hidden in OS -> disappears from normal file explorer view
   - Weakness : Visible if system show hidden files
- **Bit-shifting:** Shift binary data to hide content -> file become unreadble (lightweight encryption) -> but easy to crack.
- **Encrypt/Password:** Data unreadble without key
- **Partition hiding (ไม่ mount):** `diskpart remove letter` -> OS won’t display that partition (OS wont mount), though data still exists. 
   - Weakness : Visible to forensic tools that scan unallocated space, analyze disk space 
- **Marking bad clusters (Mount แต่ไม่ใช้เพราะถูก mark ว่าพัง):** FAT file system, attacker can manually mark good clusters as “bad”, so the OS skips them, assuming they are damaged.
   - Weakness : Detectable with modern forensic tools but invisible to casual users.
---

## 5. File Carving
- Reassemble deleted or fragmented files from disk space.
- Computer don't immediately remove data that is deleted.
   - After delete the original data is still present,  but marked as unallocated space, even some or all of the data has been overwritten, the remaining data can still be carved and reviewed.

---

## 6. Steganography & Steganalysis
- **Steganography:** hiding information inside other files (images, audio).
   - เอาข้อความลับซ่อนไว้ในรูปภาพ โดยเปลี่ยนค่า บิตเล็ก ๆ (LSB – Least Significant Bit) ของพิกเซล 
   - ฝังข้อความในไฟล์เสียง/วิดีโอโดยเปลี่ยนค่าที่มนุษย์ฟังไม่ต่าง
   - Keys : Human not noticable to these changes
- **Steganalysis:** detecting and analyzing Steganography.
- **Digital watermarking:** hides ownership info -> บอกว่าไฟล์นี้ของใคร, พยายามเอาตัวรอด. Steganography that for license purpose not hiding information เช่น ช่างภาพซ่อนชื่อใน `.jpg`

---

## 7. Encryption & Password Recovery
- **Encrypted files:** decoded using passphrase or via key escrow (Backup recovery of encryption keys, ระบบ ฝากสำเนากุญแจไว้กับบุคคลที่เชื่อถือได้เพื่อให้สามารถถอดรหัสได้ภายหลังในกรณีจำเป็น).
- **Key sizes:** 128–4096 bits (very hard to crack with modern technology).
- **Password recovery methods:**
  - Brute-force (try all)
  - Dictionary attacks (use word lists)
  - **Rainbow tables** (precomputed hashes), No conversion needed -> faster than dict and brute-force
  - **Salting:** adds randomness to prevent reuse attacks
- Tools: LastBit, AccessData PRTK, Ophcrack, John the Ripper, Passware.

---

## 8. Case Studies
- **Image Tampering:** ปลอมแปลงภาพดิจิทัล เช่น ตัดต่อ เปลี่ยนหน้า ลบวัตถุ เพิ่มสิ่งของในภาพ. เทคนิคตรวจจับ (forensics techniques):
   - ตรวจ pattern ของ lighting / shadows / reflections
   - ตรวจ metadata (EXIF)
   - ตรวจ pixel-level inconsistencies เช่น noise pattern, compression artifacts
   - วิเคราะห์ Error Level Analysis (ELA) เพื่อดูว่าภาพส่วนใดถูกแก้ไข
- **Melissa Virus (1999):** early email-based macro virus.
   - ผู้ใช้เปิดไฟล์ Word ที่ติดไวรัส
   - Macro จะรันอัตโนมัติ → ส่งอีเมลถึง 50 รายชื่อแรกใน Outlook
   - ผู้รับเปิดไฟล์อีก → แพร่ต่อไปแบบ chain reaction
   - แสดงให้เห็นว่า metadata และ macro code สามารถใช้เป็นหลักฐานทางดิจิทัลได้
- **Deepfakes:** GAN-generated สร้างภาพหรือวิดีโอที่เหมือนจริงของคนที่ “ไม่เคยมีอยู่จริง” หรือ “ทำสิ่งที่ไม่ได้ทำจริง” Forensics ต้องใช้เทคนิคใหม่ ๆ เช่น:
   - ตรวจ pattern การกะพริบตา, การเคลื่อนไหวใบหน้า
   - วิเคราะห์ inconsistency ของแสงหรือผิว
   - ใช้ AI-based deepfake detectors

