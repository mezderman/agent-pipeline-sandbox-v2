from config.enum import IntentType, PipelineName

INTENT_TO_PIPELINE_MAP = {
    IntentType.REFUND_REQUEST: PipelineName.REFUND,
    IntentType.OTHER: PipelineName.OTHER,
    IntentType.REFUND_PASS: PipelineName.REFUND_COMPLETE,
    IntentType.REFUND_FAIL: PipelineName.HUMAN_IN_LOOP,
} 