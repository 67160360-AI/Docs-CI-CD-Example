# รายงานผลการปฏิบัติการและเฉลยคำถามทบทวน (Lab Report & Answers)

**วิชา:** Continuous Integration and Continuous Deployment (CI/CD)  
**หัวข้อ:** การสร้างระบบ CI/CD Pipeline ด้วย GitHub Actions, Python, pytest และ GitHub Pages  
**ชื่อ-นามสกุล:** นายภัคพล ริตกันโต (Mr. Pakaraphon Ritkanto)  
**รหัสนิสิต:** 67160360  
**อีเมล:** 67160360@go.buu.ac.th  
**GitHub Account:** [67160360-AI](https://github.com/67160360-AI)  
**Repository:** [Docs-CI-CD-Example](https://github.com/67160360-AI/Docs-CI-CD-Example)  
**GitHub Pages URL:** [https://67160360-ai.github.io/Docs-CI-CD-Example/](https://67160360-ai.github.io/Docs-CI-CD-Example/)  

---

## สรุปผลการปฏิบัติการตามหมวด 1 - 9

| หมวด | หัวข้อ | รายละเอียดการดำเนินงานและผลลัพธ์ | สถานะ |
| :--- | :--- | :--- | :---: |
| **หมวด 1** | เตรียมโปรเจกต์ Python | ติดตั้งโครงสร้างโปรเจกต์, `requirements-dev.txt`, `pyproject.toml`, `.gitignore`, `data/scores.csv` พร้อมสร้าง Virtual Environment `.venv` สำเร็จ | **ผ่าน (100%)** |
| **หมวด 2** | เขียน test (pytest) | พัฒนา `grades.py`, `build_site.py` พร้อมชุดทดสอบ `test_grades.py` และ `test_build_site.py` ทดสอบ Unit Test ผ่าน 100% และ Code Coverage สูงกว่า 98% (เกณฑ์ขั้นต่ำ 80%) | **ผ่าน (100%)** |
| **หมวด 3** | CI (ci.yml) | สร้าง Workflow `.github/workflows/ci.yml` รันอัตโนมัติเมื่อ push ตรวจสอบโค้ดด้วย `ruff check .` และทดสอบผ่าน `pytest` แสดงผลผ่าน (เขียว) | **ผ่าน (100%)** |
| **หมวด 4** | CD (deploy) | เพิ่ม Job `deploy` ส่งหน้าเว็บ Static HTML ขึ้น **GitHub Pages** อัตโนมัติเมื่อ Job `test` ผ่านสำเร็จ และตั้งค่า Pages Source เป็น GitHub Actions | **ผ่าน (100%)** |
| **หมวด 5** | Pull Request & Branch Protection | กำหนด Branch Protection Rule ให้สาขา `main`, บังคับให้การผสานโค้ดต้องผ่าน Pull Request และ Status Check เท่านั้น และเพิ่มฟังก์ชัน `pass_rate` พร้อมทดสอบ | **ผ่าน (100%)** |
| **หมวด 6** | Secrets & Variables | กำหนด Configuration Variable `SITE_TITLE` และ Repository Secret `DEMO_API_KEY` ส่งเข้า Python ผ่าน Environment Variables ปลอดภัย | **ผ่าน (100%)** |
| **หมวด 7** | Matrix Build | รัน Job `test` ขนานกันบน Python 3.12, 3.13, 3.14 พร้อมกำหนด `fail-fast: false` เพื่อตรวจความเข้ากันได้ครบทุกเวอร์ชัน | **ผ่าน (100%)** |
| **หมวด 8** | Self-hosted runner | ศึกษาแนวทางการประยุกต์ใช้งาน runner ภายในเครื่องส่วนตัว และข้อควรระวังด้านความปลอดภัยสำหรับการใช้งานเฉพาะกับ Private Repository | **ผ่าน (100%)** |
| **หมวด 9** | แบบฝึกหัดท้าทาย | ทำแบบฝึกหัดข้อ 1-4 ครบถ้วน (เกรดบวก B+/C+, สถิติบนเว็บ, Data Validation ป้องกันชื่อซ้ำ/ว่าง, HTML Coverage Artifact) | **ผ่าน (100%)** |

---

## เฉลยคำถามทบทวนท้ายบท (Review Questions & Answers)

### ข้อ 1: ถ้าเพิ่มไฟล์ `tests/test_report.py` ใหม่ ต้องแก้ `ci.yml` ไหม เพราะอะไร?
**คำตอบ:**  
**ไม่ต้องแก้ไขไฟล์ `ci.yml` เลย** เนื่องจาก `pytest` มีกลไกการค้นหาไฟล์ทดสอบอัตโนมัติ (**Test Discovery**) โดยจะสแกนหาไฟล์ทั้งหมดที่มีชื่อขึ้นต้นด้วย `test_*.py` หรือลงท้ายด้วย `*_test.py` ภายใต้โฟลเดอร์ `tests/` ที่ระบุไว้ใน `pyproject.toml`  
เราจะจำเป็นต้องแก้ไขไฟล์ `ci.yml` ก็ต่อเมื่อมีการเปลี่ยนแปลงคำสั่งรัน เช่น ติดตั้ง Library หรือ Dependency เพิ่มเติม, การปรับเปลี่ยนเกณฑ์เปอร์เซ็นต์ Code Coverage หรือการเพิ่มเวอร์ชันของระบบปฏิบัติการ/ภาษา Python ใน Matrix เท่านั้น

---

### ข้อ 2: GitHub รู้ได้อย่างไรว่า step `pytest` ผ่านหรือไม่ผ่าน?
**คำตอบ:**  
GitHub Actions ตรวจสอบสถานะการทำงานจาก **Exit Code (Process Return Code)** ของคำสั่งที่รันใน Step นั้น:
- หากรันชุดทดสอบแล้วทุกกรณีทดสอบผ่านทั้งหมด และ Code Coverage ไม่ต่ำกว่าเกณฑ์ที่กำหนด (`--cov-fail-under=80`) คำสั่งจะจบการทำงานด้วย **Exit Code = 0** ทำให้ GitHub Actions บันทึกสถานะว่า Step ผ่านสำเร็จ (แสดงเครื่องหมายถูกสีเขียว)
- หากมีกรณีทดสอบใดไม่ผ่าน (`AssertionError` หรือ Error อื่น ๆ) หรือ Code Coverage ต่ำกว่าเกณฑ์ที่กำหนด `pytest` จะส่งคืนค่า **Exit Code != 0** (โดยทั่วไปคือ Exit Code 1) ส่งผลให้ GitHub Actions ทราบทันทีว่ากระบวนการล้มเหลว (Failed) และแสดงเครื่องหมายกากบาทสีแดง พร้อมหยุดการทำงานและข้ามขั้นตอนที่เหลือทันที

---

### ข้อ 3: บรรทัดไหนใน `ci.yml` ที่ทำให้เว็บไม่ถูก deploy เมื่อ test พัง?
**คำตอบ:**  
คือคำสั่ง:
```yaml
needs: test
```
ซึ่งระบุอยู่ภายใต้ Job `deploy` โดย `needs` เป็นตัวกำหนดความสัมพันธ์แบบลำดับขั้น (**Job Dependency**) บังคับให้ Job `deploy` จะเริ่มทำงานได้ก็ต่อเมื่อ Job `test` ทำงานเสร็จสิ้นด้วยสถานะสำเร็จ (Success) เท่านั้น หาก Job `test` ล้มเหลว (Failed) ระบบ GitHub Actions จะทำเครื่องหมายข้าม Job `deploy` ทันที (**Skipped**) ส่งผลให้ไม่มีการเผยแพร่โค้ดหรือข้อมูลที่ผิดพลาดขึ้นสู่หน้าเว็บไซต์จริง

---

### ข้อ 4: ทำไมต้อง test คะแนน 80 และ 79 ทั้งคู่ ทั้งที่ test 65 ก็ผ่านแล้ว?
**คำตอบ:**  
เพราะคะแนน **80** และ **79** คือ **"ค่าขอบเขต (Boundary Values)"** ซึ่งเป็นจุดรอยต่อในการตัดสินเกรด (เกรด A และเกรด B/B+)  
บั๊กในโปรแกรมส่วนใหญ่มักเกิดขึ้นจากการเขียนตัวดำเนินการเปรียบเทียบผิดพลาด เช่น ผู้พัฒนาเผลอเขียนเงื่อนไข `if score > 80:` แทนที่จะเป็น `if score >= 80:` ซึ่งหากเราทดสอบเฉพาะค่าตรงกลาง เช่น คะแนน 65 หรือ 85 โค้ดที่มีข้อผิดพลาดนี้จะยังคงผ่านการทดสอบได้โดยที่เราไม่รู้ตัว การทดสอบครอบคลุมทั้งค่าขอบล่างของเกรดบน (80) และค่าขอบบนของเกรดถัดไป (79) จึงเป็นหัวใจสำคัญของเทคนิค **Boundary Value Analysis** เพื่อดักจับข้อผิดพลาดได้อย่างแม่นยำ

---

### ข้อ 5: ทำไมไม่ commit โฟลเดอร์ `_site` และ `.venv` ขึ้น repo?
**คำตอบ:**  
1. **โฟลเดอร์ `_site/`:** เป็นผลลัพธ์จากการประมวลผล (**Build Artifact**) ซึ่งสามารถสร้างขึ้นใหม่ได้เสมอจาก Source Code (`build_site.py`) และข้อมูลดิบ (`data/scores.csv`) การปล่อยให้กระบวนการ CD บน GitHub Actions เป็นผู้สร้างไฟล์นี้ขึ้นใหม่สด ๆ ทุกครั้ง จะรับประกันว่าข้อมูลบนหน้าเว็บจะสอดคล้องกับโค้ดล่าสุดเสมอ อีกทั้งยังช่วยลดขนาดของ Git Repository และป้องกันปัญหาความขัดแย้งของไฟล์ (Merge Conflicts)
2. **โฟลเดอร์ `.venv/`:** เป็น Virtual Environment ที่เก็บไฟล์ Binary, ไดนามิกลิงก์ และ Library ที่คอมไพล์สำหรับเครื่องและระบบปฏิบัติการของผู้พัฒนาเครื่องนั้น ๆ โดยเฉพาะ (**Platform-dependent**) จึงไม่สามารถนำไปรันข้ามระบบปฏิบัติการอื่นได้โดยตรง อีกทั้งมีขนาดใหญ่และมีจำนวนไฟล์มหาศาล แนวทางปฏิบัติสากลจึงเก็บเพียงรายการชื่อแพ็กเกจใน `requirements-dev.txt` เพื่อให้ผู้อื่นหรือ CI Server สามารถติดตั้ง Environment ที่สะอาดและตรงกันได้อย่างเป็นมาตรฐาน

---

### ข้อ 6: Secret กับ Variable ต่างกันอย่างไร ยกตัวอย่างค่าที่ควรเก็บแบบละ 2 อย่าง?
**คำตอบ:**  
- **Secret (GitHub Actions Secrets):** ใช้จัดเก็บข้อมูลที่มีความอ่อนไหวสูงและเป็นความลับ ระบบ GitHub จะเข้ารหัสข้อมูล และเมื่อนำไปใช้งานใน Workflow ค่าจริงจะถูกปิดบังอัตโนมัติ (**Masked**) แสดงเป็น `***` ใน Logs ทั้งหมด รวมถึงถูกจำกัดการเข้าถึงจาก Pull Request ภายนอก (Forks)
  * *ตัวอย่างที่ควรเก็บ:*
    1. API Keys หรือ Access Tokens (เช่น `DEMO_API_KEY`, Stripe Secret Key)
    2. รหัสผ่านฐานข้อมูล (Database Password) หรือ SSH Private Key สำหรับเข้าสู่เซิร์ฟเวอร์
- **Variable (GitHub Actions Configuration Variables):** ใช้จัดเก็บค่าตัวแปรคอนฟิกทั่วไปที่ไม่เป็นความลับ สามารถเปิดดู ตรวจสอบ แก้ไข และเห็นค่าจริงได้ใน Settings และใน Logs ของ Workflow ได้อย่างเปิดเผย
  * *ตัวอย่างที่ควรเก็บ:*
    1. หัวข้อของเว็บไซต์ (เช่น `SITE_TITLE`: "ผลคะแนนกลางภาค 2/2569")
    2. URL ปลายทางของ API, Service Port หรือ Environment Name (เช่น `ENVIRONMENT`: "production")

---

### ข้อ 7: Matrix `os: [ubuntu-latest, windows-latest, macos-latest]` กับ `python-version: ["3.12", "3.13"]` จะได้กี่ job?
**คำตอบ:**  
จะได้ทั้งหมด **6 Jobs**  
ซึ่งคำนวณจากผลคูณคาร์ทีเซียน (Cartesian Product) ระหว่างจำนวนค่าในแต่ละมิติ:  
\[ 3 \text{ (ระบบปฏิบัติการ)} \times 2 \text{ (เวอร์ชัน Python)} = 6 \text{ Jobs} \]  
ได้แก่:
1. `ubuntu-latest` + Python 3.12
2. `ubuntu-latest` + Python 3.13
3. `windows-latest` + Python 3.12
4. `windows-latest` + Python 3.13
5. `macos-latest` + Python 3.12
6. `macos-latest` + Python 3.13

---

### ข้อ 8: ทำไมไม่ควรใช้ self-hosted runner กับ public repo?
**คำตอบ:**  
เพราะเป็น **ช่องโหว่ความปลอดภัยระดับร้ายแรงสูงสุด (Critical Security Vulnerability)**  
บน Public Repository บุคคลภายนอกทุกคนบนอินเทอร์เน็ตสามารถทำ Fork คัดลอกโปรเจกต์ แล้วแก้ไขไฟล์คำสั่งใน `.github/workflows/` เป็นสคริปต์อันตรายใด ๆ ก็ได้ จากนั้นส่ง Pull Request กลับเข้ามาที่ Repository หลัก ซึ่งจะส่งผลให้ GitHub Actions สั่งรันคำสั่งอันตรายนั้นบนเครื่อง Self-hosted Runner ของเราทันที ผู้โจมตีสามารถขโมยข้อมูลไฟล์ส่วนตัวในเครื่อง, ล้วงรหัสผ่าน, เข้าถึงระบบเครือข่ายภายในองค์กร หรือฝัง Ransomware ได้ ดังนั้น GitHub จึงมีคำเตือนอย่างชัดเจนว่า **ต้องใช้ Self-hosted runner กับ Private Repository ที่จำกัดสิทธิ์ผู้มีส่วนร่วมเท่านั้น**

---

## รายละเอียดการทำแบบฝึกหัด (หมวด 9)

### 1. เกรดบวก (B+ และ C+)
- ปรับปรุงฟังก์ชัน `grade(score)` ใน `grades.py` ให้รองรับช่วงคะแนน:
  - 80–100: **A**
  - 75–79: **B+**
  - 70–74: **B**
  - 65–69: **C+**
  - 60–64: **C**
  - 50–59: **D**
  - 0–49: **F**
- เขียนกรณีทดสอบค่าขอบเขต (Boundary Tests) ครอบคลุมทั้ง 80, 79, 75, 74, 70, 69, 65, 64, 60, 50, 49 และ 0 ใน `tests/test_grades.py`

### 2. สถิติเพิ่มเติมบนหน้าเว็บ
- ขยายฟังก์ชัน `render_html()` ใน `build_site.py` ให้แสดงข้อมูลสรุปเพิ่มเติม:
  - ค่าเฉลี่ยคะแนน (`ค่าเฉลี่ย: ...`)
  - คะแนนสูงสุด (`คะแนนสูงสุด: ...`)
  - คะแนนต่ำสุด (`คะแนนต่ำสุด: ...`)
  - เปอร์เซ็นต์ผู้สอบผ่าน (`อัตราการสอบผ่าน: ...%`)
- เขียนชุดทดสอบใน `tests/test_build_site.py` เพื่อตรวจสอบว่าหน้าเว็บมีส่วนแสดงผลสถิติเหล่านี้ครบถ้วน

### 3. การตรวจสอบข้อมูล CSV อย่างเข้มข้น (Data Validation)
- พัฒนาฟังก์ชัน `load_scores()` ใน `build_site.py` ให้ตรวจสอบ:
  - ชื่อนักเรียนต้องไม่เป็นค่าว่าง (`ValueError: ชื่อต้องไม่เป็นค่าว่าง`)
  - ชื่อนักเรียนต้องไม่ซ้ำกัน (`ValueError: พบชื่อซ้ำในระบบ`)
  - คะแนนต้องอยู่ในช่วง 0–100 เท่านั้น
- เขียนชุดทดสอบ `test_load_scores_empty_name`, `test_load_scores_duplicate_name`, และ `test_load_scores_invalid_score`

### 4. รายงาน Code Coverage เป็นไฟล์ HTML Artifact
- เพิ่มคำสั่ง `--cov-report=html` ในขั้นตอนรัน pytest
- ใช้ Action `actions/upload-artifact@v4` อัปโหลดโฟลเดอร์ `htmlcov/` ขึ้นเป็น Artifact ในแท็บ Actions เพื่อให้สามารถดาวน์โหลดรายงาน Coverage แบบละเอียดไปเปิดดูบนเว็บเบราว์เซอร์ได้
