📁 SINDH DIABETIC FOOT SCANNER
================================

🏥 Medical AI Analysis Tool for Foot Ulcer Detection

## 📂 Project Structure
```
foot_scanner/
├── app.py                    # Flask backend + HSV analysis
├── templates/
│   └── index.html           # Main UI (Bootstrap 5)
├── static/
│   ├── css/style.css        # Dark medical theme
│   ├── js/script.js         # Image preview + AJAX
│   └── uploads/             # Temporary image storage
└── README.md                # This file
```

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
cd foot_scanner
pip install flask opencv-python pillow numpy werkzeug
```

### 2. Run Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to: **http://localhost:5000**

## 🎨 Features

✅ **Medical Analysis**
- HSV color-based redness detection
- Symptom-based risk scoring
- Risk levels: SAFE, HIGH RISK, ULCER EMERGENCY

✅ **UI/UX**
- Dark medical theme (#222831, #393E46, #948979, #DFD0B8)
- Real-time image preview
- AJAX prediction (no page reload)
- Responsive Bootstrap design

✅ **Multi-lingual**
- English diagnosis with risk scores
- Urdu emergency alerts
- Patient name tracking

✅ **Patient Information**
- Patient name input
- Symptom selection (pain, swelling, pus, numbness)
- Professional medical report layout

## 📊 Risk Scoring System

| Score | Status | Urdu Alert | Action |
|-------|--------|-----------|--------|
| 0-39% | 🟢 SAFE | ✅ NORMAL | Weekly self-scan |
| 40-69% | 🟡 HIGH RISK | ⚠️ JALDI DOCTOR | Clinic in 48 hours |
| 70%+ | 🔴 EMERGENCY | 🚨 PAON KA GHAAW | Hospital now |

## 🔧 Technical Stack

- **Backend:** Flask (Python)
- **Image Processing:** OpenCV, PIL, NumPy
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Client Logic:** Vanilla JavaScript (AJAX)

## 📝 API Endpoints

**GET /?**
- Serves main UI

**POST /predict**
- Input: Image file + patient name + symptoms
- Output: JSON with diagnosis, risk score, redness percentage

## 🛡️ File Upload Limits
- Max file size: 16 MB
- Allowed formats: PNG, JPG, JPEG, GIF
- Files auto-deleted after analysis

## 🔐 Security
- Werkzeug secure filename handling
- UUID-based file naming
- Temporary file cleanup

## ⚠️ Medical Disclaimer
This tool provides AI-assisted analysis for educational purposes.
**Always consult qualified healthcare professionals for medical decisions.**

---
**Created for Sindh Healthcare Initiative 2026**
