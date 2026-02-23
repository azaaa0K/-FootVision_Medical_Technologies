# app.py - FLASK DIABETIC FOOT SCANNER
from flask import Flask, render_template, request, jsonify, flash
import os
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import numpy as np
import requests
import uuid

app = Flask(__name__)
app.secret_key = 'sindh-foot-scanner-2026'
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def medical_foot_analysis(image_path, symptoms="none", patient_name="Ahmed Khan", age="Unknown", gender="Unknown", phone="N/A"):
    """MEDICAL HSV ANALYSIS - Hospital Standard"""
    
    # Load and preprocess image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read the image file. Please ensure it is a valid JPG or PNG.")
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    
    # Clinical redness detection
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    
    red_pixels = np.sum(red_mask > 0)
    total_pixels = img.shape[0] * img.shape[1]
    
    # Calculate base ratio and apply a -10% calibration offset as requested
    raw_redness = (red_pixels / total_pixels) * 100
    redness_ratio = max(0.0, raw_redness - 10.0)
    
    # Clinical risk scoring
    base_risk = redness_ratio * 2
    symptom_boost = {"pus": 25, "swelling": 20, "pain": 15, "numbness": 10}.get(symptoms, 0)
    final_risk = min(100, base_risk + symptom_boost)
    
    # Medical diagnosis
    if final_risk >= 70:
        diagnosis = "🔴 ULCER EMERGENCY"
        urdu = "🚨 PAON KA GHAAW - ABHI HOSPITAL!"
        action = "🏥 CIVIL HOSPITAL PODIATRY NOW"
    elif final_risk >= 40:
        diagnosis = "🟡 HIGH RISK"
        urdu = "⚠️ JALDI DOCTOR Dikhayein"
        action = "👨‍⚕️ CLINIC 48 HOURS"
    else:
        diagnosis = "🟢 SAFE"
        urdu = "✅ NORMAL - Weekly check"
        action = "📅 SELF SCAN WEEKLY"
    
    return {
        'diagnosis': diagnosis,
        'risk_score': f"{final_risk:.0f}%",
        'redness': f"{redness_ratio:.1f}%",
        'urdu': urdu,
        'action': action,
        'patient': patient_name,
        'age': age,
        'gender': gender,
        'phone': phone
    }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded', 'success': False}), 400
    
    file = request.files['file']
    patient_name = request.form.get('name', '')
    age = request.form.get('age', '')
    gender = request.form.get('gender', '')
    phone = request.form.get('phone', '')
    symptoms = request.form.get('symptoms', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected', 'success': False}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Send to Colab API as requested (using stream directly)
            api_url = "https://percolative-glennis-gainfully.ngrok-free.dev/api/dfu"
            
            # Ensure the stream is reset before sending
            file.stream.seek(0)
            files = {'image': file.stream}
            data = {
                'name': patient_name,
                'symptoms': symptoms
            }
            
            response = requests.post(api_url, files=files, data=data, timeout=60)
            
            # Reset stream again and save file locally for the frontend preview
            file.stream.seek(0)
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            response.raise_for_status()
            result_data = response.json()
            
            # Intercept 'No foot visible' logic to map exact UI required dictionary
            if result_data.get('foot_detected') is False or "NO FOOT VISIBLE" in str(result_data.get('diagnosis', '')).upper() or "NO FOOT" in str(result_data.get('diagnosis', '')).upper():
                result_data = {
                    "diagnosis": "❓ NO FOOT VISIBLE",
                    "risk_score": "0%",
                    "findings": "No foot detected in uploaded photo. Please take a clear photo showing ONLY the foot.",
                    "urdu_alert": "🛑 پاؤں نظر نہیں آ رہا!",
                    "action": "دوبارہ پاؤں کی واضح تصویر لیں - صرف پاؤں دکھائیں",
                    "foot_detected": False,
                    "error_type": "no_foot"
                }

            # Ensure patient form fields are present in the returned result so the frontend
            # does not display "undefined" when fields are missing from the API.
            if not isinstance(result_data, dict):
                result_data = {}
            result_data.setdefault('patient', patient_name or '')
            result_data.setdefault('age', age or 'N/A')
            result_data.setdefault('gender', gender or 'N/A')
            result_data.setdefault('phone', phone or 'N/A')
            
            # The API returns the result at the top level, or sometimes nested if we mimic the old format
            # We return it nested under 'result' for the frontend compatibility, or just map it directly.
            
            return jsonify({
                'success': True,
                'image': f"/static/uploads/{filename}",
                'result': result_data
            })
        except requests.exceptions.Timeout:
            return jsonify({'error': 'API request timed out after 60 seconds', 'success': False}), 504
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'API connection error: {str(e)}', 'success': False}), 502
        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}', 'success': False}), 500
    
    return jsonify({'error': 'Invalid file type', 'success': False}), 400


if __name__ == "__main__":
    app.run()
