# Check Sleuth AI - CSV Analysis with Gemini

An intelligent web application that uses Gemini AI to analyze CSV files, identify data quality issues, detect anomalies, and uncover potential circular bias and data leakage in machine learning datasets.

## 🏗️ Architecture

This application uses a **secure client-server architecture**:

- **Frontend (React + Vite)**: Handles CSV upload and displays analysis results
- **Backend (Flask API)**: Securely calls Gemini API with server-side API key management
- **Vite Proxy**: Routes `/api/*` requests from frontend to backend during development

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🚀 Quick Start

### 1. Install Frontend Dependencies

```bash
npm install
```

### 2. Set Up Backend

```bash
# Navigate to backend directory
cd ../backend

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

**Backend**: Set your Gemini API key as an environment variable

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"

# Windows (CMD)
set GEMINI_API_KEY=your-api-key-here

# Linux/Mac
export GEMINI_API_KEY=your-api-key-here
```

### 4. Start the Backend Server

```bash
# In the backend directory
python app.py
```

The backend will start on `http://localhost:5000`

### 5. Start the Frontend Development Server

```bash
# In the check-sleuth-ai directory
npm run dev
```

The frontend will start on `http://localhost:3000`

## 🔒 Security Notes

- ✅ **Secure**: API key is stored server-side only
- ✅ **No Exposure**: Frontend never sees the API key
- ✅ **CORS Enabled**: Backend configured for frontend communication
- ✅ **Fallback Mode**: Works with mock data if API key not configured

## 📊 Google Analytics (Optional)

Google Analytics code is pre-configured but commented out in `index.html` (lines 37-46).

**To enable:**
1. Get your GA4 Measurement ID from https://analytics.google.com/
2. Uncomment lines 37-46 in `index.html`
3. Replace `G-XXXXXXXXXX` with your actual Measurement ID

**For advanced setup** (environment variables, custom events, GDPR compliance):
- See detailed guide: `GOOGLE_ANALYTICS_SETUP.md`

## 📦 Building for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

## 🌐 Deployment Options

### Option 1: Netlify (Frontend) + Cloud Function (Backend)

1. Deploy frontend to Netlify
2. Deploy backend as a Netlify Function or Vercel Serverless Function
3. Update frontend proxy to point to production backend URL

### Option 2: Vercel Full-Stack

1. Deploy entire application to Vercel
2. Backend becomes a serverless API route
3. Frontend and backend deployed together

### Option 3: Traditional Hosting

1. Frontend: Build and deploy static files to any CDN
2. Backend: Deploy Flask app to cloud VM or container service
3. Configure CORS to allow frontend domain

## 📖 API Endpoints

**Backend API** (`http://localhost:5000`)

- `GET /health` - Health check
- `GET /api/info` - API documentation
- `POST /api/analyze-csv` - Analyze CSV with Gemini AI (requires raw CSV as request body)
- `POST /api/detect` - Circular bias detection using Sleuth algorithms

## 🧪 Testing

Upload any CSV file through the web interface. The AI will analyze:

- **Data Quality**: Missing values, formatting issues, duplicates
- **Anomalies & Outliers**: Unusual patterns in the data
- **Circular Bias**: Features that may leak information from the target variable
- **Data Leakage**: Predictor variables derived from outcomes

## 📝 License

CC BY 4.0

## 🔗 Links

- Original App: https://ai.studio/apps/drive/15HRAfp9cxQq8ppkL4d4BK5frSGvi7VNo
- GitHub: https://github.com/hongping-zh/circular-bias-detection
