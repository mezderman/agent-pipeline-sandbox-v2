from pydantic import BaseModel
from typing import List

class Response(BaseModel):
    messages: List = []
    context_variables: dict = {}