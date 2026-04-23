from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from tools import calendar
from dotenv import load_dotenv
load_dotenv()
class JeffAgent:
    def __init__(self):
        self.llm=ChatGoogleGenerativeAI(
            model='gemini-2.5-flash-lite'    )
        self.agent=create_agent(
            model=self.llm,
            tools=[calendar],
            system_prompt=f"""You are a helpful scheduling assistant,
            schedule tennis match based on availability of Jeff using calendar tool""")
    async def invoke(self,query):
        inputs = {"messages": [
            {"role": "user", 
             "content": query}]}
        res=self.agent.invoke(inputs)
        res=res['messages']
        res=[msg.content for msg in res if isinstance(msg,AIMessage)][-1]
        print(res,type(res))
        return res
