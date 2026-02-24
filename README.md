# 📁 SINDH DIABETIC FOOT SCANNER (Hybrid AI Edition)
================================================

**🏥 Medical AI Analysis Tool for Foot Ulcer Detection**  
_A MedGemma Initiative for Sindh Healthcare 2026_

---

## 📂 Project Structure
```text
foot_scanner/
├── app.py                    # Flask backend + HSV analysis
├── templates/
│   └── index.html            # Main UI
├── static/
│   ├── css/style.css         # Dark premium medical theme
│   ├── js/script.js          # Image logic & UI behavior
│   └── uploads/              # Temporary image storage
└── README.md                 # This file!
```

---

## 🚀 The "Double-Start" Setup (Important!)
Because the YOLOv8 model requires a GPU, we run the **AI Engine in Colab** and the **Interface locally**.

### Step 1: Fire up the AI Brain (Google Colab)
1. Open your Colab Notebook and run all cells.
2. At the very bottom, look for the Ngrok Public URL (e.g., `https://xxxx-xxxx.ngrok-free.app/api/dfu`).
3. Copy this URL.

### Step 2: Run the Local Web App (Your PC)
1. Open `app.py` in VS Code.
2. Find the variable where you paste the URL (look for `requests.post`).
3. Open your terminal and run:
   ```bash
   python app.py
   ```
4. Go to: [http://localhost:5000](http://localhost:5000)

---

## 🔧 Technical Workflow (The "Golabi" Logic)
- **Detection**: We use YOLOv8 to ensure a foot is actually present. If not, we stop the scan.
- **Analysis**: We use HSV Color Analysis to detect "Redness" levels.
- **Scoring**:
  - `Red > Green + 30`: High probability of infection/ulcer.
  - `Red > 120`: Warning for swelling/inflammation.
- **Localization**: The system converts medical data into Urdu Nastaliq alerts for local patients.

---

## 📊 Risk Scoring System
| Score | Status | Urdu Alert | Action |
|-------|--------|-----------|--------|
| 0-39% | 🟢 SAFE | سارا نارمل ہے | Weekly self-scan |
| 40-69% | 🟡 HIGH RISK | جلدی ڈاکٹر کو دکھائیں | Clinic in 48 hours |
| 70%+ | 🔴 EMERGENCY | خطرناک زخم ہے | Hospital now |

---

## 🎨 Key Features
- **Bilingual Interface**: Supports English and Urdu (Noto Nastaliq font).
- **Live Risk Gauge**: A visual needle that moves based on the AI's confidence.
- **Secure Privacy**: Images are processed and given UUID names to protect patient identity.
- **Fast Response**: Total analysis time is usually under 2 seconds.

---

## 👥 Developed By (Team MedGemma)
- **Idrees Abdullah** – AI/ML & Detection Logic
- **Zubaib Baloch** – Backend Architecture & API Tunneling
- **Marwan Saleem** – UI/UX & Localization Design