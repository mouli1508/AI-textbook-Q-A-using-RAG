from typing import Optional, List
import json
import inspect
from letta.schemas.llm_config import LLMConfig
from letta.schemas.memory import ChatMemory
from letta.schemas.block import Block
from letta import create_client
from letta.schemas.embedding_config import EmbeddingConfig

client = create_client()

client.set_default_llm_config(LLMConfig.default_config("gpt-4o-mini"))

chat_memory = ChatMemory(
    human="Name: Bob",
    persona="You are a helpful assistant"
)

chat_memory.list_block_labels()
chat_memory.get_block("human")
dir(chat_memory)
print(inspect.getsource(chat_memory.core_memory_append))

chat_memory.get_prompt_template()
chat_memory.compile()


class TaskMemory(ChatMemory):

    def __init__(self, human: str, persona: str, tasks: List[str]):
        super().__init__(human=human, persona=persona, limit=2000)
        # self.link_block(
        #     name="tasks",
        #     block=Block(
        #         limit=2000,
        #         value=json.dumps(tasks),
        #         name="tasks",
        #         label="tasks"
        #     )
        # )
        self.set_block(
            block=Block(
                limit=2000,
                value=json.dumps(tasks),
                name="tasks",
                label="tasks"
            )
        )

    def task_queue_push(self, task_description: str):
        """
        Push to a task queue stored in core memory. 

        Args:
            task_description (str): A description of the next task you must accomplish. 

        Returns:
            Optional[str]: None is always returned as this function 
            does not produce a response.
        """
        import json
        tasks = json.loads(self.memory.get_block("tasks").value)
        tasks.append(task_description)
        self.memory.update_block_value("tasks", json.dumps(tasks))
        return None

    def task_queue_pop(self):
        """
        Get the next task from the task queue 

        Returns:
            Optional[str]: The description of the task popped from the 
            queue, if there are still tasks in queue. Otherwise, returns
            None (the task queue is empty)
        """
        import json
        tasks = json.loads(self.memory.get_block("tasks").value)
        if len(tasks) == 0:
            return None
        task = tasks[0]
        print("CURRENT TASKS: ", tasks)
        self.memory.update_block_value("tasks", json.dumps(tasks[1:]))
        return task


task_agent_name = "task_agent"

task_agent_state = client.create_agent(
    embedding_config="text-embedding-ada-002",
    name=task_agent_name,
    system=open("task_queue_system_prompt.txt", "r").read(),
    memory=TaskMemory(
        human="My name is Sarah",
        persona="You are an agent that must clear its tasks.",
        tasks=[]
    )
)


message = "Add 'start calling me Charles'"  \
    + "and 'tell me a haiku about my name' as two seperate tasks."

response = client.send_message(
    agent_id=task_agent_state.id,
    role="user",
    message=message
)
print(response.messages)


response = client.send_message(
    agent_id=task_agent_state.id,
    role="user",
    message="complete your tasks"
)
print(response.messages)

client.get_core_memory(task_agent_state.id).get_block("tasks")

client.get_block('cut_and_paste_id_from_above')
