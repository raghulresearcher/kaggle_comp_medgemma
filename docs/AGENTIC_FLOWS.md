# Agentic Workflow Diagrams

This document illustrates the multi-agent workflows for different medication adherence scenarios.

## System Architecture

```mermaid
graph TB
    UI[Web UI / API] --> Orchestrator[Agent Orchestrator]
    Orchestrator --> INV[Investigation Agent]
    Orchestrator --> REM[Remediation Agent]
    Orchestrator --> RISK[Risk Assessment Agent]
    Orchestrator --> EXEC[Execution Agent]
    Orchestrator --> LEARN[Learning Agent]
    
    INV --> Firebase[(Firebase Firestore)]
    REM --> Firebase
    EXEC --> Firebase
    LEARN --> Firebase
    
    RISK --> MedGemma[MedGemma AI]
    
    style Orchestrator fill:#4CAF50
    style INV fill:#2196F3
    style REM fill:#FF9800
    style RISK fill:#F44336
    style EXEC fill:#9C27B0
    style LEARN fill:#00BCD4
    style MedGemma fill:#FFD700
```

---

## Scenario 1: Medication Timing Conflict

**Trigger:** `action="skipped"`, `reason="timing_conflict"`

### Patient Problem
Patient has multiple medications with complex timing requirements (empty stomach, with food, 4 hours apart). Patient skips doses due to confusion about when to take each medication.

### Workflow Flow

```mermaid
sequenceDiagram
    participant Patient
    participant UI
    participant Orch as Orchestrator
    participant Inv as Investigation Agent
    participant Rem as Remediation Agent
    participant Risk as Risk Assessment
    participant Exec as Execution Agent
    participant Learn as Learning Agent
    participant DB as Firebase
    participant AI as MedGemma

    Patient->>UI: Reports "Skipped - Too confusing"
    UI->>Orch: Patient Action Data
    
    rect rgb(200, 220, 240)
        Note over Orch,Inv: Agent 1: Investigation
        Orch->>Inv: Analyze Pattern
        Inv->>DB: Query medication list
        DB-->>Inv: 3 medications:<br/>Levothyroxine, Metformin, Calcium
        Inv->>DB: Check timing requirements
        DB-->>Inv: Complex rules detected
        Inv->>Inv: Pattern: Patient skips morning doses<br/>Root cause: Timing confusion
        Inv-->>Orch: Issue: "Multiple medication timing conflicts"
    end
    
    rect rgb(255, 230, 200)
        Note over Orch,Rem: Agent 2: Remediation
        Orch->>Rem: Create Solution
        Rem->>AI: MedGemma consult:<br/>"Create optimal schedule for:<br/>Levothyroxine (empty stomach, 1hr before food)<br/>Metformin (with food)<br/>Calcium (4hrs after levothyroxine)"
        AI-->>Rem: Optimized schedule:<br/>6:30 AM - Levothyroxine<br/>7:30 AM - Breakfast + Metformin<br/>12:00 PM - Calcium
        Rem-->>Orch: Simplified schedule + clear instructions
    end
    
    rect rgb(255, 200, 200)
        Note over Orch,Risk: Agent 3: Risk Assessment
        Orch->>Risk: Validate Safety
        Risk->>AI: Check: Is timing medically safe?<br/>Any absorption conflicts?
        AI-->>Risk: Approved - meets all requirements<br/>No drug interactions with timing
        Risk-->>Orch: Medically validated (Risk: Low)
    end
    
    rect rgb(230, 200, 250)
        Note over Orch,Exec: Agent 4: Execution
        Orch->>Exec: Implement Solution
        Exec->>DB: Update medication schedule
        Exec->>Patient: Clear instructions:<br/>"6:30 AM - Thyroid pill (empty stomach)<br/>7:30 AM - Breakfast + Diabetes pill<br/>12:00 PM - Calcium"
        Exec-->>Orch: Patient notified + schedule updated
    end
    
    rect rgb(200, 240, 240)
        Note over Orch,Learn: Agent 5: Learning
        Orch->>Learn: Track Outcome
        Learn->>DB: Store timing pattern
        Learn->>Learn: Pattern type: Timing complexity<br/>Solution: Simplified schedule<br/>Success rate: Track adherence
        Learn-->>Orch: Learning complete
    end
    
    Orch->>UI: Workflow Complete
    UI->>Patient: Show simplified schedule
```

