# 🏗️ MedAdhere Pro - System Architecture

## 📐 Overall System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     USER LAYER (Mobile-First)                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  📱 Web User Interface                                         │
│  ├─ Push Notification Display                                 │
│  ├─ Quick Action Buttons                                      │
│  ├─ Agent Reasoning Visualization                             │
│  └─ Adherence Dashboard                                       │
│                                                                │
│  Implementation: HTML5, JavaScript, TailwindCSS                │
│                                                                │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ Push Notifications (Firebase Cloud Messaging)
                 │ WebSocket (Real-time bidirectional)
                 │ REST APIs (HTTPS)
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                  NOTIFICATION & SYNC LAYER                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  🔥 Firebase Services                                          │
│  ├─ Cloud Messaging (Push notifications)                      │
│  ├─ Firestore (Real-time patient data)                        │
│  ├─ Cloud Functions (Scheduled triggers)                      │
│  └─ Authentication (Patient login)                            │
│                                                                │
│  Responsibilities:                                             │
│  • Send medication reminders at scheduled times                │
│  • Trigger agents when patient interacts                       │
│  • Store patient profiles, schedules, adherence logs           │
│  • Handle real-time sync across devices                        │
│                                                                │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ HTTP/WebSocket
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATION LAYER                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  🤖 Flask Backend (Python)                                     │
│                                                                │
│  Main Components:                                              │
│  ├─ AgentOrchestrator (routes to correct agent)               │
│  ├─ InvestigationAgent (analyzes patterns)                    │
│  ├─ RemediationAgent (creates solutions)                      │
│  ├─ RiskAssessmentAgent (validates with MedGemma)             │
│  ├─ ExecutionAgent (implements changes)                       │
│  └─ LearningAgent (improves over time)                        │
│                                                                │
│  APIs:                                                         │
│  • POST /api/patient-action (logs medication actions)          │
│  • POST /api/agent-query (triggers agent workflow)             │
│  • GET  /api/stream-reasoning (SSE for real-time updates)      │
│  • POST /api/update-schedule (modify reminders)                │
│                                                                │
│  WebSocket:                                                    │
│  • ws://backend/agent-chat (real-time agent communication)     │
│                                                                │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ HTTP POST
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                     MEDICAL AI LAYER                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  🧠 MedGemma Inference Service (Hugging Face Endpoint)         │
│                                                                │
│  Model: google/medgemma-2-2b-it                               │
│  Endpoint: Hugging Face Inference Endpoint                    │
│  Vision: image-text-to-text (multimodal)                      │
│                                                                │
│  Endpoints:                                                    │
│  • POST /generate (medical reasoning - text)                   │
│  • POST /generate (multimodal - image + text analysis)         │
│  • GET  /health (service status)                              │
│                                                                │
│  Use Cases:                                                    │
│  • Validate medication safety                                  │
│  • Check drug interactions                                     │
│  • Provide medical guidance                                    │
│  • Assess symptom severity                                     │
│  • Visual analysis of side effects (rashes, skin conditions)   │
│  • Temporal healing progression tracking (multi-day images)    │
│                                                                │
│  Response Time: 30-60 seconds (text and vision)                │
│                                                                │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ (Optional integrations)
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                   EXTERNAL INTEGRATIONS                        │
│                    (Future/Optional)                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  💊 Pharmacy APIs (CVS, Walgreens)                            │
│  🏥 EHR Systems (FHIR APIs)                                   │
│  📧 Communication (Twilio for SMS)                            │
│  🩺 Health Data (Apple Health, Google Fit)                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow: Complete User Journey

### **Example: Patient Forgets Medication**

