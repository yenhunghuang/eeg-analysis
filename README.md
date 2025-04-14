# 🧠 EEG Spectrum Analysis Microservice

This is a **Python-based FastAPI microservice** for real-time EEG signal analysis, designed to provide alpha/theta band power metrics and ratio used in neurofeedback applications.

---

## 🔧 Features

-   Accepts time-series EEG data via HTTP POST
-   Performs **Welch method** based power spectrum analysis
-   Computes **absolute power**, **relative power**, and **alpha/theta ratio**
-   Returns structured JSON results

---

## 📁 Project Structure

```
eeg-analysis/
├── app.py                # FastAPI main app entry
├── fft_analyze.py        # EEG analysis logic (Welch FFT)
├── requirements.txt      # Python dependencies
├── render.yaml           # Render deployment config
```

---

## ▶️ Local Development

### 1. Set up virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run FastAPI locally

```bash
uvicorn app:app --reload --port 8000
```

Then open: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI

---

## 📦 API Endpoints

### `POST /analyze`

Perform EEG analysis on a segment of signal.

**Request JSON**

```json
{
  "data": [1.1, 2.3, 3.0, ...],
  "fs": 250
}
```

**Response JSON**

```json
{
    "absolute_power": {
        "theta": 0.12,
        "alpha": 0.35
    },
    "relative_power": {
        "theta": 0.15,
        "alpha": 0.42
    },
    "alpha_theta_ratio": 2.91,
    "data_info": {
        "data_length": 128,
        "analysis_method": "welch"
    }
}
```

### `GET /health`

Returns status of the service.

```json
{ "status": "healthy" }
```

---

## 🚀 Deployment on Render

### `render.yaml`

```yaml
services:
    - type: web
      name: eeg-analysis
      env: python
      buildCommand: pip install -r requirements.txt
      startCommand: uvicorn app:app --host 0.0.0.0 --port 8000
      envVars:
          - key: PORT
            value: 8000
```

---

## 🔗 Used by

-   [eeg-api](https://github.com/your-org/eeg-api) (Node.js API Gateway)

---

## 📜 License

MIT License
