import asyncio
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os

# Load environment variables (including GEMINI_API_KEY)
load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": "gemini-1.5-flash",
            "api_key": os.getenv("GEMINI_API_KEY"),
            "api_type": "google"
        }
    ]
}

# Define the agents
planner_agent = AssistantAgent(
    name="planner_agent",
    description="A helpful assistant that can plan trips.",
    system_message="You are a helpful planner who creates travel plans based on user requests. Ask the Researcher for information as needed.",
    llm_config=llm_config,
)

travel_summary_agent = AssistantAgent(
    name="travel_summary_agent",
    description="A helpful assistant that can summarize the travel plan.",
    system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  
    code_execution_config=False,
)

groupchat = GroupChat(
    agents=[user_proxy, planner_agent, travel_summary_agent],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

async def main():
    print("Start planning...")

    await asyncio.to_thread(
        user_proxy.initiate_chat,
        manager,
        message="Plan a trip to Nepal",
    )


if __name__ == "__main__":
    asyncio.run(main())