```
1. SCHEDULED TRIGGER (8:00 AM)
   Firebase Cloud Function: send_medication_reminder()
   ↓
   Push Notification: "Time for Metformin 💊"
   [✓ Took It] [⏰ Snooze] [❌ Skip]

2. USER INTERACTION
   Patient taps: [❌ Skip] → "Too confusing - timing conflict"
   ↓
   Mobile app sends to Firebase:
   {
     patient_id: "p001",
     action: "skip",
     reason: "timing_conflict",
     timestamp: "2026-02-17T08:00:00Z",
     notes: "Don't know when to take thyroid vs calcium vs metformin"
   }

3. AGENT ACTIVATION
   Firebase triggers webhook → Flask Backend
   ↓
   AgentOrchestrator receives event
   ↓
   Routes to InvestigationAgent

4. INVESTIGATION PHASE
   InvestigationAgent:
   - Queries Firestore: get_medication_list(p001)
   - Finds: 3 medications with complex timing requirements
   - Analyzes: "Multiple timing conflicts detected"
   ↓
   Streams to client via WebSocket:
   {
     type: "investigation_complete",
     finding: "Medication timing complexity",
     data: { medication_count: 3, complexity: "high" }
   }

5. REMEDIATION PHASE
   RemediationAgent:
   - Calls MedGemma VM:
     "Create optimal schedule for: Levothyroxine (empty stomach, 1hr before food),
      Metformin (with food), Calcium (4hrs after thyroid)"
   - MedGemma generates: Optimized schedule
   ↓
   Streams to client:
   {
     type: "remediation_proposed",
     solution: "6:30 AM - Levothyroxine, 7:30 AM - Breakfast + Metformin, 12:00 PM - Calcium",
     reasoning: "Meets all medical timing requirements"
   }

6. RISK ASSESSMENT
   RiskAssessmentAgent:
   - Calls MedGemma VM:
     "Validate safety of this schedule"
   - MedGemma response: "Approved. No absorption conflicts."
   ↓
   Streams to client:
   {
     type: "safety_validated",
     verdict: "approved",
     medgemma_reasoning: "Schedule is medically safe"
   }

7. USER DECISION
   Mobile shows simplified schedule:
   "New schedule to avoid confusion?"
   [Yes, use this] [No thanks]
   ↓
   User: "Yes, use this"

8. EXECUTION PHASE
   ExecutionAgent:
   - Updates Firebase schedule
   - Firestore write: /patients/p001/schedule/optimized = true
   - Updates all medication reminders
   ↓
   Confirmation to user:
   "Done! Clear instructions sent for each medication"

9. LEARNING PHASE
   LearningAgent:
   - Logs intervention:
     problem: "timing_complexity",
     pattern: "multiple_medications",
     solution: "optimized_schedule",
     expected_outcome: "improved_adherence"
   - Updates ML model
   - Schedules follow-up check (in 1 week)

10. FOLLOW-UP (Next Week)
    System tracks adherence improvement
    ↓
    Patient follows simplified schedule
    ↓
    LearningAgent records success
    ↓
    Positive reinforcement notification:
    "Great! Following your new schedule perfectly! 🎯"
```

### **Scenario 4 Workflow: Side Effect Healing Tracker (Multimodal AI with Vision)**

**Patient:** David, 52, develops allopurinol rash Day 3. Needs objective tracking to decide continue vs stop.

```
Day 3: Initial Report + Photo
  Patient uploads rash photo
  ↓
  Risk Agent detects image field
  ↓
  Calls MedGemma Vision API
  ↓
  Baseline assessment: "Mild urticarial rash, no emergency signs"
  ↓
  Approves daily monitoring protocol

Day 4: Follow-up Photo
  Patient uploads Day 4 photo
  ↓
  Temporal comparison: Day 3 → Day 4
  ↓
  MedGemma Vision: "Lesion count -15%, redness decreasing"
  ↓
  Healing trend: IMPROVING
  ↓
  Recommendation: Continue medication

Day 5: Second Follow-up
  Patient uploads Day 5 photo
  ↓
  Temporal comparison: Day 3 → Day 4 → Day 5
  ↓
  MedGemma Vision: "Lesion count -38%, clear improvement"
  ↓
  Healing trajectory: RESOLVING
  ↓
  Recommendation: Continue, rash healing

Outcome: Patient continues allopurinol, rash resolves by Day 10
```

**Key Architecture Points:**
- Same 5-agent workflow (no new agents)
- Risk Agent adds vision API call when image present
- Image field is optional (Scenarios 1-3 unchanged)
- Temporal tracking via previous_images array

---

## 🗂️ Data Models

### **Patient Profile**
```json
{
  "patient_id": "p001",
  "name": "Grace Patel",
  "age": 45,
  "conditions": ["type_2_diabetes"],
  "medications": [
    {
      "name": "Metformin",
      "dosage": "500mg",
      "frequency": "twice_daily",
      "times": ["08:00", "20:00"],
      "instructions": "Take with food"
    }
  ],
  "preferences": {
    "reminder_style": "gentle",
    "notification_sound": "default"
  }
}
```

