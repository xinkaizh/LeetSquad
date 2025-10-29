"""Green Agent A2A Server - LeetCode Solution Judge/Evaluator."""

from a2a import A2AServer
from judge.llm_judge import LLMJudge


def create_green_agent_server():
    """Create the green agent (judge) A2A server with evaluation skills."""

    server = A2AServer(name="leetcode_judge")

    # Initialize the LLM judge
    judge = LLMJudge(verbose=True)

    # Register evaluate_complexity skill
    @server.skill(
        name="evaluate_complexity",
        description="Analyze the time and space complexity of a solution",
        parameters={
            "solution_code": {
                "type": "string",
                "description": "The Python solution code to evaluate"
            },
            "problem_id": {
                "type": "string",
                "description": "The LeetCode problem ID (optional, for logging)"
            }
        }
    )
    async def evaluate_complexity(solution_code: str, problem_id: str = "unknown"):
        """Evaluate the time and space complexity of a solution."""

        print(f"[Green Agent] Received complexity evaluation request for: {problem_id}")
        print(f"[Green Agent] Code length: {len(solution_code)} characters")

        try:
            # Use the existing LLM judge to analyze complexity
            complexity_analysis = judge.analyze_complexity(solution_code)

            result = {
                "success": True,
                "problem_id": problem_id,
                "complexity_analysis": complexity_analysis,
                "message": "Complexity analysis completed successfully"
            }

            print(f"[Green Agent] Complexity analysis completed for {problem_id}")
            print(f"  Time: {complexity_analysis['time']['complexity']}")
            print(f"  Space: {complexity_analysis['space']['complexity']}")

            return result

        except Exception as e:
            print(f"[Green Agent] Error during complexity evaluation: {str(e)}")
            return {
                "success": False,
                "problem_id": problem_id,
                "error": str(e),
                "message": "Complexity analysis failed"
            }

    # Register evaluate_readability skill
    @server.skill(
        name="evaluate_readability",
        description="Analyze the readability and code quality of a solution",
        parameters={
            "solution_code": {
                "type": "string",
                "description": "The Python solution code to evaluate"
            },
            "problem_id": {
                "type": "string",
                "description": "The LeetCode problem ID (optional, for logging)"
            }
        }
    )
    async def evaluate_readability(solution_code: str, problem_id: str = "unknown"):
        """Evaluate the readability and code quality of a solution."""

        print(f"[Green Agent] Received readability evaluation request for: {problem_id}")
        print(f"[Green Agent] Code length: {len(solution_code)} characters")

        try:
            # Use the existing LLM judge to analyze readability
            readability_analysis = judge.analyze_readability(solution_code)

            result = {
                "success": True,
                "problem_id": problem_id,
                "readability_analysis": readability_analysis,
                "message": "Readability analysis completed successfully"
            }

            print(f"[Green Agent] Readability analysis completed for {problem_id}")
            print(f"  Overall Score: {readability_analysis['overall']}/15")

            return result

        except Exception as e:
            print(f"[Green Agent] Error during readability evaluation: {str(e)}")
            return {
                "success": False,
                "problem_id": problem_id,
                "error": str(e),
                "message": "Readability analysis failed"
            }

    # Register combined evaluate_solution skill
    @server.skill(
        name="evaluate_solution",
        description="Perform complete evaluation (complexity + readability) of a solution",
        parameters={
            "solution_code": {
                "type": "string",
                "description": "The Python solution code to evaluate"
            },
            "problem_id": {
                "type": "string",
                "description": "The LeetCode problem ID (optional, for logging)"
            }
        }
    )
    async def evaluate_solution(solution_code: str, problem_id: str = "unknown"):
        """Perform complete evaluation of a solution (complexity + readability)."""

        print(f"[Green Agent] Received full evaluation request for: {problem_id}")
        print(f"[Green Agent] Code length: {len(solution_code)} characters")

        try:
            # Analyze both complexity and readability
            complexity_analysis = judge.analyze_complexity(solution_code)
            readability_analysis = judge.analyze_readability(solution_code)

            result = {
                "success": True,
                "problem_id": problem_id,
                "evaluation": {
                    "complexity": complexity_analysis,
                    "readability": readability_analysis
                },
                "message": "Complete evaluation finished successfully"
            }

            print(f"[Green Agent] Complete evaluation finished for {problem_id}")
            print(f"  Time Complexity: {complexity_analysis['time']['complexity']}")
            print(f"  Space Complexity: {complexity_analysis['space']['complexity']}")
            print(f"  Readability Score: {readability_analysis['overall']}/15")

            return result

        except Exception as e:
            print(f"[Green Agent] Error during solution evaluation: {str(e)}")
            return {
                "success": False,
                "problem_id": problem_id,
                "error": str(e),
                "message": "Solution evaluation failed"
            }

    return server
