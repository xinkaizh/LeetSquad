"""Retrieve web page content from a given URL."""

import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


async def retrieve_url(url: str, timeout: float = 30.0) -> Optional[str]:
    """
    Retrieve the content of a web page from the given URL.

    Args:
        url: The URL of the web page to retrieve
        timeout: Request timeout in seconds (default: 30.0)

    Returns:
        The HTML content of the web page as a string, or None if retrieval fails

    Raises:
        httpx.HTTPError: If an HTTP error occurs during the request
    """
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error retrieving {url}: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error retrieving {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving {url}: {e}")
        raise


def retrieve_url_sync(url: str, timeout: float = 30.0) -> Optional[str]:
    """
    Synchronous version of retrieve_url for use in non-async contexts.

    Args:
        url: The URL of the web page to retrieve
        timeout: Request timeout in seconds (default: 30.0)

    Returns:
        The HTML content of the web page as a string, or None if retrieval fails

    Raises:
        httpx.HTTPError: If an HTTP error occurs during the request
    """
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error retrieving {url}: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error retrieving {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving {url}: {e}")
        raise


if __name__ == "__main__":
    import requests

    BASE_URL = "https://web-production-88ac7.up.railway.app"

    resp = requests.get(f"{BASE_URL}/agents")
    resp.raise_for_status()

    agents = resp.json()

    for agent_id, agent in agents.items():
        print(agent_id, agent["state"], agent["url"])