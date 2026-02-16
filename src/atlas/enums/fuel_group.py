"""
Fuel group enumeration for energy taxonomy.

This module defines the FuelGroupType enum, which represents different
categories of energy sources.
"""

from enum import Enum
from typing import List, Set


class FuelGroupType(str, Enum):
    """
    Enumeration of fuel groups for energy taxonomy.
    
    This enum represents different categories of energy sources,
    with properties to determine their characteristics.
    """
    
    ALTERNATIVE = "alternative"
    COAL = "coal"
    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    NUCLEAR = "nuclear"
    PETROLEUM = "petroleum"
    RENEWABLE = "renewable"
    
    @property
    def is_renewable(self) -> bool:
        """
        Check if this fuel group is considered renewable.
        
        Returns:
            bool: True if the fuel group is renewable, False otherwise
        """
        return self.value in {
            self.RENEWABLE.value,
            self.ALTERNATIVE.value,
        }
    
    @property
    def is_fossil_fuel(self) -> bool:
        """
        Check if this fuel group is considered a fossil fuel.
        
        Returns:
            bool: True if the fuel group is a fossil fuel, False otherwise
        """
        return self.value in {
            self.COAL.value,
            self.NATURAL_GAS.value,
            self.PETROLEUM.value,
        }
    
    @property
    def carbon_intensity(self) -> float:
        """
        Get the relative carbon intensity of this fuel group.
        
        Higher values indicate higher carbon emissions per unit of energy.
        
        Returns:
            float: Relative carbon intensity value (0.0 to 1.0)
        """
        intensity_map = {
            self.RENEWABLE.value: 0.1,
            self.ALTERNATIVE.value: 0.3,
            self.NUCLEAR.value: 0.2,
            self.NATURAL_GAS.value: 0.6,
            self.PETROLEUM.value: 0.8,
            self.COAL.value: 1.0,
            self.ELECTRICITY.value: 0.5,  # Average mix
        }
        return intensity_map.get(self.value, 0.5)
    
    @property
    def related_fuel_groups(self) -> List["FuelGroupType"]:
        """
        Get a list of related fuel groups.
        
        Returns:
            List[FuelGroupType]: List of related fuel groups
        """
        relations = {
            self.RENEWABLE.value: [self.ALTERNATIVE, self.ELECTRICITY],
            self.ALTERNATIVE.value: [self.RENEWABLE, self.ELECTRICITY],
            self.NUCLEAR.value: [self.ELECTRICITY],
            self.NATURAL_GAS.value: [self.FOSSIL_FUEL, self.ELECTRICITY],
            self.PETROLEUM.value: [self.FOSSIL_FUEL],
            self.COAL.value: [self.FOSSIL_FUEL, self.ELECTRICITY],
            self.ELECTRICITY.value: [self.RENEWABLE, self.NUCLEAR, self.COAL, self.NATURAL_GAS],
        }
        return relations.get(self.value, [])
    
    @property
    def common_technologies(self) -> Set[str]:
        """
        Get a set of common technologies associated with this fuel group.
        
        Returns:
            Set[str]: Set of technology names
        """
        tech_map = {
            self.RENEWABLE.value: {
                "Solar Panel", "Wind Turbine", "Hydroelectric Dam", 
                "Geothermal Plant", "Biomass Reactor"
            },
            self.ALTERNATIVE.value: {
                "Hydrogen Fuel Cell", "Biofuel Refinery", 
                "Synthetic Fuel Plant", "Electric Vehicle"
            },
            self.NUCLEAR.value: {
                "Nuclear Reactor", "Nuclear Power Plant", 
                "Uranium Enrichment", "Nuclear Waste Storage"
            },
            self.NATURAL_GAS.value: {
                "Natural Gas Plant", "Combined Cycle Gas Turbine", 
                "Gas Pipeline", "LNG Terminal"
            },
            self.PETROLEUM.value: {
                "Oil Refinery", "Oil Rig", "Petroleum Pipeline", 
                "Gasoline Engine", "Diesel Generator"
            },
            self.COAL.value: {
                "Coal Power Plant", "Coal Mine", "Coal Gasification", 
                "Carbon Capture and Storage"
            },
            self.ELECTRICITY.value: {
                "Power Grid", "Transformer", "Substation", 
                "Battery Storage", "Smart Grid"
            },
        }
        return tech_map.get(self.value, set())
    
    @classmethod
    def from_string(cls, value: str) -> "FuelGroupType":
        """
        Create a FuelGroupType from a string, with fuzzy matching.
        
        Args:
            value: String representation of the fuel group
            
        Returns:
            FuelGroupType: The matching fuel group type
            
        Raises:
            ValueError: If no matching fuel group is found
        """
        value = value.lower().strip()
        
        # Direct match
        try:
            return cls(value)
        except ValueError:
            pass
        
        # Fuzzy match
        if "renew" in value or "solar" in value or "wind" in value or "hydro" in value:
            return cls.RENEWABLE
        elif "alter" in value or "bio" in value or "hydrogen" in value:
            return cls.ALTERNATIVE
        elif "nucl" in value or "atom" in value or "fission" in value:
            return cls.NUCLEAR
        elif "gas" in value or "methane" in value:
            return cls.NATURAL_GAS
        elif "petro" in value or "oil" in value or "diesel" in value or "gasoline" in value:
            return cls.PETROLEUM
        elif "coal" in value:
            return cls.COAL
        elif "electr" in value or "power" in value or "grid" in value:
            return cls.ELECTRICITY
        
        raise ValueError(f"No matching fuel group found for: {value}")

