"""
Advanced Health Analytics Module
Predictive detection for stroke, cardiac events, and patient deterioration
"""

import numpy as np
import cv2
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Tuple, Optional

class StrokeDetector:
    """Detect stroke indicators from video analysis"""
    
    def __init__(self):
        self.facial_history = deque(maxlen=30)
        self.arm_position_history = deque(maxlen=60)
        self.gait_history = deque(maxlen=90)
        
    def detect_facial_asymmetry(self, face_landmarks) -> Tuple[bool, float, str]:
        """Detect facial drooping/asymmetry (stroke indicator)"""
        if not face_landmarks or len(face_landmarks) < 468:
            return False, 0.0, "No face detected"
        
        try:
            # Key facial points for asymmetry
            left_eye_outer = face_landmarks[33]
            right_eye_outer = face_landmarks[263]
            left_mouth = face_landmarks[61]
            right_mouth = face_landmarks[291]
            nose_tip = face_landmarks[1]
            
            # Calculate eye level difference
            eye_asymmetry = abs(left_eye_outer.y - right_eye_outer.y)
            
            # Calculate mouth asymmetry
            mouth_asymmetry = abs(left_mouth.y - right_mouth.y)
            
            # Calculate overall facial asymmetry score
            asymmetry_score = (eye_asymmetry + mouth_asymmetry) / 2
            
            # Store history
            self.facial_history.append(asymmetry_score)
            
            # Need consistent asymmetry (not just one frame)
            if len(self.facial_history) >= 10:
                avg_asymmetry = np.mean(list(self.facial_history)[-10:])
                
                is_asymmetric = avg_asymmetry > 0.03
                
                if is_asymmetric:
                    side = "left" if left_mouth.y > right_mouth.y else "right"
                    return True, float(avg_asymmetry), f"Facial drooping detected on {side} side"
            
            return False, float(asymmetry_score), "Face symmetric"
            
        except Exception as e:
            return False, 0.0, f"Error: {str(e)}"
    
    def detect_arm_drift(self, pose_landmarks) -> Tuple[bool, float, str]:
        """Detect arm weakness (one arm drifting down)"""
        if not pose_landmarks:
            return False, 0.0, "No pose detected"
        
        try:
            # Get arm positions
            left_shoulder = pose_landmarks[11]
            right_shoulder = pose_landmarks[12]
            left_elbow = pose_landmarks[13]
            right_elbow = pose_landmarks[14]
            left_wrist = pose_landmarks[15]
            right_wrist = pose_landmarks[16]
            
            # Calculate arm heights relative to shoulders
            left_arm_height = left_shoulder.y - left_wrist.y
            right_arm_height = right_shoulder.y - right_wrist.y
            
            # Arm drift = significant difference in arm heights
            arm_difference = abs(left_arm_height - right_arm_height)
            
            # Store history
            self.arm_position_history.append({
                'left': left_arm_height,
                'right': right_arm_height,
                'diff': arm_difference
            })
            
            # Check for sustained arm drift - REDUCED from 20 to 10 frames
            if len(self.arm_position_history) >= 10:
                recent_diffs = [h['diff'] for h in list(self.arm_position_history)[-10:]]
                avg_diff = np.mean(recent_diffs)
                
                # LOWERED threshold from 0.15 to 0.12 for earlier detection
                is_drift = avg_diff > 0.12
                
                if is_drift:
                    weak_side = "left" if left_arm_height < right_arm_height else "right"
                    return True, float(avg_diff), f"Arm weakness detected on {weak_side} side"
            
            return False, float(arm_difference), "Arms balanced"
            
        except Exception as e:
            return False, 0.0, f"Error: {str(e)}"
    
    def detect_gait_abnormalities(self, pose_landmarks) -> Tuple[bool, float, str]:
        """Detect abnormal walking patterns"""
        if not pose_landmarks:
            return False, 0.0, "No pose detected"
        
        try:
            # Get leg positions
            left_hip = pose_landmarks[23]
            right_hip = pose_landmarks[24]
            left_knee = pose_landmarks[25]
            right_knee = pose_landmarks[26]
            left_ankle = pose_landmarks[27]
            right_ankle = pose_landmarks[28]
            
            # Calculate leg movement
            left_leg_movement = abs(left_ankle.y - left_hip.y)
            right_leg_movement = abs(right_ankle.y - right_hip.y)
            
            # Detect asymmetric gait
            gait_asymmetry = abs(left_leg_movement - right_leg_movement)
            
            # Store gait history
            self.gait_history.append({
                'left': left_leg_movement,
                'right': right_leg_movement,
                'asymmetry': gait_asymmetry
            })
            
            # Analyze gait pattern
            if len(self.gait_history) >= 30:
                recent_asymmetry = [h['asymmetry'] for h in list(self.gait_history)[-30:]]
                avg_asymmetry = np.mean(recent_asymmetry)
                
                is_abnormal = avg_asymmetry > 0.1
                
                if is_abnormal:
                    return True, float(avg_asymmetry), "Abnormal gait detected - possible weakness"
            
            return False, float(gait_asymmetry), "Gait normal"
            
        except Exception as e:
            return False, 0.0, f"Error: {str(e)}"
    
    def calculate_stroke_risk_score(self, facial_asymmetry: bool, arm_drift: bool, 
                                   gait_abnormal: bool, confusion: bool = False) -> Dict:
        """Calculate overall stroke risk score"""
        score = 0
        indicators = []
        
        if facial_asymmetry:
            score += 40
            indicators.append("Facial asymmetry")
        
        if arm_drift:
            score += 45  # Increased from 35 - arm drift is highly significant
            indicators.append("Arm weakness")
        
        if gait_abnormal:
            score += 25  # Increased from 20
            indicators.append("Gait abnormality")
        
        if confusion:
            score += 15  # Increased from 10
            indicators.append("Confusion/disorientation")
        
        # Determine risk level - LOWERED thresholds for earlier detection
        if score >= 60:  # Changed from 70
            risk_level = "CRITICAL"
            recommendation = "IMMEDIATE: Call stroke team, prepare for CT scan"
        elif score >= 35:  # Changed from 40 - single strong indicator = HIGH
            risk_level = "HIGH"
            recommendation = "URGENT: Assess patient immediately, notify doctor"
        elif score >= 20:
            risk_level = "MEDIUM"
            recommendation = "Monitor closely, document observations"
        else:
            risk_level = "LOW"
            recommendation = "Continue routine monitoring"
        
        return {
            'stroke_risk_score': score,
            'risk_level': risk_level,
            'indicators': indicators,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }


