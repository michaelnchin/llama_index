import os
from typing import Dict, Any, Optional

from llama_index.core.tools.tool_spec.base import BaseToolSpec

from genesis.tools.browser_client import BrowserClient
from genesis.tools.code_interpreter_client import CodeInterpreter

DEFAULT_BROWSER_IDENTIFIER = "aws.browser.v1"
DEFAULT_BROWSER_SESSION_TIMEOUT = 3600
DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT = 300

DEFAULT_CODE_INTERPRETER_IDENTIFIER = "aws.codeinterpreter.v1"
DEFAULT_CODE_INTERPRETER_TIMEOUT = 900


def get_aws_region() -> str:
    """Get the AWS region from environment variables or use default."""
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-west-2"


class AWSGenesisToolSpec(BaseToolSpec):
    """AWS Genesis tool spec for browser and code interpreter tools."""

    spec_functions = [
        "browser_start",
        "browser_stop",
        "browser_view",
        "browser_control",
        "browser_release",
        "browser_ws_headers",
        "code_interpreter_start",
        "code_interpreter_stop",
        "code_interpreter_execute",
    ]

    def __init__(self, region: Optional[str] = None) -> None:
        """
        Initialize the AWS Genesis tool spec.

        Args:
            region (Optional[str]): AWS region to use for Genesis services.
                If not provided, will try to get it from environment variables.

        """
        self.region = region if region is not None else get_aws_region()
        self.browser_client = BrowserClient(self.region)
        self.code_interpreter = CodeInterpreter(self.region)

    def browser_start(
        self,
        identifier: Optional[str] = DEFAULT_BROWSER_IDENTIFIER,
        name: Optional[str] = None,
        session_timeout_seconds: Optional[int] = DEFAULT_BROWSER_SESSION_TIMEOUT,
    ) -> str:
        """
        Start a browser sandbox session.

        Args:
            identifier (Optional[str]): The browser sandbox identifier to use.
            name (Optional[str]): A name for the browser session.
            session_timeout_seconds (Optional[int]): The timeout for the session in seconds.

        Returns:
            str: The session ID of the newly created session.

        """
        session_id = self.browser_client.start(
            identifier=identifier,
            name=name,
            session_timeout_seconds=session_timeout_seconds,
        )
        return f"Browser session started with ID: {session_id}"

    def browser_stop(self) -> str:
        """
        Stop the current browser session.

        Returns:
            str: Confirmation message.

        """
        self.browser_client.stop()
        return "Browser session stopped"

    def browser_ws_headers(self) -> str:
        """
        Generate WebSocket headers for connecting to the browser sandbox.

        Returns:
            str: The WebSocket URL and headers.

        """
        ws_url, headers = self.browser_client.generate_ws_headers()
        return f"WebSocket URL: {ws_url}\nHeaders: {headers}"

    def browser_view(
        self, expires: Optional[int] = DEFAULT_BROWSER_LIVE_VIEW_PRESIGNED_URL_TIMEOUT
    ) -> str:
        """
        Generate a URL to view the browser session.

        Args:
            expires (Optional[int]): The number of seconds until the pre-signed URL expires.

        Returns:
            str: The pre-signed URL for viewing the browser session.

        """
        url = self.browser_client.generate_live_view_url(expires=expires)
        return f"Browser view URL: {url}"

    def browser_control(self) -> str:
        """
        Take control of the browser session.

        Returns:
            str: Confirmation message.

        """
        self.browser_client.take_control()
        return "Took control of browser session"

    def browser_release(self) -> str:
        """
        Release control of the browser session.

        Returns:
            str: Confirmation message.

        """
        self.browser_client.release_control()
        return "Released control of browser session"

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
