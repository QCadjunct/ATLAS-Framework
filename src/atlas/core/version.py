"""
Version information for ATLAS Framework.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Version components
MAJOR = 1
MINOR = 0
PATCH = 0

# Build information
BUILD_DATE = "2024-01-15"
BUILD_COMMIT = "main"

# API version for compatibility
API_VERSION = "v1"

def get_version_string() -> str:
    """
    Get formatted version string.
    
    Returns:
        str: Formatted version string with build information
    """
    return f"{__version__} (built {BUILD_DATE}, commit {BUILD_COMMIT})"

def get_api_version() -> str:
    """
    Get API version for compatibility checking.
    
    Returns:
        str: API version string
    """
    return API_VERSION

def is_compatible(required_version: str) -> bool:
    """
    Check if current version is compatible with required version.
    
    Args:
        required_version: Required version string (e.g., "1.0.0")
        
    Returns:
        bool: True if compatible, False otherwise
    """
    try:
        required_parts = [int(x) for x in required_version.split(".")]
        current_parts = list(__version_info__)
        
        # Major version must match
        if required_parts[0] != current_parts[0]:
            return False
            
        # Minor version must be >= required
        if len(required_parts) > 1:
            if current_parts[1] < required_parts[1]:
                return False
                
        # Patch version must be >= required
        if len(required_parts) > 2:
            if current_parts[1] == required_parts[1] and current_parts[2] < required_parts[2]:
                return False
                
        return True
        
    except (ValueError, IndexError):
        return False

