# Section 5: Scenario 3 - Side Effects Management (1 minute)

## Objective
Demonstrate MedGemma's ability to validate side effect severity and provide evidence-based management strategies. Show how AI prevents unnecessary medication discontinuation.

---

## Visual Sequence

### Part 1: Patient Reports Side Effect (0:00-0:15)

**On Screen:**
- Scenario 3 card selected
- Patient profile: Maria

**Text Overlay:**
```
Maria, 45 years old
Diagnosis: Hypertension
Medication: Lisinopril 10mg daily
Problem: Persistent nausea after 2 weeks
Considering: Stopping medication
Risk: Blood pressure will spike
```

**Voiceover:**
```
"Maria started blood pressure medication two weeks ago. She's 
experiencing nausea and wants to stop taking it.

This is a critical moment—if she stops, her blood pressure will 
spike. But is the nausea dangerous, or can it be managed?"
```

### Part 2: MedGemma Safety Validation (0:15-0:45)

**On Screen:**
- Start workflow
- Show Investigation and Risk Agent working together
- Emphasize MedGemma consultation

**Visual Flow:**
```
🔍 Investigation Agent
  ✓ Side effect: Nausea (reported severity: 4/10)
  ✓ Duration: 2 weeks (persistent)
  ✓ Timing: Occurs 30-60 min after dose
  ✓ Taking medication: On empty stomach

⚠️ Risk Assessment Agent + MedGemma
  Consulting medical AI for safety assessment...
  
  MedGemma Analysis:
  ─────────────────
  SEVERITY: Mild (common ACE inhibitor side effect)
  
  MANAGEMENT OPTIONS:
  ✓ Take with food (reduces GI irritation)
  ✓ Switch to evening dose (sleep through peak)
  ✓ Monitor for 3 days
  
  RED FLAGS TO WATCH:
  ✗ Angioedema (swelling of face/tongue) → STOP IMMEDIATELY
  ✗ Severe dizziness/fainting → Call doctor
  ✗ Persistent dry cough → Consider ARB alternative
  
  RECOMMENDATION: Try with food before discontinuing
  SAFETY: Low risk. Nausea is manageable, not dangerous.
```

**Voiceover:**
```
"The Investigation Agent captures the details—nausea rated 
four out of ten, occurring after taking the medication on an 
empty stomach.

MedGemma evaluates the severity. It's a common, mild side effect—
not dangerous. The AI recommends taking the medication with food 
and monitoring for three days before considering alternatives.

Crucially, MedGemma also flags red flags to watch for—like 
facial swelling or severe dizziness—that would require immediate 
action."
```

### Part 3: Smart Management (0:45-1:00)

**On Screen:**
- Remediation, Execution, and Learning Agents complete
- Show proactive follow-up scheduled

**Visual Flow:**
```
💡 Remediation Agent
  ✓ Intervention: Take with food
  ✓ Education: "Nausea is common, usually resolves in 1-2 weeks"
  ✓ Alternative if persists: Switch to evening dose

⚙️ Execution Agent
  ✓ Updated instructions: "Take with breakfast or dinner"
  ✓ Scheduled 3-day check-in
  ✓ Red flag alert system activated

📚 Learning Agent
  ✓ Tracked: Side effect management success
  ✓ Pattern: Empty stomach → nausea (ACE inhibitors)
  ✓ Will suggest "with food" proactively for future patients
```

**Voiceover:**
```
"The system implements the change, schedules a proactive three-day 
follow-up, and learns from this case—future patients starting 
blood pressure medication will automatically get instructions 
to take it with food.

Maria stays on her medication, her blood pressure stays controlled, 
and she avoids an emergency room visit."
```

---

## Voiceover Script (Complete)

```
[Reassuring, clinical tone]

"Maria started blood pressure medication two weeks ago. She's 
experiencing nausea and wants to stop taking it.

This is a critical moment—if she stops, her blood pressure will 
spike. But is the nausea dangerous, or can it be managed?

The Investigation Agent captures the details—nausea rated 
four out of ten, occurring after taking the medication on an 
empty stomach.

MedGemma evaluates the severity. It's a common, mild side effect—
not dangerous. The AI recommends taking the medication with food 
and monitoring for three days before considering alternatives.

Crucially, MedGemma also flags red flags to watch for—like 
facial swelling or severe dizziness—that would require immediate 
action.

The system implements the change, schedules a proactive three-day 
follow-up, and learns from this case—future patients starting 
blood pressure medication will automatically get instructions 
to take it with food.

Maria stays on her medication, her blood pressure stays controlled, 
and she avoids an emergency room visit."
```

