from enum import Enum

class AgentName(str, Enum):
    """Enum for all agent types"""
    INTENT_ROUTER = "intent-router-agent"
    REFUND = "refund-agent"
    HUMAN_IN_LOOP = "human-in-loop-agent"
    REFUND_COMPLETE = "refund-complete-agent"
    OTHER = "other-agent"
    PRODUCT_ISSUE = "product-issue-agent"

class EventType(str, Enum):
    """Enum for all event types"""
    REFUND_REQUEST = "refund_request"
    REFUND_PASS = "refund_pass"
    REFUND_FAIL = "refund_fail"
    OTHER = "other"
    PRODUCT_ISSUE = "product_issue"