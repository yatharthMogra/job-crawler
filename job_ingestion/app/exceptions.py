class IngestionError(Exception):
    """Base class for ingestion failures."""


class FetchError(IngestionError):
    """Raised when Greenhouse fetch fails."""


class ParseError(IngestionError):
    """Raised when fetched payload has invalid shape."""


class LLMProviderError(IngestionError):
    """Raised when LLM enrichment fails."""


class UnsupportedPlatformError(IngestionError):
    """Raised when a company platform has no registered connector."""


class ConnectorFetchError(FetchError):
    """Raised when a platform connector fails to fetch."""