**Word Count:** 146 words  
**Timing:** 55-60 seconds

---

## Production Notes

### Key Visual Moments

1. **Decision Point:** Maria considering stopping medication (critical moment)
2. **Severity Assessment:** MedGemma distinguishing mild vs dangerous
3. **Red Flags List:** Show what WOULD require stopping (important safety message)
4. **Simple Solution:** "Take with food" - emphasizes practical, easy fix
5. **Proactive Follow-up:** Shows system continues caring

### Text Overlays

```
Common Question:
"Should I stop my medication?"

↓

AI Medical Assessment:
Severity: MILD (manageable)
Action: Try with food first

↓

Dangerous Signs to Watch:
⚠️ Face swelling → STOP
⚠️ Severe dizziness → Call doctor

↓

Proactive Follow-up in 3 Days
```

### Visual Effects

- **Severity Meter:** Show "4/10" nausea rating
- **Traffic Light System:** 
  - 🟢 Green: Manageable (current situation)
  - 🟡 Yellow: Monitor (check-in scheduled)
  - 🔴 Red: Alert (red flags listed)
- **Calendar:** Show 3-day follow-up scheduled

---

## Key Messages

1. ✅ **Clinical Judgment** - MedGemma distinguishes mild vs severe
2. ✅ **Evidence-Based Management** - "Take with food" is standard practice
3. ✅ **Safety Monitoring** - Red flags identified and watched
4. ✅ **Prevents Discontinuation** - 50-70% of patients stop meds in first 6 months
5. ✅ **Proactive Care** - Follow-up scheduled automatically
6. ✅ **System Learning** - Future patients benefit

---

## Why This Scenario Matters

**Clinical Significance:**
- 50-70% of patients discontinue medications due to side effects
- Most side effects are mild and manageable
- Discontinuation leads to disease progression and complications
- ER visits for uncontrolled BP cost $1,000-5,000

**AI Value Proposition:**
- MedGemma provides clinical judgment (mild vs severe)
- Prevents unnecessary medication changes
- Reduces healthcare costs (avoided ER visit)
- Improves long-term outcomes (continued treatment)

---

## Expected Agent Output (Reference)

```
Investigation Agent Result:
{
  "side_effect": "Nausea",
  "severity": "4/10 (patient-reported)",
  "duration": "2 weeks (persistent)",
  "timing": "30-60 minutes after dose",
  "context": "Taking on empty stomach",
  "patient_intent": "Considering discontinuation"
}

Risk Assessment Agent + MedGemma:
{
  "severity_assessment": "Mild - common ACE inhibitor side effect",
  "is_dangerous": false,
  "management_strategy": "Take with food to reduce GI irritation",
  "monitoring_plan": "3-day check-in to assess improvement",
  "red_flags": [
    "Angioedema (facial/tongue swelling) - STOP IMMEDIATELY",
    "Severe orthostatic hypotension - Call physician",
    "Persistent dry cough - Consider ARB alternative"
  ],
  "recommendation": "Continue medication with modification",
  "safety_status": "APPROVED for continued use with food"
}

Execution Agent Result:
{
  "changes_made": [
    "Updated instructions: Take with breakfast or dinner",
    "Scheduled 3-day follow-up check-in",
    "Red flag monitoring activated"
  ],
  "patient_education": "Nausea typically resolves within 1-2 weeks. Taking with food usually helps."
}
```

---

## Alternative Endings (Choose One)

### Ending A: Success (Recommended)
"Maria's nausea resolved after taking medication with food. She stayed on treatment and her BP is now 118/78."

### Ending B: Learning Focus
"Even if Maria needed a different medication, the system learned from this case—improving recommendations for thousands of future patients."

### Ending C: Transition to Impact
"Three scenarios. Three lives improved. Now let's look at the bigger picture."

**Recommended:** Ending C (transitions smoothly to impact section)

---

## Transition to Impact Section

**Visual:** Fade from Maria's outcome  
**New Visual:** Map of United States with data points  
**Text Overlay:** "The Impact: Scaling Nationwide"  
**Voiceover:** "Three patients. Three success stories. Now imagine this at scale..."
