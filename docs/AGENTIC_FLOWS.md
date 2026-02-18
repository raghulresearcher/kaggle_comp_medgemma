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

## Scenario 1: Patient Forgot Medication

**Trigger:** `action="skipped"`, `reason="forgot"`

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

    Patient->>UI: Reports "Skipped - Forgot"
    UI->>Orch: Patient Action Data
    
    rect rgb(200, 220, 240)
        Note over Orch,Inv: Agent 1: Investigation
        Orch->>Inv: Analyze Pattern
        Inv->>DB: Query adherence history
        DB-->>Inv: Last 30 days data
        Inv->>Inv: Detect pattern:<br/>Forgets Mondays
        Inv-->>Orch: Pattern: "Behavioral - Day of week"
    end
    
    rect rgb(255, 230, 200)
        Note over Orch,Rem: Agent 2: Remediation
        Orch->>Rem: Create Solution
        Rem->>Rem: Design intervention:<br/>Earlier reminder on Mondays
        Rem-->>Orch: Intervention Plan
    end
    
    rect rgb(255, 200, 200)
        Note over Orch,Risk: Agent 3: Risk Assessment
        Orch->>Risk: Validate Safety
        Risk->>AI: Check timing change safety
        AI-->>Risk: Safe - No drug interactions
        Risk-->>Orch: Approved (Risk: Low)
    end
    
    rect rgb(230, 200, 250)
        Note over Orch,Exec: Agent 4: Execution
        Orch->>Exec: Implement Solution
        Exec->>DB: Update reminder schedule
        Exec->>Patient: Notification: "Adjusted your Monday reminder"
        Exec-->>Orch: Executed successfully
    end
    
    rect rgb(200, 240, 240)
        Note over Orch,Learn: Agent 5: Learning
        Orch->>Learn: Track Outcome
        Learn->>DB: Store intervention details
        Learn->>Learn: Pattern type: Behavioral<br/>Success rate: 78%
        Learn-->>Orch: Learning complete
    end
    
    Orch->>UI: Workflow Complete
    UI->>Patient: Show summary
```

### Decision Points

```mermaid
graph TD
    Start[Patient Skipped: Forgot] --> CheckPattern{Pattern<br/>Detected?}
    CheckPattern -->|Yes| Behavioral[Behavioral Pattern:<br/>Day of Week]
    CheckPattern -->|No| General[General Support]
    
    Behavioral --> CreatePlan[Create Targeted<br/>Reminder Adjustment]
    General --> BasicPlan[Send Encouragement]
    
    CreatePlan --> ValidateRisk{Risk<br/>Assessment}
    ValidateRisk -->|Low Risk| Execute[Execute Change]
    ValidateRisk -->|High Risk| HumanReview[Flag for<br/>Human Review]
    
    Execute --> Monitor[Monitor Adherence]
    Monitor --> Learn[Update Success Metrics]
    
    style Start fill:#FFE4B5
    style Behavioral fill:#90EE90
    style Execute fill:#87CEEB
    style Learn fill:#DDA0DD
```

---

## Scenario 2: Patient Ran Out of Medication

**Trigger:** `action="skipped"`, `reason="ran_out"`

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

    Patient->>UI: Reports "Skipped - Ran Out"
    UI->>Orch: Patient Action Data
    
    rect rgb(200, 220, 240)
        Note over Orch,Inv: Agent 1: Investigation
        Orch->>Inv: Analyze Supply Issue
        Inv->>DB: Query medication inventory
        Inv->>DB: Check refill history
        DB-->>Inv: Last refill: 25 days ago<br/>Supply should last 30 days
        Inv->>Inv: Pattern: Runs out early<br/>Possible adherence gap
        Inv-->>Orch: Root Cause: "Supply management issue"
    end
    
    rect rgb(255, 230, 200)
        Note over Orch,Rem: Agent 2: Remediation
        Orch->>Rem: Create Supply Solution
        Rem->>Rem: Plan intervention:<br/>1. Refill reminder at 5 days left<br/>2. Setup auto-refill
        Rem-->>Orch: Multi-step intervention plan
    end
    
    rect rgb(255, 200, 200)
        Note over Orch,Risk: Agent 3: Risk Assessment
        Orch->>Risk: Validate Urgency
        Risk->>AI: Check medication criticality
        AI-->>Risk: Critical medication<br/>Gap risk: High
        Risk-->>Orch: Urgent action required
    end
    
    rect rgb(230, 200, 250)
        Note over Orch,Exec: Agent 4: Execution
        Orch->>Exec: Execute Urgently
        Exec->>DB: Find nearest pharmacy
        Exec->>Patient: "Pharmacy ABC has your Rx<br/>Ready in 2 hours"
        Exec->>DB: Enable auto-refill at 7 days
        Exec-->>Orch: Actions completed
    end
    
    rect rgb(200, 240, 240)
        Note over Orch,Learn: Agent 5: Learning
        Orch->>Learn: Track Supply Pattern
        Learn->>DB: Update patient profile:<br/>"Requires early refill alerts"
        Learn->>Learn: Adjust future thresholds
        Learn-->>Orch: Profile updated
    end
    
    Orch->>UI: Workflow Complete
    UI->>Patient: Show refill options
```

### Decision Tree

```mermaid
graph TD
    Start[Patient Ran Out] --> CheckHistory{Previous<br/>Ran Out<br/>Events?}
    CheckHistory -->|First Time| OneTime[One-time Issue]
    CheckHistory -->|Recurring| Pattern[Supply Pattern]
    
    OneTime --> BasicRefill[Send Refill Reminder]
    Pattern --> Investigate[Deep Investigation]
    
    Investigate --> FindCause{Root Cause?}
    FindCause -->|Forgets to Refill| AutoRefill[Enable Auto-Refill]
    FindCause -->|Financial| Assistance[Connect to Assistance Programs]
    FindCause -->|Pharmacy Issues| ChangePharmacy[Suggest Pharmacy Change]
    
    AutoRefill --> Implement[Implement Solution]
    Assistance --> Implement
    ChangePharmacy --> Implement
    
    Implement --> Monitor[Monitor Next Cycle]
    Monitor --> Learn[Update Success Metrics]
    
    style Start fill:#FFE4B5
    style Pattern fill:#FFB6C1
    style Implement fill:#87CEEB
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

| Aspect | Scenario 1: Forgot | Scenario 2: Ran Out | Scenario 3: Side Effects |
|--------|-------------------|---------------------|--------------------------|
| **Trigger** | Skipped/Forgot | Skipped/Ran Out | Took/Side Effects |
| **Investigation Focus** | Behavioral patterns | Supply management | Medical symptoms |
| **Remediation Type** | Timing adjustment | Refill automation | Dosing guidance |
| **Risk Level** | Low | Medium-High | Variable (Mild-Severe) |
| **MedGemma Role** | Optional | Optional | **Critical** |
| **Urgency** | Standard | High | Immediate |
| **Follow-Up** | Track adherence | Monitor next refill | Symptom check in 3 days |
| **Learning Focus** | Behavior patterns | Supply patterns | Side effect management |

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