### **Adherence Log**
```json
{
  "patient_id": "p001",
  "date": "2026-02-17",
  "doses": [
    {
      "medication": "Levothyroxine",
      "scheduled_time": "08:00",
      "actual_time": null,
      "status": "missed",
      "reason": "timing_conflict",
      "context": {
        "day_of_week": "monday",
        "location": "home",
        "activity": "confused_about_timing"
      }
    }
  ]
}
```

### **Agent Intervention**
```json
{
  "intervention_id": "int_001",
  "patient_id": "p001",
  "timestamp": "2026-02-17T08:05:00Z",
  "trigger": "missed_dose_pattern",
  "agents_involved": [
    "investigation",
    "remediation",
    "risk_assessment",
    "execution"
  ],
  "investigation_findings": {
    "root_cause": "monday_morning_rush",
    "pattern_confidence": 0.87
  },
  "proposed_solution": {
    "action": "adjust_reminder_time",
    "details": "Move Monday reminder from 08:00 to 07:30"
  },
  "safety_check": {
    "medgemma_consulted": true,
    "verdict": "approved",
    "reasoning": "Timing flexibility safe for Metformin"
  },
  "execution_result": {
    "status": "completed",
    "changes_made": ["schedule_updated"]
  },
  "follow_up_date": "2026-02-24"
}
```

---

## 🔧 Technology Stack

### **Frontend**
- **Current:** HTML5, JavaScript, TailwindCSS (Web UI)
- **Future:** Native mobile apps (iOS/Android)

### **Backend (Agent Orchestration)**
- **Language:** Python 3.10+
- **Framework:** Flask 3.0
- **Agent Engine:** Custom multi-agent orchestrator
- **WebSocket:** Flask-SocketIO for real-time communication
- **Deployment:** Google Cloud Run (serverless) or VM

### **Database & Real-time Sync**
- **Primary DB:** Firebase Firestore (real-time NoSQL)
- **Notifications:** Firebase Cloud Messaging (FCM)
- **Functions:** Firebase Cloud Functions (Node.js/Python)
- **Auth:** Firebase Authentication

### **AI Model**
- **Model:** google/medgemma-2-2b-it
- **Deployment:** Hugging Face Inference Endpoint (Dedicated)
- **Framework:** Transformers
- **API:** REST API (text and multimodal)
- **Vision Capability:** image-text-to-text multimodal endpoint
  - **Use Case:** Temporal tracking of healing progression with multi-day photos
  - **Integration:** Optional image + previous_images fields in patient action data
  - **Processing:** Risk Assessment Agent conditionally calls vision API when image present
  - **Features:** Single workflow with 3+ images for comprehensive temporal analysis
  - **Analysis:** Lesion count, redness intensity, healing trajectory comparison
  - **Output:** Objective visual assessment to support continue/stop decisions

### **Infrastructure**
- **Cloud Provider:** Google Cloud Platform (GCP)
- **Region:** us-central1 (low latency)
- **Monitoring:** GCP Cloud Logging + Firebase Analytics
- **Cost:** ~$5-10/day for development/testing

---

## 🚦 API Endpoints

### **Agent Orchestration APIs**

#### `POST /api/patient-action`
Logs patient medication action (took it, skipped, etc.)

**Request:**
```json
{
  "patient_id": "p001",
  "medication": "Levothyroxine",
  "scheduled_time": "08:00",
  "action": "skip",
  "reason": "timing_conflict",
  "timestamp": "2026-02-17T08:02:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "agent_triggered": true,
  "intervention_id": "int_001",
  "message": "I'll help you with that!"
}
```

#### `POST /api/agent-query`
Triggers agent workflow for a question or issue

**Request:**
```json
{
  "patient_id": "p001",
  "query": "I'm feeling nauseous after taking Metformin",
  "context": {
    "medication": "Metformin",
    "time_since_dose": "25 minutes",
    "taken_with_food": false
  }
}
```

**Response (SSE stream):**
```
event: investigation
data: {"agent": "investigation", "message": "Analyzing symptoms..."}

event: medgemma
data: {"agent": "risk", "message": "Consulting MedGemma for safety..."}

event: solution
data: {"agent": "remediation", "solution": "Take with meals", "confidence": 0.92}

event: complete
data: {"success": true, "recommendation": "Try taking with breakfast"}
```

#### `GET /api/stream-reasoning`
Server-Sent Events (SSE) for real-time agent reasoning

**Query Params:** `patient_id=p001&intervention_id=int_001`

