# LeetSquad A2A Service - Quick Start Guide

## Overview

The A2A (Agent-to-Agent) service enables communication between two agents:
- **White Agent** (Port 8001): Solves LeetCode problems
- **Green Agent** (Port 8002): Evaluates solutions for complexity and readability

## Prerequisites

```bash
# Install python-a2a library (assumed already installed)
pip install python-a2a

# Ensure AWS credentials are configured for the judge
# The judge uses AWS Bedrock with Claude 3.5 Haiku
```

## Quick Start

### Step 1: Start the Servers

```bash
# From the project root directory
python start_a2a_servers.py
```

This will start both servers:
```
White Agent (LeetCode Solver) - Port: 8001
Green Agent (Judge/Evaluator) - Port: 8002
```

### Step 2: Run Tests (in a separate terminal)

```bash
# From the project root directory
python test_a2a.py
```

## What's Implemented

### White Agent ([src/white_agent/white_agent_server.py](src/white_agent/white_agent_server.py))

**Status**: Placeholder implementation

**Skill**: `solve_problem`
- **Input**:
  - `problem_description` (string): The LeetCode problem description
  - `problem_id` (string): Problem ID like "1_two_sum"
  - `difficulty` (string): Easy, Medium, or Hard
- **Output**:
  - `success` (bool)
  - `problem_id` (string)
  - `solution_code` (string): Python solution code
  - `message` (string)

**Current Behavior**: Returns a hardcoded two-sum solution for testing

**TODO**: Integrate with LLM to generate actual solutions

### Green Agent ([src/a2a_service/green_agent_server.py](src/a2a_service/green_agent_server.py))

**Status**: Fully functional, integrated with existing LLMJudge

**Skills**:

1. `evaluate_complexity` - Analyzes time/space complexity
   - **Input**: `solution_code`, `problem_id` (optional)
   - **Output**: Complexity analysis with Big-O notation and justifications

2. `evaluate_readability` - Analyzes code quality
   - **Input**: `solution_code`, `problem_id` (optional)
   - **Output**: Scores (0-3) for 5 categories + overall score (0-15)

3. `evaluate_solution` - Complete evaluation
   - **Input**: `solution_code`, `problem_id` (optional)
   - **Output**: Both complexity and readability analyses

## Example Usage

### Using the A2A Client

```python
import asyncio
from a2a import A2AClient

async def example():
    # Step 1: Get solution from white agent
    white_client = A2AClient(agent_url="http://localhost:8001")

    solution_response = await white_client.call_skill(
        skill_name="solve_problem",
        parameters={
            "problem_description": """
            Given an array of integers nums and an integer target,
            return indices of the two numbers that add up to target.
            """,
            "problem_id": "1_two_sum",
            "difficulty": "Easy"
        }
    )

    print(f"Solution: {solution_response['solution_code']}")

    # Step 2: Evaluate with green agent
    green_client = A2AClient(agent_url="http://localhost:8002")

    eval_response = await green_client.call_skill(
        skill_name="evaluate_solution",
        parameters={
            "solution_code": solution_response["solution_code"],
            "problem_id": "1_two_sum"
        }
    )

    # Print evaluation results
    complexity = eval_response["evaluation"]["complexity"]
    readability = eval_response["evaluation"]["readability"]

    print(f"\nTime Complexity: {complexity['time']['complexity']}")
    print(f"Space Complexity: {complexity['space']['complexity']}")
    print(f"Readability Score: {readability['overall']}/15")

asyncio.run(example())
```

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    LeetSquad A2A Service                     │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────┐         ┌─────────────────────────┐
│   White Agent           │         │   Green Agent           │
│   (Solver)              │         │   (Judge)               │
│                         │         │                         │
│   localhost:8001        │ ◄─────► │   localhost:8002        │
│                         │   A2A   │                         │
│   Skill:                │ Protocol│   Skills:               │
│   • solve_problem       │         │   • evaluate_complexity │
│                         │         │   • evaluate_readability│
│   Status: Placeholder   │         │   • evaluate_solution   │
│                         │         │                         │
│   Returns: Hardcoded    │         │   Status: Fully Working │
│   two-sum solution      │         │   Uses: AWS Bedrock +   │
│                         │         │         Claude 3.5 Haiku│
└─────────────────────────┘         └─────────────────────────┘
```

## File Structure

```
LeetSquad/
├── start_a2a_servers.py           # Start both servers
├── test_a2a.py                    # Run tests
├── A2A_QUICKSTART.md              # This file
└── src/
    ├── a2a_service/
    │   ├── __init__.py
    │   ├── main_server.py         # Server coordinator
    │   ├── green_agent_server.py  # Green agent A2A server
    │   ├── test_a2a_communication.py  # Test suite
    │   └── README.md              # Detailed documentation
    ├── white_agent/
    │   ├── white_agent_server.py  # White agent A2A server
    │   └── ...
    └── judge/
        └── llm_judge.py           # LLM judge (used by green agent)
