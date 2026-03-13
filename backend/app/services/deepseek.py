from typing import AsyncGenerator

from openai import AsyncOpenAI

from ..config import DEEPSEEK_API_KEY

client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


async def stream_chat(messages: list[dict]) -> AsyncGenerator[str, None]:
    """Call DeepSeek API with streaming and yield content chunks."""
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True,
    )
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content
