from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext
import asyncio
import nest_asyncio

# Enable nested event loops
nest_asyncio.apply()

@dataclass
class Customer:
    first_name: str
    last_name: str


@dataclass
class Customer:
    first_name: str
    last_name: str


agent = Agent(
    'openai:gpt-4o',
    deps_type=Customer,
)


@agent.system_prompt
def get_system_prompt(ctx: RunContext[Customer]) -> str:
    return f'Prompt: You are helpful assistant. Here is the user information: {ctx.deps.first_name} {ctx.deps.last_name}'


async def main():
    deps = Customer('John', 'Doe')
    result = agent.run_sync(
        'Greet user using first and last name',
        deps=deps,
    )
    print(result.data)
    print(result.all_messages())
    msg = result.new_messages()
    result = agent.run_sync(
        'What was my previous message?',
        deps=deps,
        message_history=msg,
    )
    print(result.data)


if __name__ == "__main__":
    asyncio.run(main())
        #> Did you hear about the toothpaste scandal? They called it Colgate.