"""
Test script for Scenario 1: I Forgot
Tests the full workflow with action="skipped" and reason="forgot"
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.agent_init import initialize_agents
from backend.agents.base_agent import orchestrator

def test_scenario1():
    """Test scenario 1: patient forgot medication"""
    
    print("=" * 80)
    print("Testing Scenario 1: I Forgot")
    print("=" * 80)
    
    # Initialize agents
    print("\n1. Initializing agent system...")
    initialize_agents()
    print(f"   ✓ Initialized {len(orchestrator.agents)} agents")
    
    # Prepare test data
    test_data = {
        "patient_id": "p001",
        "action": "skipped",
        "reason": "forgot",
        "medication_id": "med_lisinopril_10mg",
        "notes": "Didn't see the reminder this morning",
        "timestamp": "2026-02-18T10:30:00.000Z"
    }
    
    print("\n2. Test data:")
    print(f"   Patient: {test_data['patient_id']}")
    print(f"   Action: {test_data['action']}")
    print(f"   Reason: {test_data['reason']}")
    print(f"   Notes: {test_data['notes']}")
    
    # Execute workflow
    print("\n3. Executing workflow...")
    result = orchestrator.route_patient_action(test_data)
    
    # Display results
    print("\n4. Workflow Results:")
    print(f"   Status: {result.get('state')}")
    print(f"   Workflow ID: {result.get('workflow_id')}")
    
    agents_executed = result.get('agents_executed', [])
    print(f"\n   Agents Executed: {len(agents_executed)}")
    
    for i, agent_result in enumerate(agents_executed, 1):
        agent_name = agent_result.get('agent', 'unknown')
        agent_status = agent_result.get('status', 'unknown')
        exec_time = agent_result.get('execution_time_ms', 0)
        print(f"   {i}. {agent_name.upper()}: {agent_status} ({exec_time}ms)")
    
    # Check MedGemma consultation
    risk_agent = next((a for a in agents_executed if a.get('agent') == 'risk_assessment'), None)
    if risk_agent:
        medgemma_consulted = risk_agent.get('result', {}).get('medgemma_consulted', False)
        print(f"\n   MedGemma consulted: {'✅ Yes' if medgemma_consulted else '❌ No'}")
    
    # Verify expected behavior
    print("\n5. Validation:")
    expected_agents = 5
    actual_agents = len(agents_executed)
    
    if actual_agents == expected_agents:
        print(f"   ✅ PASS: All {expected_agents} agents executed")
    else:
        print(f"   ❌ FAIL: Expected {expected_agents} agents, got {actual_agents}")
    
    print("\n" + "=" * 80)
    return result

if __name__ == "__main__":
    try:
        result = test_scenario1()
        
        # Exit with error code if not all 5 agents ran
        agents_count = len(result.get('agents_executed', []))
        if agents_count != 5:
            print(f"\nTest FAILED: Only {agents_count}/5 agents executed")
            sys.exit(1)
        else:
            print("\nTest PASSED: All 5 agents executed successfully")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
