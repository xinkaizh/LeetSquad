import asyncio
import json
import httpx
import uuid


from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    Part,
    TextPart,
    MessageSendParams,
    Message,
    Role,
    SendMessageRequest,
    SendMessageResponse,
)

async def get_agent_card(url: str) -> AgentCard | None:
    httpx_client = httpx.AsyncClient()
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=url)
    card: AgentCard | None = await resolver.get_agent_card()
    return card

async def send_message(
    url, message, task_id=None, context_id=None
) -> SendMessageResponse:
    card = await get_agent_card(url)
    httpx_client = httpx.AsyncClient(timeout=120.0)
    client = A2AClient(httpx_client=httpx_client, agent_card=card)

    message_id = uuid.uuid4().hex
    params = MessageSendParams(
        message=Message(
            role=Role.user,
            parts=[Part(TextPart(text=message))],
            message_id=message_id,
            task_id=task_id,
            context_id=context_id,
        )
    )
    request_id = uuid.uuid4().hex
    req = SendMessageRequest(id=request_id, params=params)
    response = await client.send_message(request=req)
    return response
    
if __name__ == "__main__":
    response = asyncio.run(send_message("https://web-production-593845.up.railway.app", json.dumps({"skill": "report_results"})))
    print(response)
