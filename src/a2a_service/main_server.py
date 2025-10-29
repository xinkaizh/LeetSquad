"""Main A2A server that coordinates white agent and green agent communication."""

import asyncio
from a2a import A2AServer
from white_agent.white_agent_server import create_white_agent_server
from a2a_service.green_agent_server import create_green_agent_server


async def main():
    """Start both white agent and green agent A2A servers."""

    # Create server instances
    white_server = create_white_agent_server()
    green_server = create_green_agent_server()

    print("Starting A2A Service...")
    print("=" * 60)
    print("White Agent (LeetCode Solver) - Port: 8001")
    print("Green Agent (Judge/Evaluator) - Port: 8002")
    print("=" * 60)

    # Start both servers concurrently
    await asyncio.gather(
        white_server.start(host="localhost", port=8001),
        green_server.start(host="localhost", port=8002)
    )


if __name__ == "__main__":
    asyncio.run(main())
