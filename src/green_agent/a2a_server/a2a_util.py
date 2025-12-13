import httpx
import uuid

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    Part,
    TextPart,
    MessageSendParams,
    Message,
    Role,
    SendMessageRequest,
    SendMessageResponse,
)


async def send_message(
    url, message, task_id=None, context_id=None
) -> SendMessageResponse:
    """Util function for sending a message via A2A protocol"""
    httpx_client = httpx.AsyncClient(timeout=120.0)
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=url)
    card = await resolver.get_agent_card()

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
