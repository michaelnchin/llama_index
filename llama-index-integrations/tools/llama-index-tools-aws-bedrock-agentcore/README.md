# AWS Bedrock AgentCore Tools

This module provides tools for interacting with AWS Bedrock AgentCore's browser and code interpreter sandbox tools.

## Installation

```bash
pip install llama-index-tools-aws-bedrock-agentcore
```

For the examples below, also install:
```bash
pip install llama-index llama-index-llms-bedrock-converse
```

## Requirements

- AWS credentials configured (either through environment variables or AWS CLI)
- `bedrock-agentcore` package (requires Python >= 3.10)
- Access to AWS Bedrock AgentCore services

## Tools

### Browser

The Bedrock AgentCore `browser` tools provide a way to interact with web browsers in a secure sandbox environment.

Included tools:

- `browser_start`: Start a browser sandbox session.
- `browser_stop`: Stop the current browser session.
- `browser_view`: Generate a URL to view the browser session.
- `browser_control`: Take control of the browser session.
- `browser_release`: Release control of the browser session.
- `browser_ws_headers`: Generate WebSocket headers for connecting to the browser sandbox.

Example usage:

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.tools.aws_bedrock_agentcore import AgentCoreBrowserToolSpec
from llama_index.core.agent.workflow import FunctionAgent

tool_spec = AgentCoreBrowserToolSpec(region="us-west-2")

tools = tool_spec.to_tool_list()
print(tools)

llm = BedrockConverse(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-west-2",
)

agent = FunctionAgent(
    tools=tools,
    llm=llm,
)

start_response = await agent.run(
    "Start a browser session and navigate to google.com."
)
print(str(start_response))
view_response = await agent.run(
    "Return a URL to view the current browser session."
)
print(str(view_response))
stop_response = await agent.run("Stop the browser session.")
print(str(stop_response))
```

### Code Interpreter

The Bedrock AgentCore `code_interpreter` tools provide a way to execute code and commands in a secure sandbox environment.

Included tools:

- `execute_code`: Run code in various languages (primarily Python).
- `execute_command`: Run shell commands.
- `read_files`: Read content of files in the environment.
- `list_files`: List files in directories.
- `delete_files`: Remove files from the environment.
- `write_files`: Create or update files.
- `start_command`: Start long-running commands asynchronously.
- `get_task`: Check status of async tasks.
- `stop_task`: Stop running tasks.

Example usage:

```python
import asyncio
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.tools.aws_bedrock_agentcore import AgentCoreCodeInterpreterToolSpec
from llama_index.core.agent.workflow import FunctionAgent

import nest_asyncio
nest_asyncio.apply() # In case of existing loop (ex. in JupyterLab)

async def main():
    tool_spec = AgentCoreCodeInterpreterToolSpec(region="us-west-2")
    tools = tool_spec.to_tool_list()

    llm = BedrockConverse(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        region_name="us-west-2",
    )

    agent = FunctionAgent(
        tools=tools,
        llm=llm,
    )

    code_task = "Write a Python function that calculates the factorial of a number and test it."

    code_response = await agent.run(code_task)
    print(str(code_response))

    command_task = "Use terminal CLI commands to: 1) Show the environment's Python version. 2) Show me the list of Python package currently installed in the environment."

    command_response = await agent.run(command_task)
    print(str(command_response))

    await tool_spec.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```
