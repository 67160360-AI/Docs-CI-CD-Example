# 🚀 ระบบ CI/CD อัตโนมัติด้วย Python และ GitHub Actions

[![CI/CD](https://github.com/67160360-AI/Docs-CI-CD-Example/actions/workflows/ci.yml/badge.svg)](https://github.com/67160360-AI/Docs-CI-CD-Example/actions/workflows/ci.yml)
![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue?logo=python)
![Code Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)
![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Site-success?logo=github)

โปรเจกต์ระบบอัตโนมัติ **CI/CD (Continuous Integration / Continuous Deployment)** สำหรับการประมวลผลคะแนน ประกาศผลเกรด และแสดงผลสถิติภาพรวมผ่านหน้าเว็บ **GitHub Pages** อัตโนมัติทุกครั้งที่มีการส่งโค้ดขึ้นระบบ

---

## 👤 ข้อมูลผู้จัดทำ

- **ชื่อ-นามสกุล:** นายภัคพล ริตกันโต (Mr. Pakaraphon Ritkanto)
- **รหัสนิสิต:** 67160360
- **อีเมล:** 67160360@go.buu.ac.th
- **GitHub Repository:** [https://github.com/67160360-AI/Docs-CI-CD-Example](https://github.com/67160360-AI/Docs-CI-CD-Example)
- **🌐 หน้าเว็บไซต์จริง (GitHub Pages):** [https://67160360-ai.github.io/Docs-CI-CD-Example/](https://67160360-ai.github.io/Docs-CI-CD-Example/)
- **📝 เอกสารสรุปคำถามทบทวนและแบบฝึกหัด:** [ANSWERS.md](ANSWERS.md)

---

## 🏗️ แผนภาพสถาปัตยกรรม CI/CD Pipeline

```mermaid
flowchart TD
    A["Push / Pull Request ไปยัง main"] --> B["GitHub Actions Triggered"]
    
    subgraph Job_Test["Job: test (Matrix Build บน Python 3.12, 3.13, 3.14)"]
        B --> C1["Set up Python Environment"]
        C1 --> C2["Install Dependencies (pip cache)"]
        C2 --> C3["Code Linter (ruff check .)"]
        C3 --> C4["Unit Tests & Coverage (pytest >= 80%)"]
        C4 --> C5["Upload HTML Coverage Report Artifact"]
    end
    
    C4 -->|ถ้ามีข้อผิดพลาด| D["❌ สั่งหยุดทันที (Job Failed)"]
    D --> E["ไม่ทำการ Deploy สู่ระบบจริง"]
    
    C4 -->|ผ่านการทดสอบทั้งหมด| F{"เป็น Pull Request หรือไม่?"}
    F -->|ใช่ (PR)| G["รอตรวจสอบ Code Review & Merge"]
    F -->|ไม่ใช่ (Push ไปยัง main)| H["Job: deploy (Deploy to GitHub Pages)"]
    
    subgraph Job_Deploy["Job: deploy"]
        H --> I1["Read SITE_TITLE from GitHub Variables"]
        I1 --> I2["Check DEMO_API_KEY from Secrets"]
        I2 --> I3["Build Static Web (_site/index.html)"]
        I3 --> I4["Configure & Upload Pages Artifact"]
        I4 --> I5["Deploy to GitHub Pages Environment"]
    end
    
    I5 --> J["🌐 เว็บไซต์อัปเดตผลคะแนนสดอัตโนมัติ"]
```

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
Docs-CI-CD-Example/
├── .github/
│   └── workflows/
│       └── ci.yml               # Workflow กำหนด CI/CD Pipeline ทั้งหมด
├── data/
│   └── scores.csv               # ข้อมูลคะแนนนักเรียน (UTF-8)
├── tests/
│   ├── test_grades.py           # Unit Tests สำหรับฟังก์ชันคำนวณเกรดและค่าเฉลี่ย
│   └── test_build_site.py       # Integration Tests สำหรับการอ่านไฟล์และสร้าง HTML
├── grades.py                    # โมดูลคำนวณเกรด, ค่าเฉลี่ย, และอัตราการสอบผ่าน
├── build_site.py                # สคริปต์ประมวลผลข้อมูลและสร้างเว็บเพจ (_site/index.html)
├── requirements-dev.txt         # รายการแพ็กเกจสำหรับ Development & Testing
├── pyproject.toml               # กำหนดค่า Path และการรันของ pytest
├── .gitignore                   # ระบุไฟล์และโฟลเดอร์ที่ไม่นำขึ้น Git
├── ANSWERS.md                   # รายงานและเฉลยคำถามทบทวนประจำแลป
└── README.md                    # เอกสารแนะนำและคู่มือการใช้งานโปรเจกต์
```

---

## 🛠️ วิธีการรันและทดสอบบนเครื่องส่วนตัว (Local Execution)

### 1. ติดตั้ง Virtual Environment
```bash
# บน Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate

# บน macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements-dev.txt
```

### 3. ตรวจสอบคุณภาพโค้ด (Linting)
```bash
ruff check .
```

### 4. รันชุดทดสอบพร้อมวัดเปอร์เซ็นต์ Code Coverage
```bash
pytest --cov=grades --cov=build_site --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

### 5. ทดสอบสร้างหน้าเว็บในเครื่อง
```bash
# กำหนดหัวข้อเว็บจำลอง (PowerShell)
$env:SITE_TITLE = "ผลคะแนนสอบทดสอบบนเครื่อง"
python build_site.py

# เปิดดูผลลัพธ์ผ่านเว็บเบราว์เซอร์
start _site/index.html
```

---

## 📋 สรุปความสมบูรณ์ตามข้อกำหนดของโจทย์ (Checklist)

- [x] **หมวด 1 (Project Setup):** โครงสร้างไฟล์ครบถ้วนตามแบบแผน, ใช้งาน Virtual Environment สะอาด
- [x] **หมวด 2 (Pytest & Coverage):** เขียน Test ครอบคลุมทั้งกรณีปกติ, ค่าขอบเขต (Boundary), และกรณีผิดพลาด (Error Handling) Coverage > 98%
- [x] **หมวด 3 (CI Workflow):** ไฟล์ `.github/workflows/ci.yml` รัน ruff และ pytest ทุกครั้งที่ push
- [x] **หมวด 4 (CD Deploy):** กำหนด Job deploy ส่งขึ้น GitHub Pages เมื่อ test ผ่าน และตั้งค่า Pages Source เป็น GitHub Actions
- [x] **หมวด 5 (Pull Request):** กำหนดเงื่อนไข `if: github.event_name != 'pull_request'` ข้าม deploy ใน PR พร้อมรองรับ Branch Protection
- [x] **หมวด 6 (Secrets & Variables):** ส่งผ่านค่า `SITE_TITLE` (Variable) และ `DEMO_API_KEY` (Secret) เข้าสู่ Environment ปลอดภัย
- [x] **หมวด 7 (Matrix Build):** ทดสอบคู่ขนานครบทั้ง Python 3.12, 3.13, 3.14 แบบ `fail-fast: false`
- [x] **หมวด 8 (Self-hosted runner):** ศึกษาข้อดี-ข้อเสีย และความปลอดภัยของระบบ Self-hosted runner
- [x] **หมวด 9 (แบบฝึกหัด & คำถามทบทวน):** ตอบคำถามทบทวน 8 ข้อ และพัฒนาแบบฝึกหัดข้อ 1-4 ครบถ้วนใน [ANSWERS.md](ANSWERS.md)
