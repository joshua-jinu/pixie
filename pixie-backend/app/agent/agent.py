import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent

from app.tools.summarize import summarize
from app.tools.spotify_controller import spotify_controller
from app.agent.system_prompt import SYSTEM_PROMPT

load_dotenv()


class Agent:
    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,   # deterministic for intent
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        self.tools = [summarize, spotify_controller]

        self.store = InMemoryStore()

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            store=self.store
        )

    # ------------------------
    # Public entry point
    # ------------------------

    async def run(self, session_id: str, query: str):

        result = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]},
            config={"configurable": {"thread_id": session_id}}
        )

        return result["messages"][-1].content

agent = Agent()
