# AWS Genesis Tools

This module provides tools for interacting with AWS Genesis SDK's browser and code interpreter sandbox tools.

## Installation

```bash
pip install llama-index-tools-aws-genesis
```

## Requirements

- AWS credentials configured (either through environment variables or AWS CLI)
- `genesis` package
- Access to AWS Genesis services

## Tools

### Browser

The Genesis `browser` tools provide a way to interact with web browsers in a secure sandbox environment.

Included tools:

- `browser_start`: Start a browser sandbox session.
- `browser_stop`: Stop the current browser session.
- `browser_view`: Generate a URL to view the browser session.
- `browser_control`: Take control of the browser session.
- `browser_release`: Release control of the browser session.
- `browser_ws_headers`: Generate WebSocket headers for connecting to the browser sandbox.

Example usage:

```python
# pip install llama-index llama-index-llms-bedrock-converse llama-index-tools-aws-genesis
from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.tools.aws_genesis import AWSGenesisToolSpec
from llama_index.core.agent.workflow import FunctionAgent

tool_spec = AWSGenesisToolSpec(region="us-west-2")

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

The Genesis `code_interpreter` tools provide a way to execute a given code method in a secure sandbox environment.

Included tools:

- `code_interpreter_start`: Start a code interpreter sandbox session.
- `code_interpreter_stop`: Stop the current code interpreter session.
- `code_interpreter_execute`: Execute code in the code interpreter sandbox.

Example usage:

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.tools.aws_genesis import AWSGenesisToolSpec
from llama_index.core.agent.workflow import FunctionAgent

tool_spec = AWSGenesisToolSpec(region="us-west-2")

tools = tool_spec.to_tool_list()
print(tools)

llm = BedrockConverse(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-west-2",
)

prompt = f"""You are working in a Python code interpreter sandbox.

Task: Generate a list of 10 random integers, within 1-100.

Generate Python code to accomplish this task. Be specific and include:
- Any necessary imports (pandas, numpy, matplotlib, json, etc are available)
- Error handling
- Clear output with print statements

Return ONLY the Python code, no explanations."""

resp = llm.chat([ChatMessage(role="user", content=prompt)])

agent = FunctionAgent(
    tools=tools,
    llm=llm,
)

response = await agent.run(f"Run {resp} and return the result.")
print(str(response))
```