### Decision Points

```mermaid
graph TD
    Start[Patient Skipped:<br/>Timing Conflict] --> CheckMeds{Multiple<br/>Medications?}
    CheckMeds -->|Yes| Analyze[Analyze Timing<br/>Requirements]
    CheckMeds -->|No| Simple[Simple Reminder]
    
    Analyze --> MedGemma[MedGemma: Create<br/>Optimal Schedule]
    MedGemma --> Validate{Medically<br/>Safe?}
    
    Validate -->|Yes| Simplify[Generate Clear<br/>Instructions]
    Validate -->|No| Doctor[Flag for<br/>Doctor Review]
    
    Simplify --> Execute[Update Schedule +<br/>Send to Patient]
    Execute --> Monitor[Monitor Adherence]
    Monitor --> Learn[Update Success Metrics]
    
    style Start fill:#FFE4B5
    style MedGemma fill:#FFD700
    style Execute fill:#87CEEB
    style Learn fill:#DDA0DD
```

---

## Scenario 2: Supplement Interference

**Trigger:** `action="skipped"`, `reason="supplement_interference"`

### Patient Problem
Patient has excellent adherence (98%) but lab results are worsening. Recently started taking calcium and iron supplements that are blocking thyroid medication absorption by 50%.

### Workflow Flow

```mermaid
sequenceDiagram
    participant Patient
    participant UI
    participant Orch as Orchestrator
    participant Inv as Investigation Agent
    participant Rem as Remediation Agent
    participant Risk as Risk Assessment
    participant Exec as Execution Agent
    participant Learn as Learning Agent
    participant DB as Firebase
    participant AI as MedGemma

    Patient->>UI: Reports "Good adherence but labs worse"
    UI->>Orch: Patient Action Data
    
    rect rgb(200, 220, 240)
        Note over Orch,Inv: Agent 1: Investigation
        Orch->>Inv: Analyze Discrepancy
        Inv->>DB: Query adherence history
        DB-->>Inv: 98% adherence - excellent!
        Inv->>DB: Check recent changes
        DB-->>Inv: New supplements: Calcium + Iron<br/>Started 2 weeks ago
        Inv->>Inv: Timeline matches lab decline<br/>Hypothesis: Supplement interference
        Inv-->>Orch: Root Cause: "Supplement blocking medication"
    end
    
    rect rgb(255, 230, 200)
        Note over Orch,Rem: Agent 2: Remediation
        Orch->>Rem: Create Solution
        Rem->>AI: MedGemma consult:<br/>"Patient taking Levothyroxine + Calcium + Iron.<br/>Labs worsening despite adherence.<br/>Check interactions and suggest timing."
        AI-->>Rem: Analysis:<br/>- Calcium reduces thyroid absorption 50%<br/>- Iron reduces absorption 50%<br/>- Require 4+ hour separation<br/>Recommendation: Take supplements afternoon
        Rem-->>Orch: Timing adjustment plan
    end
    
    rect rgb(255, 200, 200)
        Note over Orch,Risk: Agent 3: Risk Assessment (CRITICAL)
        Orch->>Risk: Validate Intervention
        Risk->>AI: Confirm: Is 4-hour separation sufficient?<br/>Any other interactions?
        AI-->>Risk: Validated:<br/>- 4 hours prevents interference<br/>- Safe to continue all medications<br/>- Recheck labs in 6 weeks
        Risk-->>Orch: Approved with follow-up
    end
    
    rect rgb(230, 200, 250)
        Note over Orch,Exec: Agent 4: Execution
        Orch->>Exec: Implement Timing Change
        Exec->>DB: Update schedule:<br/>6:00 AM - Levothyroxine<br/>12:00 PM - Calcium + Iron
        Exec->>Patient: Education:<br/>"Your supplements were blocking thyroid medication.<br/>New schedule prevents interference."
        Exec->>DB: Schedule lab recheck in 6 weeks
        Exec-->>Orch: Schedule updated + patient educated
    end
    
    rect rgb(200, 240, 240)
        Note over Orch,Learn: Agent 5: Learning
        Orch->>Learn: Track Resolution
        Learn->>DB: Store supplement pattern
        Learn->>Learn: Knowledge:<br/>Calcium/Iron block levothyroxine<br/>4-hour separation effective<br/>Flag: Auto-detect supplement additions
        Learn-->>Orch: Pattern learned
    end
    
    Orch->>UI: Workflow Complete
    UI->>Patient: Show new schedule + follow-up date
```

