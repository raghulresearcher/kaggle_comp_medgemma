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

## Key Differences Across Scenarios

| Aspect | Scenario 1: Timing Conflict | Scenario 2: Supplement Interference | Scenario 3: Side Effects |
|--------|---------------------------|-----------------------------------|--------------------------|
| **Trigger** | Skipped/Timing Conflict | Skipped/Supplement Interference | Took/Side Effects |
| **Investigation Focus** | Medication timing complexity | Drug-supplement interactions | Medical symptoms |
| **Remediation Type** | Optimized schedule | Timing separation | Dosing guidance |
| **Risk Level** | Low | Medium | Variable (Mild-Severe) |
| **MedGemma Role** | **Critical** | **Critical** | **Critical** |
| **Urgency** | Standard | Medium | Immediate |
| **Follow-Up** | Track adherence improvement | Lab recheck in 6 weeks | Symptom check in 3 days |
| **Learning Focus** | Timing complexity patterns | Supplement interference patterns | Side effect management |
| **Adherence Barrier** | "Too confusing to take" | "Taking it but not working" | "Can't tolerate it" |

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
