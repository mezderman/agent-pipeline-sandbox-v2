import json
from typing import Literal
from pydantic import BaseModel, Field
from core.node import Node
from openai import OpenAI
from core.memory import Memory

class QueryAnalysis(BaseModel):
    intent: Literal["refund_request", "other"] = Field(
        ...,
        description="Classification of the query intent: either 'refund_request' or 'other'"
    )
    reason: str = Field(
        ...,
        description="Explanation of why the intent was classified this way"
    )

class QueryRouter(Node):
    def __init__(self, name):
        self.memory = Memory()
        self.client = OpenAI()
        
    def process(self, data):
        self.memory.add_message({
                "role": "developer",
                "content": """ Analyze the user query and classify its intent."""
        })
        self.memory.add_message({
                        "role": "user",
                        "content": json.dumps(data)
                    })
        completion = self.completion(self.client)
        analyzed_query = completion.choices[0].message.parsed
        return analyzed_query

    def completion(self, client: OpenAI):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=self.memory.get_messages(),
            response_format=QueryAnalysis
        )
        return completion