### MedGemma Decision Flow

```mermaid
graph TD
    Start[Supplement Detected] --> MedGemma{MedGemma<br/>Analysis}
    
    MedGemma --> CheckInteraction[Check Drug-Supplement<br/>Interactions]
    
    CheckInteraction --> Severity{Interaction<br/>Severity}
    
    Severity -->|No Interaction| Continue[Continue Current<br/>Schedule]
    Severity -->|Timing Issue| Separate[Calculate Required<br/>Separation Time]
    Severity -->|Contraindicated| Stop[Recommend<br/>Discontinuation]
    
    Separate --> Schedule[Create New<br/>Schedule]
    Schedule --> Validate[MedGemma Validates<br/>Safety]
    
    Validate --> Implement[Implement +<br/>Educate Patient]
    Stop --> Doctor[Alert Doctor]
    
    Implement --> FollowUp[Schedule Lab<br/>Follow-Up]
    FollowUp --> Learn[Track Outcome]
    
    style Start fill:#FFE4B5
    style MedGemma fill:#FFD700
    style Severity fill:#FF6B6B
    style Implement fill:#90EE90
    style Learn fill:#DDA0DD
```

---

## Scenario 3: Patient Experiencing Side Effects

**Trigger:** `action="took"`, `reason="side_effects"`

### Workflow Flow

```mermaid
sequenceDiagram
    participant Patient
    participant UI
    participant Orch as Orchestrator
    participant Inv as Investigation Agent
    participant Rem as Remediation Agent
    participant Risk as Risk Assessment
    participant Exec as Execution Agent
    participant Learn as Learning Agent
    participant DB as Firebase
    participant AI as MedGemma

    Patient->>UI: Reports "Took but experiencing side effects"
    UI->>Orch: Patient Action Data + Symptoms
    
    rect rgb(200, 220, 240)
        Note over Orch,Inv: Agent 1: Investigation
        Orch->>Inv: Analyze Side Effect
        Inv->>DB: Query medication profile
        Inv->>DB: Check symptom history
        DB-->>Inv: Symptom: Nausea<br/>Timing: Morning dose
        Inv->>Inv: Pattern analysis:<br/>Always after breakfast
        Inv-->>Orch: Issue: "Interadherence - side effects"
    end
    
    rect rgb(255, 230, 200)
        Note over Orch,Rem: Agent 2: Remediation
        Orch->>Rem: Create Mitigation Plan
        Rem->>Rem: Design intervention:<br/>1. Take with food<br/>2. Adjust timing<br/>3. Monitor severity
        Rem-->>Orch: Intervention options
    end
    
    rect rgb(255, 200, 200)
        Note over Orch,Risk: Agent 3: Risk Assessment (CRITICAL)
        Orch->>Risk: Validate Intervention Safety
        Risk->>AI: MedGemma Consult:<br/>"Metformin + nausea + timing"
        AI->>AI: Medical reasoning:<br/>Check drug properties<br/>Analyze timing impact<br/>Assess severity
        AI-->>Risk: Medical Advice:<br/>"Take with food reduces nausea.<br/>Common side effect. Safe to continue."
        Risk->>Risk: Severity assessment:<br/>Mild - Can manage
        Risk-->>Orch: Approved with guidance
    end
    
    rect rgb(230, 200, 250)
        Note over Orch,Exec: Agent 4: Execution
        Orch->>Exec: Implement Guidance
        Exec->>Patient: "Take metformin with food<br/>to reduce nausea.<br/>Follow up in 3 days."
        Exec->>DB: Schedule follow-up check
        Exec->>DB: Update dosing instructions
        Exec-->>Orch: Patient notified + follow-up scheduled
    end
    
    rect rgb(200, 240, 240)
        Note over Orch,Learn: Agent 5: Learning
        Orch->>Learn: Track Side Effect Resolution
        Learn->>DB: Store side effect pattern
        Learn->>Learn: Update knowledge:<br/>Metformin + food = Less nausea<br/>Success rate: 85%
        Learn-->>Orch: Knowledge updated
    end
    
    Orch->>UI: Workflow Complete + Follow-up scheduled
    UI->>Patient: Show guidance + follow-up date
```

