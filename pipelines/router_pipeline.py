from core.pipeline import Pipeline
from config.enum import PipelineName
from nodes.query_router_node import QueryRouterNode

class RouterPipeline(Pipeline):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(QueryRouterNode("query-router-node"))
