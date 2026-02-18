# MedAdhere Pro - Test Suite

## Running Tests

### From Project Root:

```bash
# Scenario 1: Patient Forgot Medication
python tests/test_scenario1.py

# Scenario 2: Patient Ran Out of Medication
python tests/test_scenario2.py

# Scenario 3: Patient Experiencing Side Effects
python tests/test_scenario3.py
```

## Test Scenarios

- **Scenario 1**: Tests forgot medication workflow (5 agents)
- **Scenario 2**: Tests ran out workflow (5 agents)
- **Scenario 3**: Tests side effects workflow (5 agents)

All scenarios should execute all 5 agents:
1. Investigation Agent
2. Remediation Agent
3. Risk Assessment Agent
4. Execution Agent
5. Learning Agent
