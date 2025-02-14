from config.enum import EventType, PipelineName

EVENT_TO_PIPELINE_MAP = {
    EventType.REFUND_REQUEST: PipelineName.REFUND,
    EventType.OTHER: PipelineName.OTHER,
    EventType.REFUND_PASS: PipelineName.REFUND_COMPLETE,
    EventType.REFUND_FAIL: PipelineName.HUMAN_IN_LOOP,
} 