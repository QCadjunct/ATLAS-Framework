"""
FABRIC registry class for the ATLAS Framework.

This module provides a registry for FABRIC patterns,
enabling pattern discovery and management.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from atlas.core.exceptions import FabricError
from atlas.fabric.pattern import FabricPattern


logger = logging.getLogger(__name__)


class FabricRegistry:
    """
    Registry for FABRIC patterns.
    
    This class provides methods for discovering, loading, and managing
    FABRIC patterns in the ATLAS Framework.
    """
    
    def __init__(
        self,
        patterns_dir: Optional[str] = None,
        llm_adapter: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize the FABRIC registry.
        
        Args:
            patterns_dir: Optional directory containing pattern files
            llm_adapter: Optional LLM adapter for applying patterns
            config: Optional configuration dictionary
        """
        self.patterns_dir = patterns_dir
        self.llm_adapter = llm_adapter
        self.config = config or {}
        self._patterns: Dict[str, FabricPattern] = {}
        self._loaded_patterns: Set[str] = set()
    
    def initialize(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the registry with configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        if config:
            self.config.update(config)
        
        # Set patterns directory from config if not already set
        if self.patterns_dir is None and "patterns_dir" in self.config:
            self.patterns_dir = self.config["patterns_dir"]
        
        # Load default patterns if specified
        if "default_patterns" in self.config:
            for pattern_name in self.config["default_patterns"]:
                self.load_pattern(pattern_name)
    
    def discover_patterns(self) -> List[str]:
        """
        Discover available patterns.
        
        Returns:
            List[str]: List of available pattern names
        """
        if self.patterns_dir is None:
            logger.warning("No patterns directory specified, cannot discover patterns")
            return []
        
        patterns = []
        
        # Check if the directory exists
        path = Path(self.patterns_dir)
        if not path.exists() or not path.is_dir():
            logger.warning(f"Patterns directory {self.patterns_dir} not found")
            return []
        
        # Find all JSON files in the directory
        for file_path in path.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    pattern_data = json.load(f)
                
                if "name" in pattern_data:
                    patterns.append(pattern_data["name"])
            except Exception as e:
                logger.warning(f"Failed to load pattern from {file_path}: {e}")
        
        return patterns
    
    def load_pattern(self, pattern_name: str) -> FabricPattern:
        """
        Load a pattern by name.
        
        Args:
            pattern_name: Name of the pattern to load
            
        Returns:
            FabricPattern: Loaded pattern
            
        Raises:
            FabricError: If the pattern cannot be loaded
        """
        # Check if already loaded
        if pattern_name in self._loaded_patterns:
            return self._patterns[pattern_name]
        
        # Try to load from file
        try:
            pattern = FabricPattern(pattern_name, llm_adapter=self.llm_adapter)
            self._patterns[pattern_name] = pattern
            self._loaded_patterns.add(pattern_name)
            return pattern
        except Exception as e:
            logger.error(f"Failed to load pattern {pattern_name}: {e}")
            raise FabricError(f"Failed to load pattern {pattern_name}: {e}", pattern=pattern_name)
    
    def get_pattern(self, pattern_name: str) -> Optional[FabricPattern]:
        """
        Get a pattern by name.
        
        Args:
            pattern_name: Name of the pattern to get
            
        Returns:
            Optional[FabricPattern]: Pattern, or None if not found
        """
        # Check if already loaded
        if pattern_name in self._loaded_patterns:
            return self._patterns[pattern_name]
        
        # Try to load
        try:
            return self.load_pattern(pattern_name)
        except Exception:
            logger.warning(f"Pattern {pattern_name} not found")
            return None
    
    def register_pattern(self, pattern: FabricPattern) -> None:
        """
        Register a pattern.
        
        Args:
            pattern: Pattern to register
            
        Raises:
            FabricError: If the pattern is already registered
        """
        if pattern.name in self._loaded_patterns:
            raise FabricError(f"Pattern {pattern.name} already registered", pattern=pattern.name)
        
        self._patterns[pattern.name] = pattern
        self._loaded_patterns.add(pattern.name)
    
    def unregister_pattern(self, pattern_name: str) -> None:
        """
        Unregister a pattern.
        
        Args:
            pattern_name: Name of the pattern to unregister
        """
        if pattern_name in self._loaded_patterns:
            del self._patterns[pattern_name]
            self._loaded_patterns.remove(pattern_name)
    
    def get_loaded_patterns(self) -> List[str]:
        """
        Get the names of loaded patterns.
        
        Returns:
            List[str]: List of loaded pattern names
        """
        return list(self._loaded_patterns)

