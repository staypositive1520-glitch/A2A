from google.adk.agents.llm_agent import Agent
from elon.tools import calendar
import httpx,uuid
from a2a.client import A2ACardResolver,A2AClient
from a2a.types import SendMessageRequest
import nest_asyncio
import asyncio
nest_asyncio.apply()
class Remote:
    def __init__(self,url,card):
        self.url=url
        self.card=card
        self.client=httpx.AsyncClient()
        self.remote_client=A2AClient(httpx_client=self.client,
                                     agent_card=self.card,
                                     url=self.url)
    async def send_message(self,request:SendMessageRequest):
        res=await self.remote_client.send_message(request)
        return res
class ElonAgent:
    def __init__(self,urls):
        self.agent=None
        self.remote_urls=urls
        self.cards={}
        self.remote_clients={}
    async def create_agent(self):
        await self.load_remote_agent()
        friends=', '.join([name for name in self.cards.keys()])
        self.agent=Agent(
            model='gemini-flash-latest',
            name='elon_agent',
            description=f"""you are scheduling assistance of Elon,
            schedule tennis match for Elon with other friends based on availability of Elon
            and his friends. \n\nFriends : {friends}""",
            instruction=f"""you are scheduling assistance of Elon,
            schedule tennis match for Elon with other friends based on availability of Elon
            and his friends. \n\nFriends : {friends}""",
            tools=[calendar,self.send_message_to_client],
            )
        return self.agent
    async def load_remote_agent(self):
        async with httpx.AsyncClient() as client:
            for url in self.remote_urls:
                obj=A2ACardResolver(httpx_client=client,base_url=url,
                                     agent_card_path='/.well-known/agent-card.json')
                card=await obj.get_agent_card()
                self.cards[card.name]=card
                r=Remote(url=url,card=card)
                self.remote_clients[card.name]=r
    async def send_message_to_client(self,agent_name,query):
        agent=self.remote_clients[agent_name]
        id=str(uuid.uuid4())
        msg={
            "message":{
                "role":"user",
                "parts":[{"type":"text","text":query}],
                "message_id":id
            }
        }
        res=await agent.send_message(SendMessageRequest(id=id,params=msg))
        return res
async def main():
    urls=['http://localhost:1001','http://localhost:1002']
    obj=ElonAgent(urls)
    agent=await obj.create_agent()
    return agent
root_agent=asyncio.run(main())