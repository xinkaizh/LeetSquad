"""
Multi-agent controller server for AgentBeats.

This controller provides the /to_agent/<agent-id> routing pattern
that AgentBeats expects, while proxying to standalone agent servers.
"""

import logging
import uuid
from typing import Dict

import httpx
import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask

logger = logging.getLogger(__name__)


class AgentController:
    """Controller that routes requests to registered agents"""

    def __init__(self):
        self.agents: Dict[str, Dict[str, str]] = {}
        self.app = FastAPI(title="LeetSquad Agent Controller")
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()

    def register_agent(self, name: str, url: str) -> str:
        """
        Register an agent with the controller.
        
        Args:
            name: Agent name/role (e.g., "green", "white")
            url: Backend URL where the agent server is running
            
        Returns:
            agent_id: Generated agent ID
        """
        agent_id = str(uuid.uuid4()).replace("-", "")
        self.agents[agent_id] = {
            "name": name,
            "url": url.rstrip("/"),
        }
        logger.info(f"Registered agent '{name}' with ID {agent_id} at {url}")
        return agent_id

    def _setup_routes(self):
        """Setup controller routes"""
        
        @self.app.get("/")
        async def root():
            """Controller info endpoint"""
            return {
                "controller": "LeetSquad Agent Controller",
                "agent_count": len(self.agents),
                "agents": {
                    agent_id: {"name": data["name"]}
                    for agent_id, data in self.agents.items()
                }
            }
        
        @self.app.get("/agents")
        async def list_agents():
            """List all registered agents"""
            return {
                "agents": [
                    {
                        "id": agent_id,
                        "name": data["name"],
                        "url": f"/to_agent/{agent_id}",
                    }
                    for agent_id, data in self.agents.items()
                ]
            }
        
        @self.app.api_route(
            "/to_agent/{agent_id}/{path:path}",
            methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
        )
        async def proxy_to_agent(agent_id: str, path: str, request: Request):
            """Proxy requests to the appropriate agent backend"""
            
            if agent_id not in self.agents:
                raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
            
            backend_url = self.agents[agent_id]["url"]
            target_url = f"{backend_url}/{path}"
            
            # Forward the request
            async with httpx.AsyncClient(timeout=300.0) as client:
                try:
                    # Get request body if present
                    body = await request.body()
                    
                    # Forward headers (excluding host)
                    headers = dict(request.headers)
                    headers.pop("host", None)
                    
                    # Make the proxied request
                    response = await client.request(
                        method=request.method,
                        url=target_url,
                        headers=headers,
                        content=body,
                        params=request.query_params,
                    )
                    
                    # Return the response
                    return Response(
                        content=response.content,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.headers.get("content-type"),
                    )
                    
                except httpx.RequestError as e:
                    logger.error(f"Error proxying to {target_url}: {e}")
                    raise HTTPException(
                        status_code=502,
                        detail=f"Error connecting to agent backend: {str(e)}"
                    )


def start_controller(
    host: str = "0.0.0.0",
    port: int = 8000,
    green_agent_url: str = "http://localhost:9999",
    white_agent_url: str = "http://localhost:9998",
):
    """
    Start the agent controller server.
    
    Args:
        host: Host to bind to
        port: Port to listen on
        green_agent_url: URL of the green agent backend
        white_agent_url: URL of the white agent backend (optional)
    """
    controller = AgentController()
    
    # Register agents
    green_id = controller.register_agent("green", green_agent_url)
    logger.info(f"Green agent accessible at: /to_agent/{green_id}")
    
    if white_agent_url:
        white_id = controller.register_agent("white", white_agent_url)
        logger.info(f"White agent accessible at: /to_agent/{white_id}")
    
    logger.info(f"Starting controller on {host}:{port}")
    logger.info("Agent discovery endpoint: /agents")
    
    # Run the server
    uvicorn.run(controller.app, host=host, port=port)


if __name__ == "__main__":
    start_controller()
