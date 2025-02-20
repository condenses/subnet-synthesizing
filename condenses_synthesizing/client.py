import httpx
from typing import Optional
from dataclasses import dataclass


@dataclass
class SynthesizingResponse:
    user_message: str


class SynthesizingClient:
    """Synchronous client for the synthesizing server"""

    def __init__(self, base_url: str = "http://localhost:9104", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=timeout)

    def get_message(self, timeout: Optional[float] = None) -> SynthesizingResponse:
        """Get a synthesized message from the server

        Args:
            timeout: Optional timeout in seconds. Overrides the client default if provided.
        """
        response = self.client.get(f"{self.base_url}/api/synthesizing", timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return SynthesizingResponse(**data)

    def close(self):
        """Close the client session"""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSynthesizingClient:
    """Asynchronous client for the synthesizing server"""

    def __init__(self, base_url: str = "http://localhost:9104", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.client: Optional[httpx.AsyncClient] = None
        self.timeout = timeout

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the client session"""
        if self.client:
            await self.client.aclose()

    async def get_message(
        self, timeout: Optional[float] = None
    ) -> SynthesizingResponse:
        """Get a synthesized message from the server

        Args:
            timeout: Optional timeout in seconds. Overrides the client default if provided.
        """
        if not self.client:
            self.client = httpx.AsyncClient(timeout=self.timeout)

        response = await self.client.get(
            f"{self.base_url}/api/synthesizing", timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        return SynthesizingResponse(**data)


# Example usage:
if __name__ == "__main__":
    import asyncio

    # Synchronous example
    def sync_example():
        with SynthesizingClient() as client:
            response = client.get_message()
            print(f"Sync response: {response.user_message}")

    # Async example
    async def async_example():
        async with AsyncSynthesizingClient() as client:
            response = await client.get_message()
            print(f"Async response: {response.user_message}")

    # Run examples
    print("Running synchronous example:")
    sync_example()

    print("\nRunning asynchronous example:")
    asyncio.run(async_example())
