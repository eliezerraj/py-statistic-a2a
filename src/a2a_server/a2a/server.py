import logging
import json

from src.a2a_server.domain.usecase.calculation import compute_statistics, Statistic
from src.a2a_server.a2a.exception import A2ARequestError, A2ARouterError
from src.a2a_server.infrastructure.auth.cedar_verifier import CedarVerifier
from src.a2a_server.domain.dto.apperrs import AuthorizationDeniedError

from opentelemetry.trace.status import Status, StatusCode
from opentelemetry import trace

#---------------------------------
# Configure logging and tracer
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class A2AServer:
    
    def __init__(self, settings):
        
        self.settings = settings
        self.cedar_verifier = CedarVerifier()
        
        logger.info("A2AServer initialized SUCCESSFULLY")
    
    def router(self, envelope) -> Statistic:
        with tracer.start_as_current_span("a2a.server.router") as span:
            span.set_attribute("envelope.id", getattr(envelope, "message_id", "unknown"))
            
            try:
                if envelope.message_type == "statistics.compute":
                    logger.info("Handling statistics.compute message type.")
                    
                    # This will raise AuthorizationDeniedError if not authorized
                    # (caught by global exception handler in main.py)
                    self.cedar_verifier.validate(
                        action="compute.statistics",
                        resource_type="Statistic",
                        resource_id="*",
                        resource_attrs={"data": envelope.payload["data"]},
                    )
                    
                    response = compute_statistics(envelope.payload["data"])
                    return response
                
                if envelope.message_type == "statistics.agent.status":
                    logger.info("Handling statistics.agent.status message type.")
                    
                    response = {"message": "agent status ok",
                                "data": json.dumps(self.settings.dict() if hasattr(self.settings, "dict") else self.settings.__dict__),
                            }
                    
                    return response
                else:
                    logger.error("Unsupported message type: %s", envelope.message_type)
                    raise A2ARouterError(f"Unsupported message type: {envelope.message_type}")

            except A2ARouterError:
                # Re-raise A2A-specific errors (handled at endpoint level)
                raise
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error("Unexpected error in router", exc_info=e)
                raise
