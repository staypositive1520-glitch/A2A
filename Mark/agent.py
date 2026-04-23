from crewai import Agent, Crew, Process, Task,LLM
from tools import calendar
class MarkAgent:
    def __init__(self):
        self.llm = LLM(
            model="gemini/gemini-2.5-flash-lite",
            api_key="xxxx")
        self.agent=Agent(
            llm=self.llm,
            role='scheduling assistant',
            goal='find out availability of Mark using calendar tool',
            backstory=f"""you are a helpful scheduling assistance
            please find availability of Mark for a tennis match 
            using calendar tool""",
            system_template=f"""you are a helpful scheduling assistance
            please find availability of Mark for a tennis match 
            using calendar tool""",
            tools=[calendar]
            )
    async def run(self,query):
        self.task=Task(
            description=query,
            expected_output="""
                dict of availability of Mark for tennis match on given date
            """,
            agent=self.agent,
             tools=[calendar] )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential )
        res=self.crew.kickoff()
        return res.raw