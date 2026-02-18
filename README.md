# MedAdhere Pro - AI-Powered Medication Adherence System

## Overview

MedAdhere Pro is an intelligent medication adherence assistant that leverages multi-agent AI workflows with Google's MedGemma model to help patients take their medications correctly through proactive intervention, personalized solutions, and continuous learning.

### The Problem
- 50% of patients don't take medications as prescribed
- $300 billion annual healthcare costs from non-adherence
- 125,000+ preventable deaths per year in the US

### Our Solution
An autonomous AI care team powered by 5 specialized agents that observe, analyze, act, and learn - demonstrating improved patient adherence outcomes.

## Key Features

### 1. Proactive Intervention
- Continuous monitoring of adherence patterns
- Predictive analysis to identify problems before they escalate
- Automatic adjustment of reminders based on patient behavior

### 2. Multi-Agent Workflow (5 Specialized Agents)
- **Investigation Agent** - Analyzes patterns and root causes
- **Remediation Agent** - Creates personalized solutions
- **Risk Assessment Agent** - Validates safety with MedGemma
- **Execution Agent** - Implements changes automatically
- **Learning Agent** - Improves system over time

### 3. Medical Intelligence
- Powered by google/medgemma-1.5-4b-it
- Real-time safety validation
- Drug interaction checking
- Evidence-based interventions

## Architecture

```
Web UI (HTML/JavaScript)
    ↓ REST API + WebSocket
Firebase (Firestore + Cloud Functions)
    ↓ Agent Orchestration
Flask Backend (Agent Engine)
    ↓ Medical Reasoning
MedGemma (Hugging Face Inference Endpoint - google/medgemma-1.5-4b-it)
```

## Quick Start

### Prerequisites
- Python 3.12+
- Firebase account with Firestore enabled
- Hugging Face API key with MedGemma endpoint access

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/raghulresearcher/kaggle_comp_medgemma.git
cd kaggle_comp_medgemma
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

5. **Start the backend:**
```bash
python backend/app.py
```

6. **Start the frontend:**
```bash
cd public
python -m http.server 3000
```

Access the UI at: http://localhost:3000

## Project Structure

```
medadhere-agentic-clean/
├── backend/              # Flask backend application
│   ├── agents/          # Agent system and orchestration
│   ├── config.py        # Configuration management
│   ├── app.py           # API endpoints
│   └── firebase_client.py  # Firebase integration
├── public/              # Web frontend
│   └── index.html       # User interface
├── tests/               # Test scenarios
├── docs/                # Documentation
│   ├── ARCHITECTURE.md  # System architecture
│   ├── KNOWLEDGE_TRANSFER.md  # Technical details
│   └── MVP_PLAN.md      # Development plan
├── functions/           # Firebase Cloud Functions
└── requirements.txt     # Python dependencies
```

## Demo Scenarios

### Scenario 1: Medication Timing Conflict
Patient confused about when to take multiple medications (thyroid, calcium, metformin) → System detects timing complexity → MedGemma creates optimized schedule → Patient receives clear instructions

### Scenario 2: Supplement Interference
Patient has good adherence but labs worsening → System detects new calcium/iron supplements → MedGemma identifies absorption interference → Adjusts timing to prevent interaction

### Scenario 3: Side Effects
Patient reports nausea → MedGemma validates severity → Suggests taking with food → Follows up in 3 days

## Testing

Run the included test scenarios:

```bash
python tests/test_scenario1.py  # Medication timing conflict
python tests/test_scenario2.py  # Supplement interference
python tests/test_scenario3.py  # Side effects
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Current system design and components
- [Agentic Flows](docs/AGENTIC_FLOWS.md) - Multi-agent workflow diagrams
- [Mobile Architecture](docs/MOBILE_ARCHITECTURE.md) - Production mobile-first architecture with external integrations

## Technology Stack

- **Backend:** Python 3.12, Flask, Flask-SocketIO
- **AI Model:** google/medgemma-1.5-4b-it via Hugging Face
- **Database:** Firebase Firestore
- **Frontend:** HTML5, JavaScript, TailwindCSS
- **Orchestration:** Custom multi-agent system

## License

[Add your license here]

## Contact

For questions or collaboration opportunities, please open an issue on GitHub.

