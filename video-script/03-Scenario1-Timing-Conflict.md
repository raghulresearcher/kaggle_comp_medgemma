# Section 3: Scenario 1 - Timing Conflict (1.5 minutes)

## Objective
Demonstrate full 5-agent workflow solving complex medication timing problem. Show how MedGemma provides medical reasoning that simple apps cannot.

---

## Visual Sequence

### Part 1: Patient Context (0:00-0:20)

**On Screen:**
- Web UI (http://localhost:3000)
- Scenario 1 card highlighted
- Patient profile visible

**Text Overlay:**
```
Sarah, 62 years old
Diagnoses: Hypothyroid, Diabetes, Osteoporosis
Medications: Levothyroxine, Metformin, Calcium
Problem: Skips thyroid med 3x/week
Reason: Confused about timing
```

**Voiceover:**
```
"Sarah's problem is complex. Her thyroid medication must be taken 
on an empty stomach. Her calcium supplement blocks thyroid absorption. 
And her diabetes medication needs food.

She's not forgetting—she's confused. Generic reminders won't help."
```

### Part 2: Agent Workflow (0:20-1:10)

**On Screen:**
- Click "Start Workflow" button
- Show real-time agent execution panel
- Highlight each agent as it runs
- Show agent reasoning/output

**Visual Flow:**
```
[Click Start Workflow]
↓
🔍 Investigation Agent (running...)
  ✓ Detected: 3 medications with timing conflicts
  ✓ Pattern: Thyroid doses skipped on days with calcium
  ✓ Root cause: Unclear timing requirements
↓
💡 Remediation Agent (running...)
  ✓ Consulting MedGemma for schedule optimization...
  ✓ Created: Optimized 3-medication schedule
    • 7:00 AM - Levothyroxine (empty stomach)
    • 8:30 AM - Breakfast + Metformin
    • 12:00 PM - Lunch + Calcium (4 hours after thyroid)
↓
⚠️ Risk Assessment Agent (running...)
  ✓ MedGemma validation: APPROVED
  ✓ No drug interactions detected
  ✓ Timing meets pharmacokinetic requirements
  ✓ Safe to implement
↓
⚙️ Execution Agent (running...)
  ✓ Updated reminder schedule
  ✓ Sent educational message to patient
  ✓ Scheduled follow-up in 7 days
↓
📚 Learning Agent (running...)
  ✓ Pattern logged: Timing complexity → Non-adherence
  ✓ Will monitor effectiveness
```

**Voiceover:**
```
"Watch the agents work together.

The Investigation Agent detects the pattern—thyroid doses are 
skipped when calcium is scheduled nearby.

The Remediation Agent consults MedGemma to create an optimized 
schedule: thyroid medication first thing in the morning on an 
empty stomach, then breakfast with diabetes medication ninety 
minutes later, and calcium at lunch—four hours after the thyroid 
dose.

The Risk Assessment Agent validates this with MedGemma's medical 
AI—confirming no interactions and proper timing windows.

The Execution Agent implements the new schedule and sends Sarah 
clear instructions.

And the Learning Agent logs this pattern to improve future 
recommendations."
```

### Part 3: MedGemma Insight (1:10-1:30)

**On Screen:**
- Zoom into Risk Agent's MedGemma consultation
- Show actual MedGemma reasoning (example)

**Text Overlay:**
```
MedGemma Reasoning:
─────────────────────
"Levothyroxine absorption reduced 20-60% by 
calcium carbonate. Requires 4-hour separation. 
Optimal timing: levothyroxine 30-60 min before 
first meal. Metformin with food reduces GI side 
effects. Schedule is safe and optimal."
```

**Voiceover:**
```
"This is medical reasoning a general AI cannot provide. MedGemma 
understands absorption windows, drug interactions, and clinical 
best practices—ensuring Sarah's new schedule is both safe and 
effective."
```

---

## Voiceover Script (Complete)

```
[Explanatory, building excitement]

"Sarah's problem is complex. Her thyroid medication must be taken 
on an empty stomach. Her calcium supplement blocks thyroid absorption. 
And her diabetes medication needs food.

She's not forgetting—she's confused. Generic reminders won't help.

Watch the agents work together.

The Investigation Agent detects the pattern—thyroid doses are 
skipped when calcium is scheduled nearby.

The Remediation Agent consults MedGemma to create an optimized 
schedule: thyroid medication first thing in the morning on an 
empty stomach, then breakfast with diabetes medication ninety 
minutes later, and calcium at lunch—four hours after the thyroid 
dose.

The Risk Assessment Agent validates this with MedGemma's medical 
AI—confirming no interactions and proper timing windows.

The Execution Agent implements the new schedule and sends Sarah 
clear instructions.

And the Learning Agent logs this pattern to improve future 
recommendations.

This is medical reasoning a general AI cannot provide. MedGemma 
understands absorption windows, drug interactions, and clinical 
best practices—ensuring Sarah's new schedule is both safe and 
effective."
```

**Word Count:** 168 words  
**Timing:** 85-90 seconds

---

## Production Notes

### Screen Recording Steps

1. **Open browser** to http://localhost:3000
2. **Click Scenario 1** card
3. **Click "Start Workflow"** button
4. **Record agent execution panel** (real-time updates)
5. **Wait for all 5 agents** to complete (~85 seconds)
6. **Click into Risk Agent** details to show MedGemma response

### Visual Effects

- **Agent Progress:** Highlight active agent with glow/pulse
- **Checkmarks:** Animate ✓ appearing as tasks complete
- **Text Speed:** Sync voiceover with agent completion
- **Zoom Effects:** Zoom into MedGemma response for emphasis

### Text Overlays

```
Timing Conflict Detected
↓
Medical AI Analysis
↓
Optimized Schedule Created
↓
Safety Validated by MedGemma
↓
Automatically Implemented
```

---

## Key Technical Points to Highlight

1. ✅ **Pattern Detection** - Not just reminders, actual analysis
2. ✅ **MedGemma Consultation** - Medical-grade reasoning
3. ✅ **Pharmacokinetic Timing** - 4-hour separation, absorption windows
4. ✅ **Safety Validation** - Every change checked by medical AI
5. ✅ **Automatic Implementation** - No manual work required
6. ✅ **Learning** - System improves from each case

---

## Expected Agent Output (Reference)

Based on actual test scenario output:

```
Investigation Agent Result:
{
  "findings": "Patient skipping levothyroxine 3x/week. Pattern correlates with calcium supplement timing.",
  "root_cause": "Timing confusion between thyroid medication (empty stomach), calcium (blocks absorption), and metformin (with food)",
  "medications_analyzed": ["levothyroxine_50mcg", "calcium_500mg", "metformin_500mg"]
}

Remediation Agent Result:
{
  "intervention": "Optimized medication schedule",
  "schedule": {
    "7:00 AM": "Levothyroxine 50mcg (empty stomach, 30-60 min before food)",
    "8:30 AM": "Breakfast + Metformin 500mg",
    "12:00 PM": "Lunch + Calcium 500mg (4 hrs after levothyroxine)"
  },
  "medgemma_used": true
}

Risk Agent Result:
{
  "safety_status": "APPROVED",
  "medgemma_consulted": true,
  "reasoning": "Schedule meets all pharmacokinetic requirements. No drug interactions with proposed timing.",
  "confidence": "high"
}
```

---

## Backup Plan

If live demo fails:
- [ ] Pre-record scenario execution
- [ ] Have static screenshots of each agent step
- [ ] Prepare narration that works with static images

---

## Transition to Scenario 2

**Visual:** Fade out from Scenario 1 results  
**New Visual:** Scenario 2 card appears  
**Text Overlay:** "Scenario 2: Supplement Interference"  
**Voiceover:** "Here's an even more subtle problem..."