class CardiacIndicatorDetector:
    """Detect cardiac event indicators from video"""
    
    def __init__(self):
        self.breathing_history = deque(maxlen=120)
        self.restlessness_history = deque(maxlen=300)
        self.color_history = deque(maxlen=60)
        self.chest_clutching_history = deque(maxlen=20)  # Track clutching over time
        
    def detect_chest_clutching(self, pose_landmarks) -> Tuple[bool, float]:
        """Detect hand-to-chest gesture - STRICT to avoid false positives, requires sustained detection"""
        if not pose_landmarks:
            return False, 0.0
        
        try:
            # Get hand and chest positions
            left_wrist = pose_landmarks[15]
            right_wrist = pose_landmarks[16]
            left_elbow = pose_landmarks[13]
            right_elbow = pose_landmarks[14]
            left_shoulder = pose_landmarks[11]
            right_shoulder = pose_landmarks[12]
            
            # Calculate chest center
            chest_x = (left_shoulder.x + right_shoulder.x) / 2
            chest_y = (left_shoulder.y + right_shoulder.y) / 2
            
            # Check if either hand is near chest
            left_hand_to_chest = np.sqrt((left_wrist.x - chest_x)**2 + (left_wrist.y - chest_y)**2)
            right_hand_to_chest = np.sqrt((right_wrist.x - chest_x)**2 + (right_wrist.y - chest_y)**2)
            
            min_distance = min(left_hand_to_chest, right_hand_to_chest)
            
            # STRICTER threshold - must be very close to chest
            # Also check that elbow is bent (not just arm hanging down)
            left_elbow_bent = abs(left_elbow.y - left_shoulder.y) < 0.3
            right_elbow_bent = abs(right_elbow.y - right_shoulder.y) < 0.3
            
            # Only detect if hand is VERY close AND elbow is bent (deliberate gesture)
            is_clutching_now = min_distance < 0.10 and (left_elbow_bent or right_elbow_bent)
            
            # Store history
            self.chest_clutching_history.append(is_clutching_now)
            
            # Require sustained clutching over 15 frames (0.5 seconds) to avoid false positives
            if len(self.chest_clutching_history) >= 15:
                clutching_count = sum(list(self.chest_clutching_history)[-15:])
                # Need at least 12 out of 15 frames showing clutching
                is_clutching = clutching_count >= 12
                return is_clutching, float(min_distance)
            
            return False, float(min_distance)
            
        except Exception as e:
            return False, 0.0
    
    def detect_breathing_distress(self, pose_landmarks) -> Tuple[bool, float, str]:
        """Detect rapid or labored breathing"""
        if not pose_landmarks:
            return False, 0.0, "No pose detected"
        
        try:
            # Track shoulder movement (breathing indicator)
            left_shoulder = pose_landmarks[11]
            right_shoulder = pose_landmarks[12]
            
            shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            
            self.breathing_history.append(shoulder_y)
            
            if len(self.breathing_history) >= 60:
                # Calculate breathing rate
                breathing_array = np.array(list(self.breathing_history))
                
                # Count peaks (breaths)
                peaks = 0
                for i in range(1, len(breathing_array) - 1):
                    if breathing_array[i] < breathing_array[i-1] and breathing_array[i] < breathing_array[i+1]:
                        if abs(breathing_array[i] - np.mean(breathing_array)) > 0.005:
                            peaks += 1
                
                # Convert to breaths per minute
                breaths_per_minute = (peaks / len(breathing_array)) * 30 * 60
                
                # Detect distress
                is_distress = breaths_per_minute > 25 or breaths_per_minute < 8
                
                if breaths_per_minute > 25:
                    status = "Rapid breathing (Tachypnea) - possible distress"
                elif breaths_per_minute < 8:
                    status = "Slow breathing (Bradypnea) - concerning"
                else:
                    status = "Normal breathing"
                
                return is_distress, float(breaths_per_minute), status
            
            return False, 0.0, "Calculating..."
            
        except Exception as e:
            return False, 0.0, f"Error: {str(e)}"
    
    def detect_restlessness(self, pose_landmarks) -> Tuple[bool, float]:
        """Detect excessive restlessness (cardiac distress indicator)"""
        if not pose_landmarks:
            return False, 0.0
        
        try:
            # Calculate center of mass
            key_points = [pose_landmarks[i] for i in [0, 11, 12, 23, 24]]
            center_x = np.mean([p.x for p in key_points])
            center_y = np.mean([p.y for p in key_points])
            
            self.restlessness_history.append((center_x, center_y))
            
            if len(self.restlessness_history) >= 60:
                # Calculate movement variance (restlessness indicator)
                positions = np.array(list(self.restlessness_history)[-60:])
                variance = np.var(positions, axis=0).sum()
                
                is_restless = variance > 0.01
                
                return is_restless, float(variance)
            
            return False, 0.0
            
        except Exception as e:
            return False, 0.0
    
    def detect_color_changes(self, face_roi) -> Tuple[bool, str, Dict]:
        """Detect skin color changes (pallor/cyanosis)"""
        if face_roi is None or face_roi.size == 0:
            return False, "No face detected", {}
        
        try:
            # Calculate average color
            avg_color = cv2.mean(face_roi)[:3]  # BGR
            b, g, r = avg_color
            
            self.color_history.append({'r': r, 'g': g, 'b': b})
            
            if len(self.color_history) >= 30:
                # Calculate baseline
                recent_colors = list(self.color_history)[-30:]
                baseline_r = np.mean([c['r'] for c in recent_colors[:15]])
                baseline_g = np.mean([c['g'] for c in recent_colors[:15]])
                baseline_b = np.mean([c['b'] for c in recent_colors[:15]])
                
                current_r = np.mean([c['r'] for c in recent_colors[-5:]])
                current_g = np.mean([c['g'] for c in recent_colors[-5:]])
                current_b = np.mean([c['b'] for c in recent_colors[-5:]])
                
                # Detect pallor (pale - reduced red)
                pallor_detected = current_r < baseline_r * 0.85
                
                # Detect cyanosis (bluish - increased blue, reduced red)
                cyanosis_detected = (current_b > baseline_b * 1.15) and (current_r < baseline_r * 0.9)
                
                if cyanosis_detected:
                    return True, "Cyanosis detected (bluish tint) - LOW OXYGEN", {
                        'r': current_r, 'g': current_g, 'b': current_b
                    }
                elif pallor_detected:
                    return True, "Pallor detected (pale skin) - possible shock", {
                        'r': current_r, 'g': current_g, 'b': current_b
                    }
            
            return False, "Normal skin color", {'r': r, 'g': g, 'b': b}
            
        except Exception as e:
            return False, f"Error: {str(e)}", {}
    
    def calculate_cardiac_risk_score(self, chest_clutching: bool, breathing_distress: bool,
                                    restlessness: bool, color_change: bool) -> Dict:
        """Calculate cardiac event risk score"""
        score = 0
        indicators = []
        
        if chest_clutching:
            score += 40
            indicators.append("Chest clutching gesture")
        
        if breathing_distress:
            score += 30
            indicators.append("Breathing distress")
        
        if restlessness:
            score += 15
            indicators.append("Excessive restlessness")
        
        if color_change:
            score += 15
            indicators.append("Skin color changes")
        
        # Determine risk level
        if score >= 70:
            risk_level = "CRITICAL"
            recommendation = "EMERGENCY: Call code blue, prepare for cardiac intervention"
        elif score >= 40:
            risk_level = "HIGH"
            recommendation = "URGENT: Assess vitals, notify cardiologist immediately"
        elif score >= 20:
            risk_level = "MEDIUM"
            recommendation = "Monitor closely, check vitals, document symptoms"
        else:
            risk_level = "LOW"
            recommendation = "Continue routine monitoring"
        
        return {
            'cardiac_risk_score': score,
            'risk_level': risk_level,
            'indicators': indicators,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }


