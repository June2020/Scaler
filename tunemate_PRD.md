# **Product Requirements Document (PRD)**

## **Product Name:**

TuneMate (working name)

## **Prepared By:**

[Your Name]

## **Date:**

[Insert Date]

---

# **1. Product Overview**

TuneMate is an Android application that helps users identify the **musical key, tempo (BPM), and suitable chords** of a song by recording or singing it. It enhances the experience by allowing users to  **replay their input with guitar strumming and beats** , enabling quick musical exploration and improvement.

---

# **2. Problem Statement**

Many beginner and hobby musicians struggle to:

* Identify the **key of a song**
* Find **matching chords**
* Choose an appropriate **rhythm/beat**

Existing tools are either:

* Too complex (DAWs)
* Too technical
* Not beginner-friendly

---

# **3. Goals & Objectives**

## **Primary Goals**

* Enable users to detect **key and BPM** from audio input
* Provide **instant chord suggestions**
* Allow playback with **guitar + beat accompaniment**

## **Success Metrics**

* ≥ 80% perceived accuracy of key detection
* ≥ 60% users use playback feature
* < 10 seconds analysis time
* ≥ 30% repeat usage rate

---

# **4. Target Users**

### **Primary Users**

* Beginner guitarists
* Hobby singers
* Casual musicians

### **Secondary Users**

* Music learners
* Content creators

---

# **5. User Personas**

### **Persona 1: Beginner Guitarist**

* Wants to play songs by ear
* Doesn’t know music theory

### **Persona 2: Singer**

* Wants to find correct pitch/key
* Experiments with songs

---

# **6. User Stories**

* As a user, I want to  **record my singing** , so that I can analyze it
* As a user, I want to  **select how long the app listens** , so that I can control accuracy
* As a user, I want to  **see the key of my song** , so that I understand its structure
* As a user, I want  **chord suggestions** , so I can play along
* As a user, I want to  **hear my song with guitar and beat** , so I can improve it
* As a user, I want to  **retry easily** , if I don’t like the result

---

# **7. Features & Requirements**

## **7.1 Audio Recording**

* Record audio from microphone
* Show waveform animation
* Start/Stop controls

---

## **7.2 Listening Duration Selection**

User selects analysis duration:

* 1 minute
* 2 minutes
* 5 minutes

Default: 1 minute

---

## **7.3 Audio Analysis**

### **Outputs**

* Musical key (e.g., C Major, A Minor)
* BPM (e.g., 90 BPM)

### **Constraints**

* Processing time < 10 seconds
* Handle moderate background noise

---

## **7.4 Chord Suggestion Engine**

* Based on detected key
* Show:
* Primary chords
* Suggested progression

Example:

* Key: G Major
* Chords: G – C – D – Em

---

## **7.5 Playback Engine**

### **Capabilities**

* Replay recorded audio
* Add:
* Guitar strumming
* Beat/rhythm

### **Controls**

* Play/Pause
* Change beat style (basic in MVP)
* Toggle guitar

---

## **7.6 Retry Flow**

* Re-record option
* Re-analyze instantly
* No history required in MVP

---

# **8. User Flow**

1. Launch App
2. Select duration
3. Tap Record
4. Perform (sing/play)
5. Tap Analyze
6. View Results:

* Key
* BPM
* Chords

1. Tap “Play with Beat & Guitar”
2. User:

* Accept → Exit
* Retry → Go back

---

# **9. UX/UI Requirements**

## **Design Principles**

* Minimalistic
* Music-centric
* Beginner-friendly

## **Core Screens**

1. Home Screen

* Record button
* Duration selector

1. Recording Screen

* Waveform
* Timer

1. Results Screen

* Large key display
* BPM
* Chords

1. Playback Screen

* Play controls
* Beat/guitar toggles

---

# **10. Functional Requirements**

| ID  | Requirement                 |
| --- | --------------------------- |
| FR1 | Record audio input          |
| FR2 | Allow duration selection    |
| FR3 | Detect musical key          |
| FR4 | Detect BPM                  |
| FR5 | Generate chord suggestions  |
| FR6 | Playback with beat & guitar |
| FR7 | Allow retry                 |

---

# **11. Non-Functional Requirements**

| Category      | Requirement       |
| ------------- | ----------------- |
| Performance   | Analysis < 10 sec |
| Usability     | Simple UI         |
| Accuracy      | ≥ 80% acceptable |
| Reliability   | Stable playback   |
| Compatibility | Android 8+        |

---

# **12. Technical Approach**

## **Architecture**

* Android app (Kotlin)
* Backend API (Python FastAPI)
* Audio processing:
* librosa (initial)
* Essentia (later)

## **Data Flow**

1. Record audio
2. Upload to backend
3. Analyze key + BPM
4. Return results
5. Playback generated locally

---

# **13. Risks & Mitigation**

| Risk               | Mitigation                   |
| ------------------ | ---------------------------- |
| Poor accuracy      | Improve algorithms gradually |
| Noise interference | Add filters                  |
| Slow processing    | Optimize backend             |
| User confusion     | Keep UI simple               |

---

# **14. Future Enhancements**

* AI-based key detection
* Real-time detection (live mode)
* Save & share recordings
* Advanced chord progressions
* Multiple instruments support

---

# **15. MVP Scope Summary**

### **Included**

* Recording
* Key detection
* BPM detection
* Chord suggestions
* Playback with guitar + beat
* Retry

### **Excluded**

* AI models
* Social features
* Export functionality

---

# **16. Release Plan**

### **Phase 1 (MVP)**

* Core detection + playback

### **Phase 2**

* Improved accuracy
* Better beat styles

### **Phase 3**

* AI enhancements
* Advanced music features

---

# **Final Note**

This product should prioritize:

👉 **Speed to market**

👉 **Simplicity**

👉 **Good-enough accuracy over perfection**
