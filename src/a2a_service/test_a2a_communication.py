"""Test script to verify A2A communication between white agent and green agent."""

import asyncio
import json
from a2a import A2AClient


async def test_white_agent():
    """Test the white agent's solve_problem skill."""

    print("\n" + "=" * 60)
    print("Testing White Agent (LeetCode Solver)")
    print("=" * 60)

    # Create client to connect to white agent
    client = A2AClient(agent_url="http://localhost:8001")

    # Test problem
    problem_description = """
    Given an array of integers nums and an integer target, return indices of the
    two numbers such that they add up to target.

    You may assume that each input would have exactly one solution, and you may
    not use the same element twice.

    Example:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    """

    try:
        # Call the solve_problem skill
        response = await client.call_skill(
            skill_name="solve_problem",
            parameters={
                "problem_description": problem_description,
                "problem_id": "1_two_sum",
                "difficulty": "Easy"
            }
        )

        print("\nWhite Agent Response:")
        print(json.dumps(response, indent=2))

        return response

    except Exception as e:
        print(f"\nError calling white agent: {str(e)}")
        return None


async def test_green_agent_complexity(solution_code: str):
    """Test the green agent's evaluate_complexity skill."""

    print("\n" + "=" * 60)
    print("Testing Green Agent - Complexity Analysis")
    print("=" * 60)

    # Create client to connect to green agent
    client = A2AClient(agent_url="http://localhost:8002")

    try:
        # Call the evaluate_complexity skill
        response = await client.call_skill(
            skill_name="evaluate_complexity",
            parameters={
                "solution_code": solution_code,
                "problem_id": "1_two_sum"
            }
        )

        print("\nGreen Agent Complexity Response:")
        print(json.dumps(response, indent=2))

        return response

    except Exception as e:
        print(f"\nError calling green agent (complexity): {str(e)}")
        return None


async def test_green_agent_readability(solution_code: str):
    """Test the green agent's evaluate_readability skill."""

    print("\n" + "=" * 60)
    print("Testing Green Agent - Readability Analysis")
    print("=" * 60)

    # Create client to connect to green agent
    client = A2AClient(agent_url="http://localhost:8002")

    try:
        # Call the evaluate_readability skill
        response = await client.call_skill(
            skill_name="evaluate_readability",
            parameters={
                "solution_code": solution_code,
                "problem_id": "1_two_sum"
            }
        )

        print("\nGreen Agent Readability Response:")
        print(json.dumps(response, indent=2))

        return response

    except Exception as e:
        print(f"\nError calling green agent (readability): {str(e)}")
        return None


async def test_green_agent_full_evaluation(solution_code: str):
    """Test the green agent's evaluate_solution skill (full evaluation)."""

    print("\n" + "=" * 60)
    print("Testing Green Agent - Full Evaluation")
    print("=" * 60)

    # Create client to connect to green agent
    client = A2AClient(agent_url="http://localhost:8002")

    try:
        # Call the evaluate_solution skill
        response = await client.call_skill(
            skill_name="evaluate_solution",
            parameters={
                "solution_code": solution_code,
                "problem_id": "1_two_sum"
            }
        )

        print("\nGreen Agent Full Evaluation Response:")
        print(json.dumps(response, indent=2))

        return response

    except Exception as e:
        print(f"\nError calling green agent (full evaluation): {str(e)}")
        return None


async def test_full_workflow():
    """Test the complete workflow: White agent solves, Green agent evaluates."""

    print("\n" + "=" * 80)
    print("FULL WORKFLOW TEST: White Agent Solves -> Green Agent Evaluates")
    print("=" * 80)

    # Step 1: White agent generates solution
    white_response = await test_white_agent()

    if not white_response or not white_response.get("success"):
        print("\nWorkflow failed: Could not get solution from white agent")
        return

    solution_code = white_response.get("solution_code")

    if not solution_code:
        print("\nWorkflow failed: No solution code in white agent response")
        return

    # Add delay to ensure servers are ready
    await asyncio.sleep(1)

    # Step 2: Green agent evaluates the solution
    await test_green_agent_full_evaluation(solution_code)

    print("\n" + "=" * 80)
    print("WORKFLOW TEST COMPLETED")
    print("=" * 80)


async def main():
    """Run all A2A communication tests."""

    print("\n" + "=" * 80)
    print("A2A COMMUNICATION TEST SUITE")
    print("=" * 80)
    print("\nMake sure both servers are running:")
    print("  White Agent: http://localhost:8001")
    print("  Green Agent: http://localhost:8002")
    print("\nStarting tests in 3 seconds...")
    await asyncio.sleep(3)

    # Run the full workflow test
    await test_full_workflow()


if __name__ == "__main__":
    asyncio.run(main())