### MedGemma Decision Flow

```mermaid
graph TD
    Start[Side Effect Reported] --> MedGemma{MedGemma<br/>Consultation}
    
    MedGemma --> Analyze[Analyze:<br/>1. Drug properties<br/>2. Side effect severity<br/>3. Timing factors]
    
    Analyze --> Severity{Severity<br/>Assessment}
    
    Severity -->|Mild| Manage[Self-Management<br/>Guidance]
    Severity -->|Moderate| Consult[Suggest Telemedicine<br/>Consultation]
    Severity -->|Severe| Emergency[Urgent Medical<br/>Attention Alert]
    
    Manage --> Guidance[Provide Evidence-Based<br/>Mitigation Steps]
    Guidance --> Schedule[Schedule Follow-Up<br/>in 3 Days]
    
    Consult --> Provider[Connect to<br/>Healthcare Provider]
    Emergency --> Alert[Alert Emergency<br/>Contact]
    
    Schedule --> Monitor[Monitor Adherence<br/>& Symptoms]
    Provider --> Monitor
    Alert --> Monitor
    
    Monitor --> Learn[Update Side Effect<br/>Management Knowledge]
    
    style Start fill:#FFE4B5
    style MedGemma fill:#FFD700
    style Severity fill:#FF6B6B
    style Manage fill:#90EE90
    style Consult fill:#FFA500
    style Emergency fill:#FF0000
    style Learn fill:#DDA0DD
```

---

## Agent Interaction Matrix

```mermaid
graph LR
    subgraph "5-Agent System"
        INV[Investigation<br/>Agent]
        REM[Remediation<br/>Agent]
        RISK[Risk Assessment<br/>Agent]
        EXEC[Execution<br/>Agent]
        LEARN[Learning<br/>Agent]
    end
    
    subgraph "External Systems"
        DB[(Firebase<br/>Firestore)]
        AI[MedGemma<br/>AI]
        Patient[Patient<br/>Interface]
    end
    
    INV -.->|Patient Data| DB
    INV -->|Findings| REM
    REM -->|Solutions| RISK
    RISK -.->|Medical Validation| AI
    RISK -->|Approved Plans| EXEC
    EXEC -.->|Updates| DB
    EXEC -.->|Notifications| Patient
    EXEC -->|Outcomes| LEARN
    LEARN -.->|Insights| DB
    LEARN -.->|Pattern Updates| INV
    
    style INV fill:#2196F3
    style REM fill:#FF9800
    style RISK fill:#F44336
    style EXEC fill:#9C27B0
    style LEARN fill:#00BCD4
    style AI fill:#FFD700
```

---

## Scenario 4: Side Effect Healing Tracker (with Vision)

**Trigger:** `action="side_effect"`, `reason="skin_rash"`, `image` field present

### Patient Problem
Patient develops allopurinol-induced rash (Day 3). Uncertain whether to continue or stop medication. Traditional approach: 60% discontinue unnecessarily. Solution: Daily photo monitoring with MedGemma Vision temporal analysis.

### Workflow Flow