```

## Expected Test Output

When you run `python test_a2a.py`, you should see:

```
====================================================================
A2A COMMUNICATION TEST SUITE
====================================================================

Make sure both servers are running:
  White Agent: http://localhost:8001
  Green Agent: http://localhost:8002

Starting tests in 3 seconds...

================================================================================
FULL WORKFLOW TEST: White Agent Solves -> Green Agent Evaluates
================================================================================

============================================================
Testing White Agent (LeetCode Solver)
============================================================

White Agent Response:
{
  "success": true,
  "problem_id": "1_two_sum",
  "solution_code": "def twoSum(nums, target):\n...",
  "message": "Solution generated successfully (placeholder)"
}

============================================================
Testing Green Agent - Full Evaluation
============================================================

Green Agent Full Evaluation Response:
{
  "success": true,
  "problem_id": "1_two_sum",
  "evaluation": {
    "complexity": {
      "time": { "complexity": "O(n)", ... },
      "space": { "complexity": "O(n)", ... }
    },
    "readability": {
      "naming": { "score": 3, "justification": "..." },
      ...
      "overall": 12
    }
  }
}
```

## Next Steps

To make the white agent fully functional:

1. **Implement LLM Integration**:
   - Complete [src/white_agent/llm/bedrock.py](src/white_agent/llm/bedrock.py)
   - Use the existing `BedrockClient` or create a new provider

2. **Implement Solution Generation**:
   - Update [src/white_agent/skills/solve_leetcode.py](src/white_agent/skills/solve_leetcode.py)
   - Use the `PromptEngineer` class from [src/white_agent/llm/prompt.py](src/white_agent/llm/prompt.py)

3. **Update White Agent Server**:
   - Replace placeholder in [src/white_agent/white_agent_server.py](src/white_agent/white_agent_server.py)
   - Call the actual solution generation skill

4. **Add Test Case Validation**:
   - Integrate with [src/accuracy_check/run_testcases.py](src/accuracy_check/run_testcases.py)
   - Validate solutions before sending to judge

## Troubleshooting

**Servers won't start**:
```bash
# Check if ports are in use
netstat -an | findstr "8001"
netstat -an | findstr "8002"

# Verify python-a2a is installed
pip show python-a2a
```

**Green agent fails**:
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify Bedrock access to Claude 3.5 Haiku in us-west-2
aws bedrock list-foundation-models --region us-west-2
```

**Import errors**:
```bash
# Run from project root
cd C:\Users\cathe\Desktop\LeetSquad
python start_a2a_servers.py
```

## Support

For more details, see:
- [src/a2a_service/README.md](src/a2a_service/README.md) - Detailed A2A documentation
- [README.md](README.md) - Project overview
- python-a2a documentation

## Summary

You now have:
- ✅ A2A service structure created
- ✅ White agent server with placeholder solve_problem skill
- ✅ Green agent server with full evaluation capabilities
- ✅ Test suite for verifying A2A communication
- ✅ Easy-to-use launcher scripts
- 📝 White agent needs LLM integration (TODO)

Start the servers and run the tests to see the A2A communication in action!
