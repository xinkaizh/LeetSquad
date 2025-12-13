"""CLI entry point for LeetBench."""

import asyncio
import logging
import typer

from pydantic_settings import BaseSettings

from src.green_agent.tools import report_results
from src.green_agent.tools import start_server as start_green_server
from src.green_agent.tools import test_green_agent
from src.white_agent.tools import start_server as start_white_server
from src.white_agent.tools import start_solving


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
# Turn down logging from noisy libraries
logging.getLogger("a2a").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)


class LeetSettings(BaseSettings):
    # the values will be overriden by AgentBeats during runtime
    role: str = "unspecified"
    host: str = "127.0.0.1"
    agent_port: int = 9000


app = typer.Typer(
    help="Agentified Leetcode Solver Benchmark - Standardized agent assessment framework"
)


@app.command(name="run")
def run():
    """Launcher for AgentBeats"""
    settings = LeetSettings()
    if settings.role == "green":
        start_green_server(
            host=settings.host,
            port=settings.agent_port,
            skip_tests=False,
            skip_llm_judge=False,
            limit_problems=10,
        )
    elif settings.role == "white":
        start_white_server(
            host=settings.host,
            port=settings.agent_port,
            name="LeetCodeSolver",
            max_turns=25,
            trace=False,
        )
    else:
        raise ValueError(
            f"Unknown role: {settings.role}. Set ROLE env variable to 'green' or 'white'"
        )


@app.command()
def green(
    limit_problems: int = typer.Option(
        10, "--limit-problems", help="number of problems to use"
    ),
):
    """Launch a green agent"""
    start_green_server(
        "0.0.0.0",
        9999,
        skip_tests=False,
        skip_llm_judge=False,
        llm_judge_model="gpt-5-mini",
        llm_provider="openai",
        limit_problems=limit_problems,
    )


@app.command()
def white(
    name: str = typer.Option("LeetCodeSolver", "--name", help="white agent name"),
    max_turns: int = typer.Option(
        25, "--max-turns", help="max number of times for tool calls"
    ),
    trace: bool = typer.Option(False, "--trace", help="whether to use cloud trace"),
):
    """Launch a white agent"""
    start_white_server(
        "0.0.0.0",
        9998,
        name=name,
        max_turns=max_turns,
        trace=trace,
    )


@app.command()
def report():
    """Retrieve benchmarking results"""
    asyncio.run(report_results())


@app.command()
def test():
    """Run predefiend test cases on green agent"""
    asyncio.run(test_green_agent("localhost", 9999))


@app.command()
def start():
    """Signal the white agent to start solving"""
    asyncio.run(start_solving("http://localhost:9998", "http://localhost:9999"))


if __name__ == "__main__":
    app()
