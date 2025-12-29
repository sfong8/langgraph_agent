from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
import asyncio
# Initialize Groq LLM
model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.1
)


client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": [r"E:\PyCharmProjects\langgraphAgent\math_server.py"], # make sure you set the correct path
            "transport": "stdio",
        },
        "weather": {
            # make sure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp", # make sure you opened the localhost
            "transport": "streamable_http",
        },
    }
)


# Define `tools` and each response that use `await` under the async `main()`
async def main():
    tools = await client.get_tools()
    agent = create_agent(model,
                         tools)

    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    print(math_response)
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
    print(weather_response)


if __name__ == "__main__":
    asyncio.run(main())