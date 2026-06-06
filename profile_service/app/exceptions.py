class ProfileServiceError(Exception):
    """Base class for profile service failures."""


class NotFoundError(ProfileServiceError):
    """Raised when a requested resource does not exist."""


class ConflictError(ProfileServiceError):
    """Raised when an operation conflicts with current state."""


class LLMProviderError(ProfileServiceError):
    """Raised when LLM calls fail."""


class ExtractionError(ProfileServiceError):
    """Raised when PDF text extraction fails."""


class ValidationError(ProfileServiceError):
    """Raised when request validation fails at the service layer."""
