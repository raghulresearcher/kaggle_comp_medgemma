"""
Test script for Scenario 3: Side Effects
Tests the full workflow with action="took" and reason="side_effects"
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.agent_init import initialize_agents
from backend.agents.base_agent import orchestrator

def test_scenario3():
    """Test scenario 3: patient took medication but experiencing side effects"""
    
    print("=" * 80)
    print("Testing Scenario 3: Side Effects")
    print("=" * 80)
    
    # Initialize agents
    print("\n1. Initializing agent system...")
    initialize_agents()
    print(f"   ✓ Initialized {len(orchestrator.agents)} agents")
    
    # Prepare test data
    test_data = {
        "patient_id": "p003",
        "action": "took",
        "reason": "side_effects",
        "medication_id": "med_metformin_500mg",
        "notes": "Feeling nauseous after taking",
        "timestamp": "2026-02-18T10:30:00.000Z"
    }
    
    print("\n2. Test data:")
    print(f"   Patient: {test_data['patient_id']}")
    print(f"   Action: {test_data['action']}")
    print(f"   Reason: {test_data['reason']}")
    print(f"   Notes: {test_data['notes']}")
    
    # Execute workflow
    print("\n3. Executing workflow...")
    print(f"   Routing: action='{test_data['action']}', reason='{test_data['reason']}'")
    
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
        
        # Show error if any
        if agent_status == "error":
            error_msg = agent_result.get('error', 'Unknown error')
            print(f"      ERROR: {error_msg}")
    
    # Show what Investigation found
    inv_agent = next((a for a in agents_executed if a.get('agent') == 'investigation'), None)
    if inv_agent:
        print(f"\n   Investigation Findings:")
        inv_result = inv_agent.get('result', {})
        print(f"   - Root Cause: {inv_result.get('root_cause')}")
        print(f"   - Recommendations: {inv_result.get('recommendations', [])[:2]}")
    
    # Show what Remediation proposed
    rem_agent = next((a for a in agents_executed if a.get('agent') == 'remediation'), None)
    if rem_agent:
        print(f"\n   Remediation Interventions:")
        rem_result = rem_agent.get('result', {})
        interventions = rem_result.get('interventions', [])
        for intervention in interventions[:3]:
            print(f"   - Type: {intervention.get('type')}, Action: {intervention.get('action')}")
    
    # Verify expected behavior
    print("\n5. Validation:")
    expected_agents = 5
    actual_agents = len(agents_executed)
    
    if actual_agents == expected_agents:
        print(f"   ✅ PASS: All {expected_agents} agents executed")
    else:
        print(f"   ❌ FAIL: Expected {expected_agents} agents, got {actual_agents}")
        print(f"   Missing agents: Investigation, Remediation, Risk Assessment, Execution, Learning")
        print(f"   Actual agents: {[a.get('agent') for a in agents_executed]}")
    
    # Check if MedGemma was consulted
    risk_agent = next((a for a in agents_executed if a.get('agent') == 'risk_assessment'), None)
    if risk_agent:
        medgemma_consulted = risk_agent.get('result', {}).get('medgemma_consulted', False)
        print(f"   MedGemma consulted: {'✅ Yes' if medgemma_consulted else '❌ No'}")
        
        # Show risk agent details for debugging
        print(f"\n   Risk Agent Details:")
        risk_result = risk_agent.get('result', {})
        print(f"   - Approved: {risk_result.get('approved')}")
        print(f"   - Overall Risk: {risk_result.get('overall_risk_level')}")
        print(f"   - Intervention Assessments: {len(risk_result.get('intervention_assessments', []))}")
        
        # Show reasoning
        if 'reasoning' in risk_result:
            print(f"\n   Risk Agent Reasoning (first 5 steps):")
            for step in risk_result['reasoning'][:5]:
                print(f"     {step}")
    
    print("\n" + "=" * 80)
    return result

if __name__ == "__main__":
    try:
        result = test_scenario3()
        
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
