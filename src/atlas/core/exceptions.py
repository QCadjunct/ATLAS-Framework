"""
Exception hierarchy for ATLAS Framework.

Provides comprehensive exception handling with detailed error information
and recovery suggestions.
"""

from typing import Any, Dict, List, Optional, Union
import traceback
from datetime import datetime


class ATLASError(Exception):
    """
    Base exception class for all ATLAS Framework errors.
    
    Provides comprehensive error information including context,
    suggestions for resolution, and debugging information.
    
    Args:
        message: Human-readable error message
        error_code: Unique error code for programmatic handling
        context: Additional context information about the error
        suggestions: List of suggested actions to resolve the error
        cause: Original exception that caused this error
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.context = context or {}
        self.suggestions = suggestions or []
        self.cause = cause
        self.timestamp = datetime.utcnow()
        self.traceback_info = traceback.format_exc() if cause else None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary containing all error information
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "context": self.context,
            "suggestions": self.suggestions,
            "timestamp": self.timestamp.isoformat(),
            "cause": str(self.cause) if self.cause else None,
            "traceback": self.traceback_info,
        }
    
    def __str__(self) -> str:
        """
        String representation of the exception.
        
        Returns:
            str: Formatted error message with context
        """
        parts = [f"{self.error_code}: {self.message}"]
        
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            parts.append(f"Context: {context_str}")
        
        if self.suggestions:
            suggestions_str = "; ".join(self.suggestions)
            parts.append(f"Suggestions: {suggestions_str}")
        
        if self.cause:
            parts.append(f"Caused by: {self.cause}")
        
        return " | ".join(parts)


class ValidationError(ATLASError):
    """
    Exception raised when data validation fails.
    
    Used for Pydantic validation errors, schema validation failures,
    and custom validation logic errors.
    """
    
    def __init__(
        self,
        message: str,
        field_errors: Optional[Dict[str, List[str]]] = None,
        validation_type: str = "general",
        **kwargs: Any,
    ) -> None:
        self.field_errors = field_errors or {}
        self.validation_type = validation_type
        
        # Add field errors to context
        context = kwargs.get("context", {})
        context.update({
            "field_errors": self.field_errors,
            "validation_type": self.validation_type,
        })
        kwargs["context"] = context
        
        # Add validation-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        if self.field_errors:
            suggestions.append("Check field values and types")
            suggestions.append("Refer to schema documentation")
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)


class ConfigurationError(ATLASError):
    """
    Exception raised when configuration is invalid or missing.
    
    Used for missing configuration files, invalid configuration values,
    and configuration schema violations.
    """
    
    def __init__(
        self,
        message: str,
        config_path: Optional[str] = None,
        config_section: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.config_path = config_path
        self.config_section = config_section
        
        # Add configuration context
        context = kwargs.get("context", {})
        context.update({
            "config_path": self.config_path,
            "config_section": self.config_section,
        })
        kwargs["context"] = context
        
        # Add configuration-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        suggestions.extend([
            "Check configuration file exists and is readable",
            "Validate configuration against schema",
            "Ensure all required fields are present",
        ])
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="CONFIGURATION_ERROR", **kwargs)


class ConnectionError(ATLASError):
    """
    Exception raised when connection to external services fails.
    
    Used for database connections, API connections, and network failures.
    """
    
    def __init__(
        self,
        message: str,
        service_name: Optional[str] = None,
        connection_uri: Optional[str] = None,
        retry_count: int = 0,
        **kwargs: Any,
    ) -> None:
        self.service_name = service_name
        self.connection_uri = connection_uri
        self.retry_count = retry_count
        
        # Add connection context
        context = kwargs.get("context", {})
        context.update({
            "service_name": self.service_name,
            "connection_uri": self.connection_uri,
            "retry_count": self.retry_count,
        })
        kwargs["context"] = context
        
        # Add connection-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        suggestions.extend([
            "Check network connectivity",
            "Verify service is running and accessible",
            "Check authentication credentials",
            "Review firewall and security settings",
        ])
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="CONNECTION_ERROR", **kwargs)


class SecurityError(ATLASError):
    """
    Exception raised when security validation fails.
    
    Used for authentication failures, authorization errors,
    and security policy violations.
    """
    
    def __init__(
        self,
        message: str,
        security_context: Optional[str] = None,
        required_permissions: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.security_context = security_context
        self.required_permissions = required_permissions or []
        
        # Add security context
        context = kwargs.get("context", {})
        context.update({
            "security_context": self.security_context,
            "required_permissions": self.required_permissions,
        })
        kwargs["context"] = context
        
        # Add security-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        suggestions.extend([
            "Check authentication credentials",
            "Verify user permissions and roles",
            "Review security policies",
            "Contact system administrator if needed",
        ])
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="SECURITY_ERROR", **kwargs)


class GraphError(ATLASError):
    """
    Exception raised when graph database operations fail.
    
    Used for Neo4j connection errors, Cypher query failures,
    and graph schema violations.
    """
    
    def __init__(
        self,
        message: str,
        query: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        self.query = query
        self.parameters = parameters
        
        # Add graph context
        context = kwargs.get("context", {})
        context.update({
            "query": self.query,
            "parameters": self.parameters,
        })
        kwargs["context"] = context
        
        # Add graph-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        suggestions.extend([
            "Check Cypher query syntax",
            "Verify graph database connection",
            "Review query parameters and types",
            "Check graph schema constraints",
        ])
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="GRAPH_ERROR", **kwargs)


class ExtractionError(ATLASError):
    """
    Exception raised when data extraction fails.
    
    Used for web scraping failures, document parsing errors,
    and LLM extraction failures.
    """
    
    def __init__(
        self,
        message: str,
        source_url: Optional[str] = None,
        extraction_method: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.source_url = source_url
        self.extraction_method = extraction_method
        
        # Add extraction context
        context = kwargs.get("context", {})
        context.update({
            "source_url": self.source_url,
            "extraction_method": self.extraction_method,
        })
        kwargs["context"] = context
        
        # Add extraction-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        suggestions.extend([
            "Check source URL accessibility",
            "Verify extraction method configuration",
            "Review rate limiting and retry settings",
            "Check for changes in source structure",
        ])
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="EXTRACTION_ERROR", **kwargs)


class BehaviorError(ATLASError):
    """
    Exception raised when node behavior execution fails.
    
    Used for behavior composition errors, execution failures,
    and behavior configuration issues.
    """
    
    def __init__(
        self,
        message: str,
        behavior_type: Optional[str] = None,
        node_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.behavior_type = behavior_type
        self.node_id = node_id
        
        # Add behavior context
        context = kwargs.get("context", {})
        context.update({
            "behavior_type": self.behavior_type,
            "node_id": self.node_id,
        })
        kwargs["context"] = context
        
        # Add behavior-specific suggestions
        suggestions = kwargs.get("suggestions", [])
        suggestions.extend([
            "Check behavior configuration",
            "Verify behavior is enabled and priority is set",
            "Review behavior dependencies",
            "Check node has required methods",
        ])
        kwargs["suggestions"] = suggestions
        
        super().__init__(message, error_code="BEHAVIOR_ERROR", **kwargs)


# Exception registry for programmatic access
EXCEPTION_REGISTRY = {
    "ATLAS_ERROR": ATLASError,
    "VALIDATION_ERROR": ValidationError,
    "CONFIGURATION_ERROR": ConfigurationError,
    "CONNECTION_ERROR": ConnectionError,
    "SECURITY_ERROR": SecurityError,
    "GRAPH_ERROR": GraphError,
    "EXTRACTION_ERROR": ExtractionError,
    "BEHAVIOR_ERROR": BehaviorError,
}


def get_exception_class(error_code: str) -> type[ATLASError]:
    """
    Get exception class by error code.
    
    Args:
        error_code: Error code string
        
    Returns:
        type[ATLASError]: Exception class for the error code
        
    Raises:
        ValueError: If error code is not found
    """
    if error_code not in EXCEPTION_REGISTRY:
        raise ValueError(f"Unknown error code: {error_code}")
    
    return EXCEPTION_REGISTRY[error_code]


def create_exception(
    error_code: str,
    message: str,
    **kwargs: Any,
) -> ATLASError:
    """
    Create exception instance by error code.
    
    Args:
        error_code: Error code string
        message: Error message
        **kwargs: Additional exception arguments
        
    Returns:
        ATLASError: Exception instance
    """
    exception_class = get_exception_class(error_code)
    return exception_class(message, **kwargs)

