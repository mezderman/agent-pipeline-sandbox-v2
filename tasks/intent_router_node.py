import json
from pydantic import BaseModel, Field
from core.task import Task
from openai import OpenAI
from config.enum import EventType

class EventAnalysis(BaseModel):
    event: EventType = Field(
        ...,
        description=f"""Classification of the query intent: 
        If the query is about a product issue, return '{EventType.PRODUCT_ISSUE}'.
        If the query is about a refund, return '{EventType.REFUND_REQUEST}'. 
        If the query is about something else, return '{EventType.OTHER}'."""
    )
    intent: str = Field(
        ...,
        description=f"""{event}"""
    )
    from_email: str = Field(
        ...,
        description="From email"
    )
    subject: str = Field(
        ...,
        description="Subject"
    )
    message_date: str = Field(
        ...,
        description="Message date"
    )
    body: str = Field(
        ...,
        description="Body"
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
        description="Explanation of why the event was classified this way"
    )

class IntentRouterNode(Task):
    def __init__(self, name):
        super().__init__(name)
        self.client = OpenAI()

    def process(self, data):
        super().process(data)
        msg = [
            {
                "role": "system",
                "content": """You are a customer service assistant. Analyze the user query and classify its intent.
                Pay special attention to refund requests and related issues."""
            },
            {
                "role": "user",
                "content": json.dumps(data)
            }
        ]
        event_analysis = self.completion(self.client, msg)
        return event_analysis

    def save_output_data(self, analyzed_query):
        self.set_output_data(analyzed_query)

    def completion(self, client: OpenAI, msg):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=msg,
            response_format=EventAnalysis
        )
        analyzed_query = completion.choices[0].message.parsed
        return analyzed_query.model_dump(mode='json')


   