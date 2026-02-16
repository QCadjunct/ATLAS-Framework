"""
FABRIC pattern class for the ATLAS Framework.

This module provides a class for representing and applying
FABRIC patterns in the ATLAS Framework.
"""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from atlas.core.exceptions import FabricError


logger = logging.getLogger(__name__)


class FabricPatternConfig(BaseModel):
    """Configuration for a FABRIC pattern."""
    
    name: str = Field(..., description="Name of the pattern")
    description: str = Field(..., description="Description of the pattern")
    prompt_template: str = Field(..., description="Prompt template for the pattern")
    required_args: List[str] = Field(default_factory=list, description="Required arguments")
    optional_args: Dict[str, Any] = Field(default_factory=dict, description="Optional arguments with defaults")
    examples: List[Dict[str, Any]] = Field(default_factory=list, description="Example usages")


class FabricPattern:
    """
    Class for representing and applying FABRIC patterns.
    
    This class provides methods for loading and applying
    FABRIC patterns in the ATLAS Framework.
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Union[Dict[str, Any], FabricPatternConfig]] = None,
        llm_adapter: Optional[Any] = None
    ) -> None:
        """
        Initialize the FABRIC pattern.
        
        Args:
            name: Name of the pattern
            config: Optional pattern configuration
            llm_adapter: Optional LLM adapter for applying the pattern
            
        Raises:
            FabricError: If the pattern cannot be initialized
        """
        self.name = name
        self.llm_adapter = llm_adapter
        
        # Set config if provided
        if config is not None:
            if isinstance(config, dict):
                self.config = FabricPatternConfig.model_validate(config)
            else:
                self.config = config
        else:
            # Try to load from file
            self.config = self._load_from_file()
    
    def _load_from_file(self) -> FabricPatternConfig:
        """
        Load the pattern configuration from a file.
        
        Returns:
            FabricPatternConfig: Pattern configuration
            
        Raises:
            FabricError: If the pattern file cannot be loaded
        """
        # Check common locations
        locations = [
            Path(f"fabric/patterns/{self.name}.json"),
            Path(f"src/atlas/fabric/patterns/{self.name}.json"),
            Path(f"atlas/fabric/patterns/{self.name}.json"),
        ]
        
        for path in locations:
            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        config_data = json.load(f)
                    return FabricPatternConfig.model_validate(config_data)
                except Exception as e:
                    logger.warning(f"Failed to load pattern {self.name} from {path}: {e}")
        
        # If we get here, the pattern was not found
        raise FabricError(f"Pattern {self.name} not found", pattern=self.name)
    
    def apply(self, *args: Any, **kwargs: Any) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        """
        Apply the pattern to modify function arguments.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Tuple[Tuple[Any, ...], Dict[str, Any]]: Modified arguments
            
        Raises:
            FabricError: If the pattern cannot be applied
        """
        # Check if LLM adapter is available
        if self.llm_adapter is None:
            logger.warning(f"No LLM adapter available for pattern {self.name}, skipping")
            return args, kwargs
        
        # Check required arguments
        for arg_name in self.config.required_args:
            if arg_name not in kwargs:
                raise FabricError(
                    f"Missing required argument {arg_name} for pattern {self.name}",
                    pattern=self.name
                )
        
        # Prepare the prompt
        prompt_args = {**self.config.optional_args}
        for arg_name in self.config.required_args:
            prompt_args[arg_name] = kwargs[arg_name]
        
        try:
            # Format the prompt template
            prompt = self.config.prompt_template.format(**prompt_args)
            
            # Apply the pattern using the LLM adapter
            result = self.llm_adapter.apply_pattern(
                pattern_name=self.name,
                prompt=prompt,
                args=args,
                kwargs=kwargs
            )
            
            # Extract modified arguments
            modified_args = result.get("args", args)
            modified_kwargs = result.get("kwargs", kwargs)
            
            return modified_args, modified_kwargs
        except Exception as e:
            logger.error(f"Error applying pattern {self.name}: {e}")
            raise FabricError(f"Error applying pattern {self.name}: {e}", pattern=self.name)
    
    def process_result(self, result: Any) -> Any:
        """
        Process the result of a function call.
        
        Args:
            result: Function result
            
        Returns:
            Any: Processed result
            
        Raises:
            FabricError: If the result cannot be processed
        """
        # Check if LLM adapter is available
        if self.llm_adapter is None:
            logger.warning(f"No LLM adapter available for pattern {self.name}, skipping result processing")
            return result
        
        try:
            # Process the result using the LLM adapter
            processed_result = self.llm_adapter.process_pattern_result(
                pattern_name=self.name,
                result=result
            )
            
            return processed_result
        except Exception as e:
            logger.error(f"Error processing result for pattern {self.name}: {e}")
            raise FabricError(f"Error processing result for pattern {self.name}: {e}", pattern=self.name)

