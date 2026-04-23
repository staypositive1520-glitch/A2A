from a2a.server.agent_execution.agent_executor import AgentExecutor
from agent import JeffAgent
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks.task_updater import TaskUpdater
from a2a.types import Part
from a2a.types import TextPart
class JeffAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent=JeffAgent()
    async def execute(self,context: RequestContext, event_queue: EventQueue):
        updater=TaskUpdater(event_queue=event_queue, task_id=context.task_id,
                            context_id=context.context_id)
        if not context.current_task:
            await updater.submit()
        await updater.start_work()
        res=await self.agent.invoke(context.get_user_input())
        print(res)
        parts=[Part(root=TextPart(kind='text',text=res))]
        await updater.add_artifact(parts)
        await updater.complete()
    async def cancel(context: RequestContext, event_queue: EventQueue):
        pass