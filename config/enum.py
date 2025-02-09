from enum import Enum

class PipelineName(str, Enum):
    """Enum for all pipeline types"""
    ROUTER = "query-router-pipeline"
    REFUND = "refund-pipeline"
    OTHER = "other-pipeline"

class IntentType(str, Enum):
    """Enum for all intent types"""
    REFUND_REQUEST = "refund_request"
    OTHER = "other"