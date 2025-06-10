#  Marketing Campaign Agent

A proof-of-concept LangChain/LangGraph project that simulates an autonomous AI agent capable of planning, forecasting, and reporting on a marketing campaign, based on mock product and sales data. 
---

##  Goal
To create a modular, always-on, agentic AI system that:
1. Receives a campaign goal 
2. Retrieves historical product and regional sales data
3. Plans an appropriate media/channel strategy
4. Forecasts campaign performance
5. Outputs a structured campaign brief
6. Allows for human review and overrides at key steps

---

##  Architecture Overview

### Agent Workflow (Orchestrated by LangGraph):
```
[User Goal]
   ↓
[Task Planner] → [Data Retriever] → [Channel Selector] → [Forecaster] → [Human Review] → [Reporter]
```

### Key Components
- **LangGraph**: Manages the flow of reasoning and tool use
- **LangChain**: Hosts LLM tools and routing
- **Python/LLM tools**:
  - `retriever.py`: Summarizes mock sales data
  - `planner.py`: Breaks high-level campaign goals into tasks
  - `channel_selector.py`: Chooses marketing channels based on product & region
  - `forecaster.py`: Simulates expected performance
  - `reporter.py`: Creates a markdown report
  - `human_review.py`: Prompts a human to approve or override the agent’s plan

---

##  Tech Stack
- Python 
- LangChain / LangGraph
- OpenAI or Anthropic LLM API
- Pandas for mock data manipulation

---

## 📁 Repo Structure
```
marketing-campaign-agent/
├── data/                  # Contains mock CSVs for product sales
├── langgraph_app/         # LangGraph orchestration logic
├── tools/                 # Tool implementations (retriever, planner, etc.)
├── ui/                    # Optional Streamlit app
├── tests/                 # Unit tests for tools
├── docs/                  # Diagrams and specs
├── .github/workflows/     # CI config (lint/tests)
├── requirements.txt
├── .env.template
└── README.md
```

---


##  Team Collaboration
- Feature branches and pull requests
- One tool per team member
- CI/CD checks on PR
- Main DAG lives in `langgraph_app/`

