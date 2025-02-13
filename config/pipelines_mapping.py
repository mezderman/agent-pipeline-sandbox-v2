from config.enum import IntentType, PipelineName

INTENT_TO_PIPELINE_MAP = {
    IntentType.REFUND_REQUEST: PipelineName.REFUND,
    IntentType.OTHER: PipelineName.OTHER
} 