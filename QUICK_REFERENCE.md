# Quick Reference - Patient Monitoring System

## System Access
- **Frontend**: http://localhost:5174/
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Alert Types

### Traditional Alerts
| Type | Icon | Severity | Description |
|------|------|----------|-------------|
| FALL | ▼ | CRITICAL | Patient has fallen |
| SEIZURE | ※ | CRITICAL | Seizure activity detected |
| BED_EXIT | ▶ | HIGH | Patient left bed area |
| RAPID_MOVEMENT | ⚡ | MEDIUM | Fast movement detected |
| ABNORMAL_POSTURE | ◈ | MEDIUM | Unusual body position |
| ABNORMAL_BREATHING | ◐ | HIGH | Breathing rate abnormal |

### Predictive Health Alerts (NEW)
| Type | Icon | Severity | Description |
|------|------|----------|-------------|
| STROKE_RISK | 🧠 | HIGH/CRITICAL | Stroke indicators detected |
| CARDIAC_RISK | ❤️ | HIGH/CRITICAL | Cardiac event indicators |
| HEALTH_DETERIORATION | ⚕️ | HIGH/CRITICAL | Overall health declining |

## Dashboard Stats

### Traditional Monitoring
- Total Alerts
- Fall Incidents
- Seizure Alerts
- Bed Exits
- Rapid Movements
- Abnormal Posture
- Breathing Alerts

### Predictive Health (NEW)
- Stroke Risk
- Cardiac Risk
- Health Alerts

## How to Use

### 1. Upload Video
- Click "Choose File" or drag & drop video
- Click "Analyze Video"
- Wait for processing

### 2. View Results
- Dashboard shows alert counts
- Alert list shows detailed information
- Each alert includes:
  - Type and severity
  - Timestamp and frame number
  - Specific metrics (speed, confidence, risk score)
  - Recommendations (for health alerts)

### 3. Load Patient Details
- Click "Load Patient Details" in room card
- Fetches from Google Sheets
- Shows patient ID, name, disease, doctor, etc.

### 4. General Ward View
- Switch view mode to "General Ward"
- Compare before/after ward images
- Detect missing patients using AI

## Risk Score Interpretation

### Stroke Risk Score
- **70-100**: CRITICAL - Call stroke team immediately
- **40-69**: HIGH - Urgent assessment needed
- **20-39**: MEDIUM - Monitor closely
- **0-19**: LOW - Routine monitoring

### Cardiac Risk Score
- **70-100**: CRITICAL - Code blue, cardiac intervention
- **40-69**: HIGH - Urgent vitals, notify cardiologist
- **20-39**: MEDIUM - Monitor, check vitals
- **0-19**: LOW - Routine monitoring

### Health Score
- **70-100**: CRITICAL - Immediate intervention
- **50-69**: HIGH - Urgent assessment
- **30-49**: MEDIUM - Increased monitoring
- **0-29**: LOW - Routine care

## Stroke Indicators

### What System Detects:
1. **Facial Asymmetry**: One side of face drooping
2. **Arm Drift**: One arm weaker, drifting down
3. **Gait Abnormality**: Uneven walking pattern

### Clinical Significance:
These are the FAST (Face, Arms, Speech, Time) stroke indicators used in emergency medicine.

## Cardiac Indicators

### What System Detects:
1. **Chest Clutching**: Hand-to-chest gesture
2. **Breathing Distress**: Rapid (>25 bpm) or slow (<8 bpm) breathing
3. **Restlessness**: Excessive movement/agitation
4. **Color Changes**: Pale or bluish skin tone

### Clinical Significance:
Common early warning signs of cardiac events (heart attack, arrhythmia, heart failure).

## Technical Details

### Detection Thresholds
- Seizure: High variance (>0.006), erratic movement
- Rapid Movement: Speed >0.06, 3 consecutive frames
- Facial Asymmetry: >0.03 difference, sustained 10 frames
- Arm Drift: >0.15 difference, sustained 20 frames
- Breathing: <8 or >30 bpm triggers alert

### Frame Processing
- Every 3rd frame analyzed
- Multiple detection algorithms run in parallel
- Real-time WebSocket broadcasting

## Troubleshooting

### Backend Not Starting
```bash
cd patient/backend
python main.py
```

### Frontend Not Starting
```bash
cd patient/frontend
npm run dev
```

### No Alerts Detected
- Check video quality (clear view of patient)
- Ensure patient is visible in frame
- Verify MediaPipe models downloaded
- Check backend console for detection logs

### WebSocket Not Connecting
- Verify backend is running on port 8000
- Check CORS settings in main.py
- Refresh frontend page

## API Endpoints

### Video Processing
- `POST /api/upload-video` - Upload video file
- `POST /api/process-video/{filename}` - Process uploaded video

### Ward Analysis
- `POST /api/compare-ward-images` - Compare before/after images
- `POST /api/analyze-ward-presence` - Analyze patient presence

### Health Check
- `GET /api/health` - System health status
- `GET /` - API info

### WebSocket
- `WS /ws/alerts` - Real-time alert stream

## Configuration

### Environment Variables (.env)
```
GEMINI_API_KEY=your_api_key_here
```

### Google Sheets API
Update `GOOGLE_SHEETS_API` in App.jsx with your deployment URL.

## Support

For issues or questions:
1. Check backend console logs
2. Check browser console (F12)
3. Verify all dependencies installed
4. Ensure models downloaded successfully
