# Unit Tests

Comprehensive unit tests for MedAdhere Pro agent system.

## Structure

```
tests/unit_test/
├── __init__.py              # Package marker
├── conftest.py              # Pytest fixtures and configuration
├── test_investigation_agent.py   # Investigation Agent tests
├── test_remediation_agent.py     # Remediation Agent tests
├── test_risk_agent.py            # Risk Assessment Agent tests
├── test_execution_agent.py       # Execution Agent tests (to be added)
├── test_learning_agent.py        # Learning Agent tests (to be added)
└── test_medgemma_hf.py           # MedGemma wrapper tests
```

## Running Tests

### Run all unit tests:
```bash
pytest tests/unit_test/
```

### Run specific test file:
```bash
pytest tests/unit_test/test_investigation_agent.py
```

### Run with coverage:
```bash
pytest tests/unit_test/ --cov=backend/agents --cov-report=html
```

### Run with verbose output:
```bash
pytest tests/unit_test/ -v
```

## Test Categories

### Agent Tests
- **Initialization**: Verify agents initialize with correct properties
- **Input Validation**: Test required input fields and error handling
- **Processing Logic**: Test core agent functionality
- **Output Format**: Verify output structure and required fields
- **Reasoning Steps**: Ensure reasoning traces are captured

### MedGemma Tests
- **Text-only calls**: Standard medical reasoning
- **Multimodal calls**: Image + text analysis
- **Temporal tracking**: Multi-day image comparison
- **Error handling**: API failures and retries

## Fixtures (conftest.py)

Available fixtures for all tests:
- `sample_patient_data`: Standard patient action data
- `sample_adherence_logs`: Historical adherence records
- `sample_investigation_output`: Investigation agent results
- `sample_remediation_output`: Remediation agent results
- `mock_medgemma_response`: Mocked MedGemma API response

## Writing New Tests

Example test structure:
```python
class TestYourAgent:
    def test_initialization(self):
        agent = YourAgent()
        assert agent is not None
        assert hasattr(agent, 'llm')
    
    def test_process_with_valid_input(self, sample_data):
        agent = YourAgent()
        result = agent.process(sample_data)
        assert "expected_field" in result
```

## Mocking Guidelines

- Mock Firebase calls: `@patch('backend.agents.your_agent.adherence_service')`
- Mock MedGemma: `@patch('backend.agents.your_agent.MedGemmaHF')`
- Use `Mock()` for simple objects, `MagicMock()` for complex ones

## Coverage Goals

- **Target**: >80% code coverage for agents
- **Focus**: Core business logic, error handling, edge cases
- **Exclude**: Firebase config, external API wrappers

## CI/CD Integration

These tests run automatically on:
- Pull requests to main branch
- Commits to main branch
- Manual workflow dispatch

Test results are reported in GitHub Actions.