```mermaid
sequenceDiagram
    participant Patient
    participant UI
    participant Orch as Orchestrator
    participant Inv as Investigation Agent
    participant Rem as Remediation Agent
    participant Risk as Risk Assessment (Vision)
    participant Exec as Execution Agent
    participant Learn as Learning Agent
    participant DB as Firebase
    participant Vision as MedGemma Vision API

    Patient->>UI: Reports "Rash - should I stop?" + uploads Day 3 photo
    UI->>Orch: Patient Action Data with image

    rect rgb(200, 220, 240)
        Note over Orch,Inv: Agent 1: Investigation
        Orch->>Inv: Analyze Side Effect Report
        Inv->>DB: Query medication history
        DB-->>Inv: Allopurinol 300mg, started 3 days ago
        Inv->>Inv: Detects: Side effect with baseline image (Day 3)<br/>Pattern: Visual monitoring candidate
        Inv-->>Orch: Issue: "Allopurinol rash - requires visual tracking"
    end

    rect rgb(255, 230, 200)
        Note over Orch,Rem: Agent 2: Remediation
        Orch->>Rem: Create Monitoring Protocol
        Rem->>Rem: Proposes:<br/>- Daily photo check-ins (9 AM)<br/>- Antihistamine for symptom relief<br/>- 48-72 hour observation period<br/>- Escalation criteria defined
        Rem-->>Orch: Daily photo monitoring protocol
    end

    rect rgb(255, 200, 200)
        Note over Orch,Risk: Agent 3: Risk Assessment with Vision
        Orch->>Risk: Validate Safety + Analyze Image
        Risk->>Risk: Detects image field → activates vision mode
        Risk->>Vision: MedGemma Vision API call:<br/>"Analyze Day 3 baseline rash photo:<br/>Assess severity, lesion count, redness,<br/>emergency signs"
        Vision-->>Risk: Baseline assessment:<br/>Lesion count: ~25 spots<br/>Redness: Moderate intensity<br/>Distribution: Arms and torso<br/>Severity: MILD urticarial rash<br/>Emergency signs: None detected<br/>Safe to monitor
        Risk-->>Orch: Approved for daily monitoring (Risk: Low-Medium)
    end

    rect rgb(230, 200, 250)
        Note over Orch,Exec: Agent 4: Execution
        Orch->>Exec: Implement Monitoring
        Exec->>DB: Store Day 3 baseline image
        Exec->>DB: Schedule daily photo reminders (9 AM)
        Exec->>Patient: Instructions:<br/>"Continue medication. Upload photo daily.<br/>Take antihistamine for itching.<br/>We'll track healing progress."
        Exec-->>Orch: Patient notified + monitoring active
    end

    rect rgb(200, 240, 240)
        Note over Orch,Learn: Agent 5: Learning
        Orch->>Learn: Initialize Tracking
        Learn->>DB: Store pattern: "allopurinol_rash_monitoring"<br/>Baseline: Day 3 image + assessment
        Learn-->>Orch: Learning initialized
    end

    Note over Patient,Vision: === Day 4 Follow-up ===

    Patient->>UI: Uploads Day 4 photo + notes "Slightly better"
    UI->>Orch: Patient Action Data (Day 4 image + previous Day 3)

    Orch->>Risk: Analyze Progression
    Risk->>Risk: Temporal comparison mode activated
    Risk->>Vision: MedGemma Vision API:<br/>"Compare Day 3 → Day 4:<br/>Assess healing progression"
    Vision-->>Risk: Temporal analysis:<br/>Lesion count: ~21 spots (-15%)<br/>Redness: Decreasing intensity<br/>Healing trend: IMPROVING<br/>Recommendation: Continue monitoring
    Risk-->>Orch: Healing trend: IMPROVING (Risk: Low)

    Orch->>Patient: "Great! Rash improving. Continue medication."

    Note over Patient,Vision: === Day 5 Second Follow-up ===

    Patient->>UI: Uploads Day 5 photo + notes "Much better!"
    UI->>Orch: Patient Action Data (Day 5 + Day 3, 4 history)

    Orch->>Risk: Final Progression Analysis
    Risk->>Vision: MedGemma Vision API:<br/>"Compare Day 3 → Day 4 → Day 5:<br/>Full temporal healing trajectory"
    Vision-->>Risk: Multi-day temporal analysis:<br/>Lesion count: ~15 spots (-38% from Day 3)<br/>Redness: Significantly decreased<br/>Healing trajectory: CLEAR IMPROVEMENT<br/>Prediction: Resolving, continue medication
    Risk-->>Orch: Healing trajectory: RESOLVING (Risk: Low)

    Orch->>Exec: Update Treatment Plan
    Exec->>Patient: "Rash resolving! Continue allopurinol.<br/>Check-in in 2 days."

    Orch->>Learn: Track Successful Outcome
    Learn->>DB: Pattern learned:<br/>"allopurinol_rash_benign_resolution"<br/>Image progression: Day 3-5 stored<br/>Outcome: Continued medication successfully

    Note over Patient,Vision: === Day 10 Final Outcome ===
    Patient->>Patient: Rash fully resolved
    Patient->>Patient: Continues allopurinol (gout controlled)
    Note over Patient: Avoided unnecessary discontinuation,<br/>gout flare, medication switch costs,<br/>and potential ED visit
```

### Key Visualization

