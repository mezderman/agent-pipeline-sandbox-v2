from config.enum import EventType, AgentName

EVENT_TO_AGENT_MAP = {
    EventType.REFUND_REQUEST: AgentName.REFUND,
    EventType.OTHER: AgentName.OTHER,
    EventType.REFUND_PASS: AgentName.REFUND_COMPLETE,
    EventType.REFUND_FAIL: AgentName.HUMAN_IN_LOOP,
    EventType.PRODUCT_ISSUE: AgentName.PRODUCT_ISSUE,
} 