from a2a.types import AgentSkill, AgentCapabilities, AgentCard
from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import JeffAgentExecutor
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
import uvicorn
def main():
    skill1=AgentSkill(
        name='find out avilablity',
        id='calendar',
        description='''based on given date find availability of Jeff
        for a tennis match''',
        tags=['scheduling','tennis','availability'],
        examples=['is Jeff available on "2026-04-08" for tennis match ?'])
    capability=AgentCapabilities(
        can_access_internet=True,
        can_access_tools=True,
        can_access_file=True)
    card=AgentCard(
        id='jeff_agent',
        name='jeff_agent',
        description='scheduling agent of jeff, using calendar tool find when jeff is free for tennis match',
        url='http://localhost:1002',
        version='1.0',
        preferredTransport='JSONRPC',
        defaultInputModes=['text/plain'],
        defaultOutputModes=['text/plain'],
        skills=[skill1],
        capabilities=capability
    )
    req=DefaultRequestHandler(
        agent_executor=JeffAgentExecutor(),
        task_store=InMemoryTaskStore()
    )
    server=A2AStarletteApplication(
        agent_card=card,
        http_handler=req
    )
    uvicorn.run(server.build(),host='0.0.0.0',port=1002)
if __name__=='__main__':
    main()