```mermaid
graph LR
    Day3[Day 3: Baseline Photo<br/>25 lesions, moderate redness] -->|MedGemma Vision| Assessment3[Mild rash<br/>Safe to monitor]
    Day4[Day 4: Follow-up Photo<br/>21 lesions, less red] -->|Temporal Comparison| Assessment4[Improving -15%<br/>Continue]
    Day5[Day 5: Second Follow-up<br/>15 lesions, fading] -->|Multi-day Analysis| Assessment5[Resolving -38%<br/>Clear improvement]
    Assessment5 --> Outcome[Day 10: Fully healed<br/>Medication continued]
    
    style Day3 fill:#ffcccc
    style Day4 fill:#ffe6cc
    style Day5 fill:#e6ffcc
    style Outcome fill:#ccffcc
    style Assessment3 fill:#fff0b3
    style Assessment4 fill:#b3e6ff
    style Assessment5 fill:#b3ffb3
```

### Architecture Highlight: No New Agents Needed

```mermaid
graph TB
    subgraph "Existing 5-Agent System (Unchanged)"
        INV[Investigation Agent<br/>✓ Unchanged]
        REM[Remediation Agent<br/>✓ Unchanged]
        RISK[Risk Assessment Agent<br/>✅ +Vision capability]
        EXEC[Execution Agent<br/>✓ Unchanged]
        LEARN[Learning Agent<br/>✓ Unchanged]
    end
    
    Image[Image Field<br/>Optional] -->|If present| RISK
    RISK -->|Conditional call| Vision[MedGemma Vision API]
    
    Text[Text-Only<br/>Scenarios 1-3] --> RISK
    RISK -->|Standard path| MedGemma[MedGemma Text API]
    
    style RISK fill:#ff6b6b
    style Vision fill:#ffd700
    style Image fill:#c7ecee
    style Text fill:#dfe6e9
    
    Note1[Only Risk Agent modified<br/>Single if-statement:<br/>if image field present → call vision API<br/>else → standard text analysis]
```

---

## Key Differences Across Scenarios

| Aspect | Scenario 1: Timing Conflict | Scenario 2: Supplement Interference | Scenario 3: Side Effects | Scenario 4: Healing Tracker |
|--------|---------------------------|-----------------------------------|--------------------------|----------------------------|
| **Trigger** | Skipped/Timing Conflict | Skipped/Supplement Interference | Took/Side Effects | Side Effect/Skin Rash |
| **Investigation Focus** | Medication timing complexity | Drug-supplement interactions | Medical symptoms | Visual monitoring baseline |
| **Remediation Type** | Optimized schedule | Timing separation | Dosing guidance | Photo monitoring protocol |
| **Risk Level** | Low | Medium | Variable (Mild-Severe) | Low-Medium (temporal tracking) |
| **MedGemma Role** | **Critical** (text) | **Critical** (text) | **Critical** (text) | **Critical** (vision) |
| **Modality** | Text-only | Text-only | Text-only | **Multimodal (image + text)** |
| **Temporal Tracking** | No | No | No | **Yes (Day 3→4→5)** |
| **Urgency** | Standard | Medium | Immediate | Daily follow-up |
| **Follow-Up** | Track adherence improvement | Lab recheck in 6 weeks | Symptom check in 3 days | Daily photo check-in |
| **Learning Focus** | Timing complexity patterns | Supplement interference patterns | Side effect management | **Visual healing patterns** |
| **Adherence Barrier** | "Too confusing to take" | "Taking it but not working" | "Can't tolerate it" | "Should I stop because of rash?" |
| **Innovation** | AI scheduling | AI drug interaction detection | AI severity assessment | **AI visual temporal analysis** |

---

## How to Use These Diagrams

### Viewing in VS Code
- Open this file and press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac) to see the rendered diagrams
- The Mermaid extension will render all diagrams automatically

### Viewing on GitHub
- All Mermaid diagrams render automatically when you view this file on GitHub

### Creating Custom Diagrams with Draw.io
1. Create a new file with `.drawio` extension (e.g., `custom_flow.drawio`)
2. VS Code will open the Draw.io editor
3. Design your diagram visually
4. Save and commit to repository

### Editing These Diagrams
- Mermaid diagrams are text-based - just edit the code blocks
- See [Mermaid documentation](https://mermaid.js.org/) for syntax reference
