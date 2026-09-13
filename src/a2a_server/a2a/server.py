import logging

from src.a2a_server.domain.usecase.calculation import compute_statistics, Statistic
from src.a2a_server.a2a.exception import A2ARequestError, A2ARouterError

from opentelemetry.trace.status import Status, StatusCode
from opentelemetry import trace

#---------------------------------
# Configure logging and tracer
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class A2AServer:
    
    def __init__(self):
        self.tracer = tracer
        self.logger = logger
        self.logger.info("A2AServer initialized.")
    
    def router(self, envelope) -> Statistic:
        with tracer.start_as_current_span("a2a.server.router") as span:
            span.set_attribute("envelope.id", getattr(envelope, "message_id", "unknown"))
            
            try:
                if envelope.message_type == "statistics.compute":
                    self.logger.info("Handling statistics.compute message type.")
                    
                    response = compute_statistics(envelope.payload["data"])
                    return response
                else:
                    self.logger.error("Handling unsupported message type.")
                    message = f"Unsupported message type: {envelope.message_type}"
                    raise A2ARouterError(message)

            except A2ARouterError as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error("Error A2ARouterError message", exc_info=e)
                raise e
            
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error("Error uncaugth Exception", exc_info=e)
                raise e
