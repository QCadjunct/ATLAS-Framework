"""
Enum loader for the ATLAS Framework.

This module provides a loader for creating enums from dictionaries,
enabling extensible, dictionary-driven enums.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

from atlas.core.exceptions import ConfigError


T = TypeVar("T", bound=Enum)


class EnumLoader:
    """
    Loader for creating enums from dictionaries.
    
    This class provides methods for loading enum definitions from
    dictionaries and files, enabling extensible, dictionary-driven enums.
    """
    
    @staticmethod
    def create_enum_from_dict(
        name: str,
        values: Dict[str, Any],
        base_enum: Optional[Type[Enum]] = None,
        methods: Optional[Dict[str, Callable[..., Any]]] = None
    ) -> Type[Enum]:
        """
        Create an enum from a dictionary.
        
        Args:
            name: Name of the enum
            values: Dictionary of enum values
            base_enum: Optional base enum to inherit from
            methods: Optional dictionary of methods to add to the enum
            
        Returns:
            Type[Enum]: Created enum class
            
        Raises:
            ConfigError: If the enum cannot be created
        """
        try:
            # Determine the base classes
            bases = (base_enum,) if base_enum else (Enum,)
            
            # Create the enum namespace
            namespace = {
                "__module__": "atlas.enums",
                **{key: value for key, value in values.items()},
            }
            
            # Add methods if provided
            if methods:
                namespace.update(methods)
            
            # Create the enum class
            return cast(Type[Enum], type(name, bases, namespace))
        except Exception as e:
            raise ConfigError(f"Failed to create enum {name}: {e}", config_key=name)
    
    @staticmethod
    def load_enum_from_file(
        file_path: Union[str, Path],
        base_enum: Optional[Type[Enum]] = None,
        methods: Optional[Dict[str, Callable[..., Any]]] = None
    ) -> Type[Enum]:
        """
        Load an enum from a file.
        
        Args:
            file_path: Path to the enum definition file
            base_enum: Optional base enum to inherit from
            methods: Optional dictionary of methods to add to the enum
            
        Returns:
            Type[Enum]: Loaded enum class
            
        Raises:
            ConfigError: If the file cannot be loaded or the enum cannot be created
        """
        path = Path(file_path)
        
        if not path.exists():
            raise ConfigError(f"Enum definition file not found: {path}", config_key="file_path")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                if path.suffix == ".json":
                    definition = json.load(f)
                else:
                    raise ConfigError(
                        f"Unsupported file format: {path.suffix}", 
                        config_key="file_format"
                    )
        except Exception as e:
            raise ConfigError(f"Failed to load enum definition file: {e}", config_key="file_load")
        
        # Extract the enum name and values
        if "name" not in definition or "values" not in definition:
            raise ConfigError(
                "Enum definition must contain 'name' and 'values'", 
                config_key="definition"
            )
        
        name = definition["name"]
        values = definition["values"]
        
        # Create the enum
        return EnumLoader.create_enum_from_dict(name, values, base_enum, methods)
    
    @staticmethod
    def extend_enum(
        base_enum: Type[T],
        additional_values: Dict[str, Any],
        methods: Optional[Dict[str, Callable[..., Any]]] = None
    ) -> Type[T]:
        """
        Extend an existing enum with additional values.
        
        Args:
            base_enum: Base enum to extend
            additional_values: Dictionary of additional enum values
            methods: Optional dictionary of methods to add to the enum
            
        Returns:
            Type[T]: Extended enum class
            
        Raises:
            ConfigError: If the enum cannot be extended
        """
        try:
            # Create a new namespace with existing values
            namespace = {
                "__module__": "atlas.enums",
                **{key: value for key, value in base_enum.__members__.items()},
                **additional_values,
            }
            
            # Add methods if provided
            if methods:
                namespace.update(methods)
            
            # Create the extended enum class
            return cast(Type[T], type(base_enum.__name__, (base_enum,), namespace))
        except Exception as e:
            raise ConfigError(f"Failed to extend enum {base_enum.__name__}: {e}", config_key=base_enum.__name__)

