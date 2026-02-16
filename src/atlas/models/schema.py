"""
Configuration schema for the ATLAS Framework.

This module provides Pydantic models for validating configuration,
ensuring that configuration is valid and complete.
"""

from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class GraphConfig(BaseModel):
    """Configuration for the graph database."""
    
    uri: str = Field(..., description="URI of the graph database")
    username: Optional[str] = Field(None, description="Username for authentication")
    password: Optional[str] = Field(None, description="Password for authentication")
    database: Optional[str] = Field(None, description="Database name")
    max_connections: int = Field(10, description="Maximum number of connections")
    connection_timeout: int = Field(30, description="Connection timeout in seconds")
    
    model_config = {
        "extra": "allow",
    }


class LLMConfig(BaseModel):
    """Configuration for the language model."""
    
    provider: str = Field(..., description="Provider of the language model")
    model: str = Field(..., description="Name of the language model")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    api_base: Optional[str] = Field(None, description="Base URL for API requests")
    max_tokens: int = Field(2048, description="Maximum number of tokens per request")
    temperature: float = Field(0.7, description="Temperature for generation")
    
    model_config = {
        "extra": "allow",
    }
    
    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """
        Validate that temperature is between 0 and 1.
        
        Args:
            v: Temperature value
            
        Returns:
            float: Validated temperature
            
        Raises:
            ValueError: If temperature is not between 0 and 1
        """
        if v < 0 or v > 1:
            raise ValueError("Temperature must be between 0 and 1")
        return v


class FabricConfig(BaseModel):
    """Configuration for FABRIC patterns."""
    
    patterns_dir: str = Field(..., description="Directory containing pattern files")
    default_patterns: List[str] = Field(
        default_factory=list,
        description="List of default patterns to load"
    )
    
    model_config = {
        "extra": "allow",
    }


class ATLASConfig(BaseModel):
    """Configuration for the ATLAS Framework."""
    
    graph: Optional[GraphConfig] = Field(None, description="Graph database configuration")
    llm: Optional[LLMConfig] = Field(None, description="Language model configuration")
    fabric: Optional[FabricConfig] = Field(None, description="FABRIC patterns configuration")
    
    model_config = {
        "extra": "allow",
    }
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "ATLASConfig":
        """
        Create a configuration from a dictionary.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            ATLASConfig: Validated configuration
        """
        return cls.model_validate(config)

