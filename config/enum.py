from enum import Enum

class PipelineName(str, Enum):
    """Enum for all pipeline types"""
    INTENT_ROUTER = "intent-router-pipeline"
    REFUND = "refund-pipeline"
    HUMAN_IN_LOOP = "human-in-loop-pipeline"
    REFUND_COMPLETE = "refund-complete-pipeline"
    OTHER = "other-pipeline"
    PRODUCT_ISSUE = "product-issue-pipeline"

class EventType(str, Enum):
    """Enum for all event types"""
    REFUND_REQUEST = "refund_request"
    REFUND_PASS = "refund_pass"
    REFUND_FAIL = "refund_fail"
    OTHER = "other"
    PRODUCT_ISSUE = "product_issue"