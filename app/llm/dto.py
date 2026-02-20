from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class LLMResponse:
   
    text: str | None = None

    # tool call
    tool_name: str | None = None
    tool_args: dict | None = None
    
    contents: list | None = None

    error_code: int | str | None = None
    error_message: str | None = None
    retriable: bool = False
    is_final: bool = False
    
@dataclass
class ToolCall:
    name: str = ""
    args: dict | None = None
    output: Any = None