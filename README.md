# LeetSquad

Group project for Agentic AI. We're building a green (eval) agent that benchmarks white (participant) agents on code generation capabilities using Leetcode problems.

**Important: All commands below assume you are running from the project's root directory.**

## 1. Setup

### 1.1. API Key Setup

Create a `.env` file under the project root directory and configure:

```
OPENAI_API_KEY="<your API key>"
```

Both the green and white agent use LLM. The default model is GPT-5-Mini.

### 1.2. Python Runtime Setup

```bash
# Create a virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

## 2. Usage

```bash
# 1. In a separate terminal, launch green agent
uv run main.py green

# 2. In a separate terminal, launch white agent (it won't start solving problems yet)
uv run main.py white

# 3. In a separate terminal, signal white agent to begin solving problems
uv run main.py start

# 4. Wait until completion and retrieve benchmarking results
uv run main.py report
```

Use `--help` to view the optional parameters for each command. You may also omit them to use the default settings.

**Note:**

- The full dataset contains 2,641 problems. By default, the green agent loads only the first 10. You can use `--limit-problems` to change this.
- By default, the white agent may invoke green-agent skills up to 25 times (enough for 10 problems). You can adjust this using `--max-turns`. As a rule of thumb: `max_turns = 2 × limit_problems + 5`

## 3. Agent Interaction

The communication between green and white agents is handled through A2A protocol. The green agent exposes the following skills:

### 3.1 Register

The white agent invokes this skill to register itself with the green agent. Upon receiving the request, the green agent will assign an ID to the white agent.

Input schema:

```json
{
    "skill": "register",
    "name": "<white agent name>"
}
```

Output schema:

```json
{
    "status": "accepted",
    "id": "<assigned ID>"
}
```

### 3.2 Distribute Problem

The white agent invokes this skill to get a new coding problem from the green agent.

Input schema:

```json
{
    "skill": "distribute_problem",
    "id": "<assigned ID>",
    "name": "<white agent name, acts as a simple auth token>"
}
```

Output schema:

```json
{
    "status": "accepted/rejected",
    "error": "<reason for rejection, only exists if rejected>",
    "problem_description": "<problem description>",
    "starter_code": "<starter code>",
    "entry_point": "<entry point in starter code>"
}
```

### 3.3 Process Answer

The white agent invokes this skill to submit its answer to the green agent. The green agent will then evaluate the generated code based on its correctness and readability, and record the scores.

Input schema:

```json
{
    "skill": "process_answer",
    "id": "<assigned ID>",
    "name": "<white agent name, acts as a simple auth token>",
    "solution": "<generated code>"
}
```

Output schema:

```json
{
    "status": "accepted/rejected",
    "error": "<reason for rejection, only exists if rejected>"
}
```

## 4. Scoring System

### 4.1 Score Calculation

The green agent evaluates solutions using a comprehensive scoring system that considers multiple factors:

| Component | Weight | Max Points | Description |
|-----------|--------|------------|-------------|
| **Correctness** | 40% | 100 | Percentage of test cases passed |
| **Time Complexity** | 30% | 100+ | Compared against optimal complexity (bonus for better) |
| **Space Complexity** | 15% | 100+ | Compared against optimal complexity (bonus for better) |
| **Readability** | 15% | 100 | LLM-judged code quality (normalized from 0-12 scale) |

Weighted scores are then multiplied by a difficulty factor:

| Difficulty | Multiplier |
|------------|------------|
| Easy | 1.0x |
| Medium | 1.5x |
| Hard | 2.0x |

In short:

- weighted_score = (correctness × 0.40) + (time × 0.30) + (space × 0.15) + (readability × 0.15)
- final_score = weighted_score × difficulty_multiplier


### 4.2 Leaderboard Metrics

The `report_results` command generates a leaderboard with:

- **raw_avg_score**: Average of `weighted_score` across all problems (before difficulty multiplier)
- **difficulty_adjusted_avg_score**: Average of `final_score` across all problems (with difficulty multiplier applied)
- **problems_attempted**: Number of problems the agent attempted
- **problems_solved**: Number of problems with 100% test accuracy

## 5. For Developers

```bash
# Lint code
uv run ruff check

# Auto-format code
uv run ruff format

# To add a new dependency, modify `pyproject.toml` file , then run
uv lock
uv sync

# Run test cases on green agent
uv run main.py test
```