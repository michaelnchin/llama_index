"""AWS Bedrock AgentCore Code Interpreter Tool."""

import os
from typing import Dict, Any, Optional

from llama_index.core.tools.tool_spec.base import BaseToolSpec

from bedrock_agentcore.tools.code_interpreter_client import CodeInterpreter

DEFAULT_CODE_INTERPRETER_IDENTIFIER = "aws.codeinterpreter.v1"
DEFAULT_CODE_INTERPRETER_TIMEOUT = 900


def get_aws_region() -> str:
    """Get the AWS region from environment variables or use default."""
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-west-2"


class AgentCoreCodeInterpreterToolSpec(BaseToolSpec):
    """AWS Bedrock AgentCore Code Interpreter Tool Spec."""

    spec_functions = [
        "code_interpreter_start",
        "code_interpreter_stop",
        "code_interpreter_execute",
    ]

    def __init__(self, region: Optional[str] = None) -> None:
        """
        Initialize the AWS Bedrock AgentCore Code Interpreter Tool Spec.

        Args:
            region (Optional[str]): AWS region to use for Bedrock AgentCore services.
                If not provided, will try to get it from environment variables.

        """
        self.region = region if region is not None else get_aws_region()
        self.code_interpreter = CodeInterpreter(self.region)

    def code_interpreter_start(
        self,
        identifier: Optional[str] = DEFAULT_CODE_INTERPRETER_IDENTIFIER,
        name: Optional[str] = None,
        session_timeout_seconds: Optional[int] = DEFAULT_CODE_INTERPRETER_TIMEOUT,
    ) -> str:
        """
        Start a code interpreter sandbox session.

        Args:
            identifier (Optional[str]): The code interpreter sandbox identifier to use. This should always be aws.codeinterpreter.v1.
            name (Optional[str]): A name for the code interpreter session.
            session_timeout_seconds (Optional[int]): The timeout for the session in seconds.

        Returns:
            str: The session ID of the newly created session.

        """
        session_id = self.code_interpreter.start(
            identifier=identifier,
            name=name,
            session_timeout_seconds=session_timeout_seconds,
        )
        return f"Code interpreter session started with ID: {session_id}"

    def code_interpreter_stop(self) -> str:
        """
        Stop the current code interpreter session.

        Returns:
            str: Confirmation message.

        """
        self.code_interpreter.stop()
        return "Code interpreter session stopped"

    def code_interpreter_execute(
        self,
        method: str = "execute",
        params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Execute code in the code interpreter sandbox.

        Args:
            method (str): The name of the method to invoke in the sandbox. Default is "execute".
            params (Optional[Dict[str, Any]]):  Parameters to pass to the method.

        Returns:
            str: The result of the code execution.

        """
        result = self.code_interpreter.invoke(method, params)
        return f"Code execution result: {result}"
