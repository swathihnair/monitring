# Predictive Health Monitoring Features

## Overview
Advanced AI-powered health analytics that predict critical conditions before they occur, enabling proactive medical intervention.

## Features Implemented

### 1. Stroke Detection 🧠
Real-time detection of stroke indicators through video analysis:

#### Indicators Monitored:
- **Facial Asymmetry**: Detects drooping or asymmetry in facial features (eyes, mouth)
- **Arm Drift**: Identifies weakness in one arm (arm drifting downward)
- **Gait Abnormalities**: Detects asymmetric or abnormal walking patterns

#### Risk Scoring:
- **CRITICAL (70-100)**: Immediate stroke team activation, prepare for CT scan
- **HIGH (40-69)**: Urgent patient assessment, notify doctor immediately
- **MEDIUM (20-39)**: Close monitoring, document observations
- **LOW (0-19)**: Continue routine monitoring

### 2. Cardiac Event Detection ❤️
Identifies early warning signs of cardiac distress:

#### Indicators Monitored:
- **Chest Clutching**: Detects hand-to-chest gestures
- **Breathing Distress**: Monitors for rapid (>25 bpm) or slow (<8 bpm) breathing
- **Excessive Restlessness**: Tracks unusual movement patterns
- **Skin Color Changes**: Detects pallor (pale) or cyanosis (bluish tint)

#### Risk Scoring:
- **CRITICAL (70-100)**: Emergency code blue, prepare for cardiac intervention
- **HIGH (40-69)**: Urgent vitals check, notify cardiologist
- **MEDIUM (20-39)**: Monitor closely, check vitals, document symptoms
- **LOW (0-19)**: Continue routine monitoring

### 3. Behavioral Analysis 📊
Long-term pattern tracking for deterioration prediction:

#### Metrics Tracked:
- **Activity Levels**: Daily movement patterns and trends
- **Sleep Quality**: Sleep duration and quality analysis
- **Confusion Signs**: Erratic head movements indicating disorientation
- **Social Interaction**: Isolation detection

### 4. Overall Health Score ⚕️
Comprehensive health risk calculation combining all indicators:

#### Components:
- Stroke risk (35% weight)
- Cardiac risk (35% weight)
- Activity decline (15% weight)
- Sleep quality (15% weight)

#### Risk Levels:
- **CRITICAL (70-100)**: Immediate medical intervention required
- **HIGH (50-69)**: Urgent assessment needed
- **MEDIUM (30-49)**: Increased monitoring recommended
- **LOW (0-29)**: Continue routine care

## Technical Implementation

### Backend (Python)
- **MediaPipe Pose Landmarker**: Body pose detection and tracking
- **MediaPipe Face Landmarker**: Facial feature detection for asymmetry analysis
- **health_analytics.py**: Core detection algorithms
  - `StrokeDetector`: Facial asymmetry, arm drift, gait analysis
  - `CardiacIndicatorDetector`: Chest clutching, breathing, restlessness, color changes
  - `BehavioralAnalyzer`: Activity tracking, sleep patterns, confusion detection
  - `HealthRiskCalculator`: Overall health scoring and prediction

### Frontend (React)
- Real-time health risk display
- Predictive alert cards with risk scores
- Detailed recommendations for medical staff
- Visual indicators for critical conditions

## Alert Types

### New Alert Types Added:
1. **STROKE_RISK**: Stroke indicators detected
2. **CARDIAC_RISK**: Cardiac event indicators detected
3. **HEALTH_DETERIORATION**: Overall health declining

### Alert Information Includes:
- Risk level (CRITICAL, HIGH, MEDIUM, LOW)
- Risk score (0-100)
- Specific indicators detected
- Recommended actions for medical staff
- Timestamp and frame number

## Usage

### Viewing Health Analytics:
1. Upload patient video through the interface
2. System automatically analyzes for all health indicators
3. Health risk cards display on dashboard:
   - Stroke Risk count
   - Cardiac Risk count
   - Health Alerts count
4. Detailed alerts show specific indicators and recommendations

### Alert Response:
- **CRITICAL alerts**: Immediate medical intervention
- **HIGH alerts**: Urgent assessment within minutes
- **MEDIUM alerts**: Increased monitoring, document observations
- **LOW alerts**: Continue routine care

## Benefits

### Proactive Care:
- Detect conditions before they become critical
- Enable early intervention
- Reduce emergency response times

### Comprehensive Monitoring:
- Multiple health indicators tracked simultaneously
- Holistic health assessment
- Trend analysis over time

### Clinical Decision Support:
- Clear risk scores and recommendations
- Evidence-based indicators
- Actionable insights for medical staff

## Future Enhancements

### Planned Features:
- Historical trend analysis and visualization
- Predictive timeline (when deterioration likely to occur)
- Integration with vital signs monitoring
- Machine learning model training on patient-specific patterns
- Multi-patient comparison and risk ranking
- Automated notification to specific medical staff based on risk level

## Technical Requirements

### Dependencies:
- MediaPipe 0.10.33 (pose and face detection)
- OpenCV (video processing)
- NumPy (numerical computations)
- FastAPI (backend API)
- React (frontend UI)

### Models Used:
- `pose_landmarker.task`: Body pose detection
- `face_landmarker.task`: Facial landmark detection

## Performance

### Processing Speed:
- Analyzes every 3rd frame for optimal balance
- Real-time detection with minimal latency
- Efficient memory usage with rolling buffers

### Accuracy:
- Facial asymmetry: High precision with 30-frame history
- Arm drift: Sustained detection over 20 frames
- Gait analysis: 30-frame pattern recognition
- Breathing rate: 60-frame analysis (2 seconds)

## Medical Disclaimer

This system is designed to assist medical professionals and should not replace clinical judgment. All alerts should be verified by qualified healthcare providers. The system provides indicators and risk scores to support decision-making, not to make autonomous medical decisions.