class BehavioralAnalyzer:
    """Analyze patient behavior patterns for deterioration prediction"""
    
    def __init__(self):
        self.activity_log = []  # Store activity over days
        self.sleep_log = []
        self.movement_patterns = deque(maxlen=1000)
        self.confusion_indicators = deque(maxlen=200)
        
    def track_activity_level(self, movement_detected: bool, timestamp: datetime) -> Dict:
        """Track daily activity levels"""
        self.activity_log.append({
            'movement': movement_detected,
            'timestamp': timestamp
        })
        
        # Keep last 7 days
        cutoff = datetime.now() - timedelta(days=7)
        self.activity_log = [a for a in self.activity_log if a['timestamp'] > cutoff]
        
        # Calculate activity score for today
        today_start = datetime.now().replace(hour=0, minute=0, second=0)
        today_activities = [a for a in self.activity_log if a['timestamp'] > today_start]
        
        activity_count = sum(1 for a in today_activities if a['movement'])
        
        # Compare to previous days
        if len(self.activity_log) > 0:
            yesterday_start = today_start - timedelta(days=1)
            yesterday_activities = [a for a in self.activity_log 
                                   if yesterday_start < a['timestamp'] < today_start]
            yesterday_count = sum(1 for a in yesterday_activities if a['movement'])
            
            if yesterday_count > 0:
                decline_percentage = ((yesterday_count - activity_count) / yesterday_count) * 100
                
                is_declining = decline_percentage > 30
                
                return {
                    'activity_today': activity_count,
                    'activity_yesterday': yesterday_count,
                    'decline_percentage': decline_percentage,
                    'is_declining': is_declining,
                    'status': 'Declining' if is_declining else 'Stable'
                }
        
        return {
            'activity_today': activity_count,
            'status': 'Monitoring'
        }
    
    def analyze_sleep_patterns(self, is_lying_down: bool, timestamp: datetime) -> Dict:
        """Analyze sleep quality and patterns"""
        self.sleep_log.append({
            'lying_down': is_lying_down,
            'timestamp': timestamp
        })
        
        # Keep last 3 days
        cutoff = datetime.now() - timedelta(days=3)
        self.sleep_log = [s for s in self.sleep_log if s['timestamp'] > cutoff]
        
        # Analyze last night's sleep
        last_night_start = datetime.now().replace(hour=22, minute=0) - timedelta(days=1)
        last_night_end = datetime.now().replace(hour=6, minute=0)
        
        night_sleep = [s for s in self.sleep_log 
                      if last_night_start < s['timestamp'] < last_night_end]
        
        if len(night_sleep) > 0:
            sleep_time = sum(1 for s in night_sleep if s['lying_down'])
            total_time = len(night_sleep)
            sleep_percentage = (sleep_time / total_time) * 100 if total_time > 0 else 0
            
            # Detect poor sleep
            poor_sleep = sleep_percentage < 60
            
            return {
                'sleep_percentage': sleep_percentage,
                'poor_sleep': poor_sleep,
                'status': 'Poor sleep quality' if poor_sleep else 'Good sleep'
            }
        
        return {'status': 'Insufficient data'}
    
    def detect_confusion_signs(self, pose_landmarks) -> Tuple[bool, str]:
        """Detect confusion/disorientation indicators"""
        if not pose_landmarks:
            return False, "No pose detected"
        
        try:
            # Get head position
            nose = pose_landmarks[0]
            
            # Track head movement patterns
            self.confusion_indicators.append({
                'x': nose.x,
                'y': nose.y
            })
            
            if len(self.confusion_indicators) >= 60:
                # Calculate head movement variance (confusion = erratic head movement)
                positions = np.array([(c['x'], c['y']) for c in list(self.confusion_indicators)[-60:]])
                variance = np.var(positions, axis=0).sum()
                
                # High variance = erratic movement = possible confusion
                is_confused = variance > 0.02
                
                if is_confused:
                    return True, "Erratic head movements detected - possible confusion"
            
            return False, "Normal behavior"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def detect_social_interaction(self, num_people_detected: int) -> Dict:
        """Monitor social interaction levels"""
        # Track number of people in frame over time
        # Reduced interaction = possible deterioration
        
        return {
            'people_count': num_people_detected,
            'interaction_level': 'High' if num_people_detected > 1 else 'Low',
            'isolation_concern': num_people_detected == 1
        }


