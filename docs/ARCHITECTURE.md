# 🏗️ MedAdhere Pro - System Architecture

## 📐 Overall Architecture (Minimum Viable Demo)

```
┌────────────────────────────────────────────────────────────────┐
│                     USER LAYER (Mobile-First)                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  📱 Mobile UI Prototype                                        │
│  ├─ Push Notification Mockups                                 │
│  ├─ Quick Action Screens                                      │
│  ├─ Agent Reasoning Chat                                      │
│  └─ Adherence Dashboard                                       │
│                                                                │
│  Implementation: Figma Prototype + Screen Recordings          │
│                  OR Simple React/Flutter Demo                  │
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
│  🧠 MedGemma Inference Service (GCP VM)                        │
│                                                                │
│  Model: google/medgemma-1.5-4b-it                             │
│  Instance: n1-standard-4 (4 vCPU, 15GB RAM)                   │
│  Location: us-central1-a                                      │
│  External IP: 136.116.155.46:8080                             │
│                                                                │
│  Endpoints:                                                    │
│  • POST /generate (medical reasoning)                          │
│  • GET  /health (service status)                              │
│                                                                │
│  Use Cases:                                                    │
│  • Validate medication safety                                  │
│  • Check drug interactions                                     │
│  • Provide medical guidance                                    │
│  • Assess symptom severity                                     │
│                                                                │
│  Response Time: 30-60 seconds (CPU inference)                  │
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
   Patient taps: [❌ Skip] → "I forgot"
   ↓
   Mobile app sends to Firebase:
   {
     patient_id: "p001",
     action: "skip",
     reason: "forgot",
     timestamp: "2026-02-17T08:00:00Z"
   }

3. AGENT ACTIVATION
   Firebase triggers webhook → Flask Backend
   ↓
   AgentOrchestrator receives event
   ↓
   Routes to InvestigationAgent

4. INVESTIGATION PHASE
   InvestigationAgent:
   - Queries Firestore: get_adherence_history(p001)
   - Finds: 3 "forgot" events this week (all Monday AM)
   - Analyzes: "Pattern detected - weekday morning rush"
   ↓
   Streams to client via WebSocket:
   {
     type: "investigation_complete",
     finding: "Monday morning pattern",
     data: { skip_count: 3, pattern: "weekday_am" }
   }

5. REMEDIATION PHASE
   RemediationAgent:
   - Generates solutions based on pattern
   - Options: [earlier_reminder, habit_linking, pill_placement]
   ↓
   Streams to client:
   {
     type: "remediation_proposed",
     solution: "Move Monday reminder to 7:30 AM",
     reasoning: "Avoids morning rush period"
   }

6. RISK ASSESSMENT
   RiskAssessmentAgent:
   - Calls MedGemma VM:
     "Is it safe to take Metformin 30 min earlier?"
   - MedGemma response: "Yes, safe. Timing flexibility OK."
   ↓
   Streams to client:
   {
     type: "safety_validated",
     verdict: "approved",
     medgemma_reasoning: "Time shift is safe"
   }

7. USER DECISION
   Mobile shows options:
   "Move Monday reminder to 7:30 AM?"
   [Yes, try it] [No thanks] [Tell me more]
   ↓
   User: "Yes, try it"

8. EXECUTION PHASE
   ExecutionAgent:
   - Updates Firebase schedule
   - Firestore write: /patients/p001/schedule/monday = "07:30"
   - Reschedules Firebase Cloud Function
   ↓
   Confirmation to user:
   "Done! I'll remind you at 7:30 AM on Mondays"

9. LEARNING PHASE
   LearningAgent:
   - Logs intervention:
     problem: "forgot_doses",
     pattern: "monday_morning",
     solution: "earlier_reminder",
     expected_outcome: "improved_adherence"
   - Updates ML model
   - Schedules follow-up check (next Monday)

10. FOLLOW-UP (Next Monday 7:30 AM)
    Firebase sends earlier reminder
    ↓
    Patient takes medication on time
    ↓
    LearningAgent records success
    ↓
    Positive reinforcement notification:
    "Great! That's 3 days in a row! 🎯"
```

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
      "medication": "Metformin",
      "scheduled_time": "08:00",
      "actual_time": null,
      "status": "missed",
      "reason": "forgot",
      "context": {
        "day_of_week": "monday",
        "location": "home",
        "activity": "morning_rush"
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

### **Frontend (Mobile UI)**
- **Option A:** Figma mockups + screen recordings (fastest for demo)
- **Option B:** React Native (production-ready)
- **Option C:** Flutter (cross-platform)

### **Backend (Agent Orchestration)**
- **Language:** Python 3.10+
- **Framework:** Flask 3.0
- **Agent Engine:** Custom multi-agent orchestrator
- **WebSocket:** Flask-SocketIO for real-time chat
- **Deployment:** Google Cloud Run (serverless) or VM

### **Database & Real-time Sync**
- **Primary DB:** Firebase Firestore (real-time NoSQL)
- **Notifications:** Firebase Cloud Messaging (FCM)
- **Functions:** Firebase Cloud Functions (Node.js/Python)
- **Auth:** Firebase Authentication

### **AI Model**
- **Model:** google/medgemma-1.5-4b-it
- **Deployment:** GCP Compute Engine VM (n1-standard-4)
- **Framework:** PyTorch + Transformers
- **API:** Flask REST server

### **Infrastructure**
- **Cloud Provider:** Google Cloud Platform (GCP)
- **Region:** us-central1 (low latency)
- **Monitoring:** GCP Cloud Logging + Firebase Analytics
- **Cost:** ~$5-10/day for demo (can stop when not testing)

---

## 🚦 API Endpoints

### **Agent Orchestration APIs**

#### `POST /api/patient-action`
Logs patient medication action (took it, skipped, etc.)

**Request:**
```json
{
  "patient_id": "p001",
  "medication": "Metformin",
  "scheduled_time": "08:00",
  "action": "skip",
  "reason": "forgot",
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

#### `POST http://136.116.155.46:8080/generate`
Medical reasoning and safety validation

**Request:**
```json
{
  "prompt": "Is it safe to take Metformin 30 minutes earlier than scheduled?",
  "max_length": 512,
  "temperature": 0.7
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

### **Current (Demo):**
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

## 💰 Cost Estimate (Demo Period)

| Component | Cost/Day | Notes |
|-----------|----------|-------|
| MedGemma VM (n1-standard-4) | $4.56 | Stop when not testing |
| Firebase (Firestore + FCM) | $0-1 | Free tier sufficient |
| Cloud Functions | $0 | Free tier (2M invocations) |
| Bandwidth | $0.50 | Minimal for demo |
| **Total** | **~$5/day** | **~$150/month if always on** |

**Optimization:** Stop VM after testing → **$0.20/day** (storage only)

---

## 🎯 Minimum Viable Demo Scope

### **✅ Must Have (For Competition):**
1. Mobile UI mockups (5 key screens)
2. Push notification flow (simulated)
3. Agent orchestration backend (working)
4. MedGemma integration (deployed & tested)
5. 3 complete scenarios (forgot, refill, side effects)
6. Real-time reasoning display (WebSocket)
7. Demo video (3-5 minutes)

### **❌ Not Needed (For Competition):**
- Full native mobile app (mockups sufficient)
- App store deployment
- Real pharmacy integrations (mock data OK)
- EHR connections (sample data)
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
   └─ Mobile UI mockups (Next)

2. Backend Development
   └─ Agent orchestrator
   └─ Firebase integration
   └─ WebSocket implementation

3. MedGemma Integration
   └─ Deploy VM (Already done ✓)
   └─ Test inference
   └─ API wrapper

4. Demo Creation
   └─ Mobile screen recordings
   └─ Video editing
   └─ Script writing

5. Competition Submission
   └─ Documentation
   └─ Code cleanup
   └─ Final testing
```

---

## 📚 See Also

- [AGENTS.md](AGENTS.md) - Detailed agent workflows
- [MOBILE.md](MOBILE.md) - Mobile-first design patterns
- [COMPETITION.md](COMPETITION.md) - Submission guidelines
- [SETUP.md](SETUP.md) - Development setup instructions
