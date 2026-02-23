// Sindh Foot Scanner - Premium UI Logic
let currentImage = null;

// SCREEN NAVIGATION
function navigateTo(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    // Show target screen
    const target = document.getElementById(screenId);
    if (target) {
        target.classList.add('active');
        window.scrollTo(0, 0);
    }
}

// IMAGE UPLOAD & PREVIEW
const fileInput = document.getElementById('imageInput');
const uploadArea = document.getElementById('uploadArea');

fileInput.addEventListener('change', function (e) {
    handleFile(e.target.files[0]);
});

if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.border = '2px dashed #007bff';
        uploadArea.style.opacity = '0.7';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.border = '';
        uploadArea.style.opacity = '1';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.border = '';
        uploadArea.style.opacity = '1';
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFile(e.dataTransfer.files[0]);
        }
    });
}

function handleFile(file) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            currentImage = event.target.result;
            const preview = document.getElementById('preview-img');
            const placeholder = document.getElementById('upload-placeholder');
            const analyzeBtn = document.getElementById('analyzeBtn');

            preview.src = currentImage;
            preview.style.display = 'block';
            placeholder.style.display = 'none';
            analyzeBtn.style.display = 'flex';
        };
        reader.readAsDataURL(file);
    }
}


// START ANALYSIS FLOW
async function startAnalysis() {
    navigateTo('screen-analyzing');

    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    const name = document.getElementById('patientName').value || 'Ahmed Khan';
    const age = document.getElementById('patientAge').value;
    const gender = document.getElementById('patientGender').value;
    const phone = document.getElementById('patientPhone').value;

    formData.append('file', fileInput.files[0]);
    formData.append('name', name);
    formData.append('age', age);
    formData.append('gender', gender);
    formData.append('phone', phone);

    try {
        // Simulate a small delay for "High-End AI" feel
        await new Promise(resolve => setTimeout(resolve, 2000));

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        let result;
        try {
            result = await response.json();
        } catch (e) {
            throw new Error('Server returned an invalid response (not JSON). Please check if the server is running on port 5000.');
        }

        if (result.success) {
            updateResultScreen(result.result);
            // Also update the image with the one from the server if needed
            if (result.image) document.getElementById('res-img').src = result.image;
            navigateTo('screen-result');
        } else {
            alert('Analysis Error: ' + (result.error || 'Unknown error occurred'));
            navigateTo('screen-upload');
        }
    } catch (error) {
        console.error('Fetch Error:', error);
        alert('Server Connection Error: ' + error.message);
        navigateTo('screen-upload');
    }
}

function safeSetText(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
}

function safeSetHTML(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
}

function updateResultScreen(data) {
    // Set Timestamp
    const now = new Date();
    const options = { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' };
    const timeStr = now.toLocaleString('en-US', options).replace(',', ' •');
    safeSetText('res-timestamp', timeStr);

    // Basic Details (use fallbacks to avoid showing 'undefined')
    safeSetText('res-patient-name', data.patient || 'N/A');
    safeSetText('res-patient-age', data.age || 'N/A');
    safeSetText('res-patient-gender', data.gender || 'N/A');

    // Generate a pseudo-random ID for clinical look
    const randomHex = Math.floor(Math.random() * 16777215).toString(16).toUpperCase().padStart(6, '0');
    safeSetText('res-patient-id', `${randomHex}-FFA`);

    // Image
    const resImg = document.getElementById('res-img');
    if (resImg) resImg.src = currentImage;

    // Metrics calculations
    safeSetText('res-redness', data.findings || 'N/A');

    // Update labels to match new data without rebuilding HTML
    const rednessEl = document.getElementById('res-redness');
    if (rednessEl && rednessEl.nextElementSibling) {
        rednessEl.nextElementSibling.innerText = "Findings";
        rednessEl.style.fontSize = "0.9rem"; // Adjust for potentially long text
    }

    const swellingEl = document.getElementById('res-swelling');
    if (swellingEl) {
        swellingEl.innerHTML = data.diagnosis || 'N/A';
        swellingEl.style.fontSize = "0.9rem";
        if (swellingEl.nextElementSibling) swellingEl.nextElementSibling.innerText = "Diagnosis";
    }

    const woundEl = document.getElementById('res-wound');
    if (woundEl) {
        woundEl.innerHTML = 'N/A';
        if (woundEl.nextElementSibling) woundEl.nextElementSibling.innerText = "Wound Area";
    }

    const riskInt = parseInt(data.risk_score) || 0;

    // Risk Dashboard
    safeSetHTML('res-bold-score', `${riskInt}<span>/100</span>`);

    const needle = document.getElementById('res-risk-needle');
    if (needle) needle.style.left = `${riskInt}%`;
    const fill = document.getElementById('res-risk-fill');
    if (fill) fill.style.width = `${riskInt}%`;

    safeSetText('res-action-short', data.action || 'Unknown');
    safeSetText('res-urdu', data.urdu_alert || data.urdu || '');

    // Status text & colors
    const statusText = document.getElementById('res-status-text');
    if (statusText) {
        statusText.innerText = data.diagnosis || "Low Risk / Normal";
        if (riskInt > 70) {
            statusText.style.color = "#ef4444"; // Tailwind accent-red
        } else if (riskInt > 40) {
            statusText.style.color = "#FBBF24"; // Tailwind accent-yellow
        } else {
            statusText.style.color = "#10B981"; // Tailwind accent-green
        }
    }
}

function retakeScan() {
    // Reset upload state
    document.getElementById('imageInput').value = '';
    document.getElementById('preview-img').style.display = 'none';
    document.getElementById('upload-placeholder').style.display = 'block';
    document.getElementById('analyzeBtn').style.display = 'none';

    // Reset result state
    const resImg = document.getElementById('res-img');
    if (resImg) resImg.src = '';

    const needle = document.getElementById('res-risk-needle');
    if (needle) needle.style.left = '0%';
    const fill = document.getElementById('res-risk-fill');
    if (fill) fill.style.width = '0%';

    currentImage = null;
    navigateTo('screen-upload');
}

// Initial state check
window.onload = () => {
    navigateTo('screen-home');
};