class HealthRiskCalculator:
    """Calculate overall health risk and deterioration prediction"""
    
    def __init__(self):
        self.stroke_detector = StrokeDetector()
        self.cardiac_detector = CardiacIndicatorDetector()
        self.behavioral_analyzer = BehavioralAnalyzer()
    
    def calculate_overall_health_score(self, stroke_risk: int, cardiac_risk: int,
                                      activity_declining: bool, poor_sleep: bool) -> Dict:
        """Calculate comprehensive health risk score"""
        
        # Weighted scoring
        overall_score = (
            stroke_risk * 0.35 +
            cardiac_risk * 0.35 +
            (30 if activity_declining else 0) * 0.15 +
            (20 if poor_sleep else 0) * 0.15
        )
        
        # Determine overall risk
        if overall_score >= 70:
            risk_level = "CRITICAL"
            action = "IMMEDIATE medical intervention required"
        elif overall_score >= 50:
            risk_level = "HIGH"
            action = "Urgent assessment needed"
        elif overall_score >= 30:
            risk_level = "MEDIUM"
            action = "Increased monitoring recommended"
        else:
            risk_level = "LOW"
            action = "Continue routine care"
        
        return {
            'overall_health_score': int(overall_score),
            'risk_level': risk_level,
            'action_required': action,
            'component_scores': {
                'stroke_risk': stroke_risk,
                'cardiac_risk': cardiac_risk,
                'behavioral_concerns': activity_declining or poor_sleep
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def predict_deterioration_timeline(self, current_trends: Dict) -> List[Dict]:
        """Predict when patient might deteriorate"""
        predictions = []
        
        # Simple prediction based on current trends
        if current_trends.get('activity_declining'):
            predictions.append({
                'timeframe': '2-4 hours',
                'event': 'Further activity decline',
                'probability': 0.7,
                'severity': 'MEDIUM'
            })
        
        if current_trends.get('breathing_distress'):
            predictions.append({
                'timeframe': '1-2 hours',
                'event': 'Respiratory distress',
                'probability': 0.8,
                'severity': 'HIGH'
            })
        
        if current_trends.get('stroke_indicators'):
            predictions.append({
                'timeframe': 'IMMEDIATE',
                'event': 'Stroke progression',
                'probability': 0.9,
                'severity': 'CRITICAL'
            })
        
        return predictions
