import logging
import sys

try:
    import structlog
except ImportError:  # pragma: no cover - dependency fallback path
    structlog = None


def configure_logging(log_level: str = "INFO") -> None:
    if structlog is None:
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
            stream=sys.stdout,
            level=getattr(logging, log_level.upper(), logging.INFO),
        )
        return

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=shared_processors + [structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