**Stream:**
```
data: {"type": "start", "message": "Investigation starting..."}

data: {"type": "step", "agent": "investigation", "finding": "Pattern detected"}

data: {"type": "step", "agent": "remediation", "proposal": "Earlier reminder"}

data: {"type": "complete", "result": "Solution proposed"}
```

### **MedGemma Inference API**

#### Text Analysis: `POST https://<endpoint>.huggingface.cloud`
Medical reasoning and safety validation

**Request:**
```json
{
  "inputs": "Is it safe to take Metformin 30 minutes earlier than scheduled?",
  "parameters": {
    "max_new_tokens": 512,
    "temperature": 0.7
  }
}
```

**Response:**
```json
{
  "generated_text": "Yes, taking Metformin 30 minutes earlier is generally safe..."
}
```

#### Vision Analysis: `POST https://<endpoint>.huggingface.cloud`
Multimodal image + text analysis for side effects

**Request:**
```json
{
  "inputs": {
    "text": "Analyze this rash progression from Day 3 to Day 5...",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  },
  "parameters": {
    "max_new_tokens": 512,
    "temperature": 0.7
  }
}
```

**Response:**
```json
{
  "generated_text": "Yes, Metformin has flexible timing. Taking it 30 minutes earlier is safe...",
  "inference_time": 45.2
}
```

---

## 🔐 Security & Privacy

### **Patient Data Protection**
- All data encrypted at rest (Firebase encryption)
- HTTPS/TLS for all communications
- HIPAA-compliant data handling (for production)
- Minimal data collection (only what's needed)

### **Authentication**
- Firebase Authentication (email/phone)
- Biometric unlock option (fingerprint/face)
- Session expiration (30 days)

### **MedGemma Safety**
- No patient data sent to MedGemma (only anonymized queries)
- All medical advice includes disclaimers
- Doctor escalation for uncertain cases
- Audit log of all AI decisions

---

## 📏 Scalability Considerations

### **Current Implementation:**
- 1-10 test patients
- Single GCP VM for MedGemma
- Firebase free tier

### **Production (Future):**
- 10,000+ patients
- MedGemma: Auto-scaling with GPU
- Firebase Blaze plan (pay-as-you-go)
- CDN for static assets
- Multi-region deployment

---

## 💰 Cost Estimate (Development)

| Component | Cost/Day | Notes |
|-----------|----------|-------|
| MedGemma VM (n1-standard-4) | $4.56 | Stop when not testing |
| Firebase (Firestore + FCM) | $0-1 | Free tier sufficient |
| Cloud Functions | $0 | Free tier (2M invocations) |
| Bandwidth | $0.50 | Minimal for development |
| **Total** | **~$5/day** | **~$150/month if always on** |

**Optimization:** Stop VM after testing → **$0.20/day** (storage only)

---

## 🎯 Current Implementation Scope

### **✅ Implemented Features:**
1. Web-based user interface
2. Push notification flow (simulated)
3. Agent orchestration backend (5 specialized agents)
4. MedGemma integration (deployed & tested)
5. 3 complete scenarios (timing conflict, supplement interference, side effects)
6. Real-time reasoning display (WebSocket)
7. Intelligent workflow summaries

### **🔜 Future Enhancements:**
- Native mobile apps (iOS & Android)
- App store deployment
- Real pharmacy integrations
- EHR system connections
- Production-scale infrastructure

---

## 📊 Success Metrics

### **Technical Metrics:**
- Agent response time: < 5 seconds
- MedGemma inference: 30-60 seconds
- WebSocket latency: < 500ms
- Notification delivery: 99%+

### **Healthcare Metrics:**
- Adherence improvement: 60% → 87%
- Intervention success rate: 70%+
- Time to resolution: < 2 minutes
- Patient satisfaction: 4.5/5

---

## 🔄 Development Workflow

```
1. Design Phase (Current)
   └─ Architecture documentation ✓
   └─ Agent workflow design ✓
   └─ Mobile app development (Next)

2. Backend Development
   └─ Agent orchestrator
   └─ Firebase integration
   └─ WebSocket implementation

3. MedGemma Integration
   └─ Deploy VM (Already done ✓)
   └─ Test inference
   └─ API wrapper

4. Production Readiness
   └─ Mobile app development
   └─ External integrations
   └─ Security hardening
```

---

## 📚 See Also

- [AGENTIC_FLOWS.md](AGENTIC_FLOWS.md) - Multi-agent workflow diagrams
- [MOBILE_ARCHITECTURE.md](MOBILE_ARCHITECTURE.md) - Production mobile-first architecture
