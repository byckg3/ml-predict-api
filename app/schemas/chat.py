from typing import Any
from pydantic import BaseModel

class ChatPayload( BaseModel ):
    user_input: str
    history: list[ Any ] = []