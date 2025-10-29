# A2A Service for LeetSquad

This directory contains the Agent-to-Agent (A2A) communication service that enables the white agent (LeetCode solver) and green agent (judge/evaluator) to communicate using the python-a2a library.

## Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│   White Agent       │         │   Green Agent       │
│  (LeetCode Solver)  │         │   (Judge/Evaluator) │
│                     │         │                     │
│  Port: 8001         │ ◄─────► │  Port: 8002         │
│                     │   A2A   │                     │
│  Skills:            │         │  Skills:            │
│  - solve_problem    │         │  - evaluate_complexity
│                     │         │  - evaluate_readability
│                     │         │  - evaluate_solution │
└─────────────────────┘         └─────────────────────┘
```

## Components

### 1. White Agent Server ([white_agent_server.py](../white_agent/white_agent_server.py))

**Location**: `src/white_agent/white_agent_server.py`

**Skills**:
- `solve_problem`: Generates a solution for a LeetCode problem
  - Input: problem_description, problem_id, difficulty
  - Output: solution_code

**Current Status**: Placeholder implementation (returns a simple two-sum solution)

**TODO**: Integrate with LLM provider to generate actual solutions

### 2. Green Agent Server ([green_agent_server.py](green_agent_server.py))

**Location**: `src/a2a_service/green_agent_server.py`

**Skills**:
- `evaluate_complexity`: Analyzes time and space complexity
  - Input: solution_code, problem_id (optional)
  - Output: complexity_analysis (time, space, justifications)

- `evaluate_readability`: Analyzes code quality and readability
  - Input: solution_code, problem_id (optional)
  - Output: readability_analysis (scores for naming, structure, simplicity, idiomatic, comments)

- `evaluate_solution`: Performs complete evaluation (complexity + readability)
  - Input: solution_code, problem_id (optional)
  - Output: Complete evaluation with both analyses

**Current Status**: Fully integrated with existing LLMJudge class

### 3. Main Server ([main_server.py](main_server.py))

Coordinates and starts both agent servers concurrently.

### 4. Test Script ([test_a2a_communication.py](test_a2a_communication.py))

Comprehensive test suite to verify A2A communication between agents.

## Installation

Ensure you have the python-a2a library installed:

```bash
pip install python-a2a
```

Also ensure you have AWS credentials configured for the green agent (judge) to work properly.

## Usage

### Starting the A2A Service

Run both servers from the project root:

```bash
python -m src.a2a_service.main_server
```

This will start:
- White Agent on `http://localhost:8001`
- Green Agent on `http://localhost:8002`

### Running Tests

In a separate terminal (while servers are running):

```bash
python -m src.a2a_service.test_a2a_communication
```

### Manual Testing with A2A Client

```python
import asyncio
from a2a import A2AClient

async def test():
    # Connect to white agent
    white_client = A2AClient(agent_url="http://localhost:8001")

    # Request solution
    solution_response = await white_client.call_skill(
        skill_name="solve_problem",
        parameters={
            "problem_description": "Your problem description here",
            "problem_id": "1_two_sum",
            "difficulty": "Easy"
        }
    )

    # Connect to green agent
    green_client = A2AClient(agent_url="http://localhost:8002")

    # Evaluate solution
    eval_response = await green_client.call_skill(
        skill_name="evaluate_solution",
        parameters={
            "solution_code": solution_response["solution_code"],
            "problem_id": "1_two_sum"
        }
    )

    print(eval_response)

asyncio.run(test())
```

## Workflow

The typical workflow is:

1. **White Agent** receives a LeetCode problem and generates a solution
2. **Green Agent** receives the solution and evaluates it:
   - Analyzes time and space complexity using Claude 3.5 Haiku
   - Scores readability across 5 categories
   - Returns comprehensive evaluation results

## File Structure

```
src/
├── a2a_service/
│   ├── __init__.py
│   ├── main_server.py              # Main server coordinator
│   ├── green_agent_server.py       # Green agent A2A server
│   ├── test_a2a_communication.py   # Test suite
│   └── README.md                   # This file
├── white_agent/
│   └── white_agent_server.py       # White agent A2A server
└── judge/
    └── llm_judge.py                # LLM judge (used by green agent)
```

## Next Steps

To make the white agent fully functional:

1. Implement the LLM provider integration in `src/white_agent/llm/bedrock.py`
2. Implement the actual solution generation in `src/white_agent/skills/solve_leetcode.py`
3. Update the white agent server to use the real implementation instead of placeholders
4. Add test case validation before sending to green agent
5. Implement error handling and retry logic

## Troubleshooting

**Servers won't start**:
- Ensure python-a2a is installed: `pip install python-a2a`
- Check if ports 8001 and 8002 are available
- Verify Python version is compatible (>=3.14)

**Green agent evaluation fails**:
- Check AWS credentials are configured
- Verify AWS Bedrock access to Claude 3.5 Haiku
- Check the AWS region (default: us-west-2)

**Tests fail**:
- Ensure both servers are running before running tests
- Add more delay in the test script if needed
- Check server logs for error messages
