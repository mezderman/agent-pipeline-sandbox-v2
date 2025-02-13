import json
from typing import Literal
from pydantic import BaseModel, Field
from core.node import Node
from openai import OpenAI
from core.pipeline_manager import PipelineManager
from config.enum import PipelineName, IntentType



class QueryAnalysis(BaseModel):
    intent: Literal["refund_request", "other"] = Field(
        ...,
        description="Classification of the query intent: either 'refund_request' or 'other'"
    )
    customer_id: str = Field(
        ...,
        description="Customer ID"
    )
    order_id: str = Field(
        ...,
        description="Order ID"
    )
    reason: str = Field(
        ...,
        description="Explanation of why the intent was classified this way"
    )

class QueryRouterNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = OpenAI()

        
    def process(self, data):
        super().process(data)
        msg= [
            {
                "role": "developer",
                "content": """ Analyze the user query and classify its intent."""
            },
            {
                "role": "user",
                "content": json.dumps(data)
            }
        ]
        analyzed_query = self.completion(self.client, msg)
        return analyzed_query


    def save_output_data(self, analyzed_query):
        self.set_output_data(analyzed_query)

    def completion(self, client: OpenAI, msg):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=msg,
            response_format=QueryAnalysis
        )
        analyzed_query = completion.choices[0].message.parsed
        return analyzed_query


   