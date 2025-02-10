import json
from typing import Literal
from pydantic import BaseModel, Field
from core.node import Node
from openai import OpenAI
from core.memory import Memory
from core.pipeline_manager import PipelineManager
from config.enum import PipelineName, IntentType

INTENT_TO_PIPELINE_MAP = {
    IntentType.REFUND_REQUEST: PipelineName.REFUND,
    IntentType.OTHER: PipelineName.OTHER
}

class QueryAnalysis(BaseModel):
    intent: Literal["refund_request", "other"] = Field(
        ...,
        description="Classification of the query intent: either 'refund_request' or 'other'"
    )
    reason: str = Field(
        ...,
        description="Explanation of why the intent was classified this way"
    )

class QueryRouterNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.memory = Memory()
        self.client = OpenAI()

        
    def process(self, data):
        super().process(data)
        self.memory.add_message({
                "role": "developer",
                "content": """ Analyze the user query and classify its intent."""
        })
        self.memory.add_message({
                        "role": "user",
                        "content": json.dumps(data)
                    })
        
        analyzed_query = self.completion(self.client)
       
        self.save_output_data(analyzed_query)
        pipeline_result = self.run_next_pipeline()

        return pipeline_result

    def run_next_pipeline(self):
        pipeline_manager = PipelineManager.get_instance()
        pipeline_name = INTENT_TO_PIPELINE_MAP[self.get_output_data().intent]
        pipeline_result = pipeline_manager.run_pipeline(pipeline_name, self.get_output_data())
        return pipeline_result

    def save_output_data(self, analyzed_query):
        msg={
                "role": "assistant",
                "content": f"""
                    Intent: {analyzed_query.intent}
                """
            }
        self.memory.add_message(msg)
        self.set_output_data(analyzed_query)

    def completion(self, client: OpenAI):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=self.memory.get_messages(),
            response_format=QueryAnalysis
        )
        analyzed_query = completion.choices[0].message.parsed
        return analyzed_query


   