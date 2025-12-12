import asyncio
import json
import logging
import os
import re

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
import requests

from .a2a_util import send_message

from .agent import CodingEvaluationAgent


logger = logging.getLogger(__name__)

class CodingEvaluationAgentExecutor(AgentExecutor):
    """
    Executor class for the CodingEvaluationAgent.

    This class bridges the A2A agent execution framework with the green agent's
    core evaluation logic. It receives A2A user requests, parses the skill invocation,
    delegates the request to the appropriate method on CodingEvaluationAgent, and
    returns the result to the event queue.
    """

    def __init__(self, green_agent_port, **benchmarking_kwargs):
        """
        Constructor args are used directly to initialize BenchmarkingManager
        """
        CodingEvaluationAgent.initialize_manager(**benchmarking_kwargs)
        self.agent = CodingEvaluationAgent()
        # Code below is a hacky way to retrieve the actual green agent URL that looks
        # something like https://cloudrun_host/to_agent/8358dd168ea74b3583bb3232c96ed371
        # The white agent won't be able to call green agent without the ID part
        cloudrun_host = os.environ.get("CLOUDRUN_HOST")
        if cloudrun_host:
            base_url = f"https://{cloudrun_host}"
            resp = requests.get(f"{base_url}/agents")
            resp.raise_for_status()
            agents = resp.json()
            for _, agent in agents.items():  # will only have one agent
                self.green_agent_url = agent["url"]
        else:
            # for local run, use localhost
            self.green_agent_url = "http://localhost:9999"

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        message = context.get_user_input()
        input = {}
        try:
            input = json.loads(message)
        except json.JSONDecodeError as e:
            # message sent by AgentBeats isn't json, so this chunk will be executed
            if message and parse_tags(message).get("white_agent_url"):
                # for each white agent URL, invoke 'start_solving' and provide the
                # green agent's own URL for callback
                # TODO: implement a loop
                white_agent_url = parse_tags(message).get("white_agent_url")
                await send_message(white_agent_url, json.dumps(
                    {
                        "skill": "start_solving", 
                        "green_agent_url": self.green_agent_url,
                    }
                ))
                logger.info(f"Invoked white agent at {white_agent_url}")
                logger.info("The white agents have 3 minutes before results are reported")
                # Code below will keep AgentBeats assessment running for 3 minutes.
                # After 3 minutes, the green agent will report results to AgentBeats
                # and the assessement ends automatically.
                await asyncio.sleep(180)  
                result = await self.agent.report_results(input)
            else:
                result = json.dumps(
                    {
                        "status": "rejected",
                        "error": (
                            "Does not match AgentBeats startup string. "
                            "Expect <white_agent_url>...</white_agent_url>"
                        ),
                    }
                )
            await event_queue.enqueue_event(new_agent_text_message(result))
            return

        # messages sent by white agents will be valid json
        skill = input.get("skill")
        match skill:
            case "register":
                result = await self.agent.register(input)
            case "distribute_problem":
                result = await self.agent.distribute_problem(input)
            case "process_answer":
                result = await self.agent.process_answer(input)
            case "report_results":
                # convenience skill for getting results, shouldn't be used by white agents
                result = await self.agent.report_results(input)
            case _:
                result = json.dumps({"status": "rejected", "error": "Invalid skill"})

        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass


def parse_tags(str_with_tags: str) -> dict[str, str]:
    """the target str contains tags in the format of <tag_name> ... </tag_name>, parse them out and return a dict"""

    tags = re.findall(r"<(.*?)>(.*?)</\1>", str_with_tags, re.DOTALL)
    return {tag: content.strip() for tag, content in tags}
