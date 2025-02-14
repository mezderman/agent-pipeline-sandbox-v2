from enum import Enum

class PipelineName(str, Enum):
    """Enum for all pipeline types"""
    ROUTER = "query-router-pipeline"
    REFUND = "refund-pipeline"
    HUMAN_IN_LOOP = "human-in-loop-pipeline"
    REFUND_COMPLETE = "refund-complete-pipeline"
    OTHER = "other-pipeline"

class EventType(str, Enum):
    """Enum for all event types"""
    REFUND_REQUEST = "refund_request"
    REFUND_PASS = "refund_pass"
    REFUND_FAIL = "refund_fail"
    OTHER = "other"