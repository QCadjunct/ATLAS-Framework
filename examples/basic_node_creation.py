#!/usr/bin/env python3
"""
ATLAS Framework - Simple Example: Basic Node Creation

This example demonstrates the fundamental concepts of ATLAS Framework:
- Creating nodes without inheritance
- Using configuration-driven development
- Basic behavior execution
- Type-safe operations with Pydantic v2

Requirements:
- Python 3.11+
- ATLAS Framework installed
"""

import asyncio
import json
from typing import Dict, Any, List
from pathlib import Path

# ATLAS Framework imports
from atlas import ConfigurationManager, ATLASNode
from atlas.enums import NodeLabelType, FuelGroupType, ValidationStatusType
from atlas.models.behaviors import ComputationBehavior
from atlas.utils.logging import get_logger

# Setup logging
logger = get_logger(__name__)


async def main():
    """
    Simple example demonstrating basic ATLAS Framework usage.
    
    This example shows:
    1. Configuration loading
    2. Node creation without inheritance
    3. Basic behavior execution
    4. Type-safe operations
    """
    
    print("🚀 ATLAS Framework - Simple Example: Basic Node Creation")
    print("=" * 60)
    
    # Step 1: Load configuration
    print("\n📋 Step 1: Loading Configuration")
    config_path = Path(__file__).parent / "config" / "simple_config.json"
    
    # Create simple configuration if it doesn't exist
    if not config_path.exists():
        await create_simple_config(config_path)
    
    config_manager = ConfigurationManager.from_file(str(config_path))
    print(f"✅ Configuration loaded from: {config_path}")
    
    # Step 2: Create energy term nodes
    print("\n🔧 Step 2: Creating Energy Term Nodes")
    
    # Create a solar energy node
    solar_node = config_manager.create_energy_term(
        term_name="Solar Photovoltaic",
        definition="Technology that converts sunlight directly into electricity using semiconductor materials",
        fuel_group=FuelGroupType.RENEWABLE,
        additional_properties={
            "efficiency_rating": 0.22,
            "technology_type": "crystalline_silicon",
            "typical_capacity_mw": 100.0
        }
    )
    
    print(f"✅ Created Solar Node:")
    print(f"   - ID: {solar_node.node_id}")
    print(f"   - Labels: {[label.value for label in solar_node.labels]}")
    print(f"   - Fuel Group: {solar_node.properties.get('fuel_group')}")
    print(f"   - Efficiency: {solar_node.properties.get('efficiency_rating')}")
    
    # Create a wind energy node
    wind_node = config_manager.create_energy_term(
        term_name="Wind Turbine",
        definition="Device that converts kinetic energy from wind into electrical energy",
        fuel_group=FuelGroupType.RENEWABLE,
        additional_properties={
            "efficiency_rating": 0.35,
            "technology_type": "horizontal_axis",
            "typical_capacity_mw": 3.0
        }
    )
    
    print(f"✅ Created Wind Node:")
    print(f"   - ID: {wind_node.node_id}")
    print(f"   - Labels: {[label.value for label in wind_node.labels]}")
    print(f"   - Technology: {wind_node.properties.get('technology_type')}")
    
    # Create a fossil fuel node for comparison
    coal_node = config_manager.create_energy_term(
        term_name="Coal Power Plant",
        definition="Thermal power station that burns coal to generate electricity",
        fuel_group=FuelGroupType.FOSSIL,
        additional_properties={
            "efficiency_rating": 0.33,
            "carbon_intensity_kg_per_mwh": 820.0,
            "typical_capacity_mw": 500.0
        }
    )
    
    print(f"✅ Created Coal Node:")
    print(f"   - ID: {coal_node.node_id}")
    print(f"   - Carbon Intensity: {coal_node.properties.get('carbon_intensity_kg_per_mwh')} kg/MWh")
    
    # Step 3: Demonstrate type safety with enums
    print("\n🔒 Step 3: Demonstrating Type Safety")
    
    # Show enum properties in action
    print(f"Solar Node Properties:")
    print(f"   - Is Renewable: {any(label.is_renewable for label in solar_node.labels)}")
    print(f"   - Carbon Category: {solar_node.carbon_category}")
    print(f"   - Validation Status: {solar_node.validation_status.value}")
    print(f"   - Can Transition To: {[status.value for status in solar_node.validation_status.can_transition_to]}")
    
    # Step 4: Execute behaviors
    print("\n⚡ Step 4: Executing Node Behaviors")
    
    # Execute computation behavior on solar node
    computation_context = {
        "analysis_type": "efficiency_analysis",
        "weather_data": {
            "solar_irradiance": 1000,  # W/m²
            "temperature": 25,         # °C
            "wind_speed": 2.5         # m/s
        },
        "location_data": {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "elevation": 16
        }
    }
    
    try:
        solar_computation = await solar_node.execute_behavior("computation", computation_context)
        print(f"✅ Solar Computation Result:")
        print(f"   - Success: {solar_computation.get('success', False)}")
        print(f"   - Efficiency Score: {solar_computation.get('efficiency_score', 'N/A')}")
        print(f"   - Performance Ratio: {solar_computation.get('performance_ratio', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️  Solar computation failed: {e}")
    
    # Execute behavior on wind node
    wind_context = {
        "analysis_type": "wind_analysis",
        "weather_data": {
            "wind_speed": 12.5,        # m/s
            "wind_direction": 270,     # degrees
            "air_density": 1.225       # kg/m³
        }
    }
    
    try:
        wind_computation = await wind_node.execute_behavior("computation", wind_context)
        print(f"✅ Wind Computation Result:")
        print(f"   - Success: {wind_computation.get('success', False)}")
        print(f"   - Power Output: {wind_computation.get('power_output_mw', 'N/A')} MW")
        print(f"   - Capacity Factor: {wind_computation.get('capacity_factor', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️  Wind computation failed: {e}")
    
    # Step 5: Demonstrate identical interfaces
    print("\n🔄 Step 5: Demonstrating Identical Interfaces (DRY Principle)")
    
    nodes = [solar_node, wind_node, coal_node]
    
    print("All nodes use identical interfaces despite different types:")
    for i, node in enumerate(nodes, 1):
        print(f"\n{i}. Node: {node.properties.get('term_name', 'Unknown')}")
        print(f"   - Type: {type(node).__name__}")  # Same class for all!
        print(f"   - Labels: {[label.value for label in node.labels]}")
        print(f"   - Behaviors: {len(node.behaviors)} configured")
        print(f"   - Properties: {len(node.properties)} total")
        
        # All nodes support the same operations
        print(f"   - Supports computation: {node.has_behavior('computation')}")
        print(f"   - Supports analysis: {node.has_behavior('analysis')}")
        print(f"   - Validation status: {node.validation_status.value}")
    
    # Step 6: Show configuration-driven flexibility
    print("\n📊 Step 6: Configuration-Driven Flexibility")
    
    # Create a custom node type on the fly
    custom_node = config_manager.create_node(
        node_type="custom_energy_storage",
        properties={
            "term_name": "Lithium-Ion Battery",
            "definition": "Rechargeable battery technology using lithium ions",
            "fuel_group": "storage",
            "energy_density_wh_per_kg": 250,
            "cycle_life": 5000,
            "round_trip_efficiency": 0.95
        },
        labels=[NodeLabelType.ENERGY_TERM, NodeLabelType.TECHNICAL_CONCEPT]
    )
    
    print(f"✅ Created Custom Storage Node:")
    print(f"   - ID: {custom_node.node_id}")
    print(f"   - Energy Density: {custom_node.properties.get('energy_density_wh_per_kg')} Wh/kg")
    print(f"   - Round-trip Efficiency: {custom_node.properties.get('round_trip_efficiency')}")
    
    # Step 7: Summary and next steps
    print("\n🎯 Summary")
    print("=" * 40)
    print("✅ Successfully demonstrated:")
    print("   - Configuration-driven node creation")
    print("   - Type-safe operations with Pydantic v2")
    print("   - Zero code duplication (DRY principle)")
    print("   - Identical interfaces for all node types")
    print("   - Behavior execution and composition")
    print("   - Enum-based constraints and validation")
    
    print(f"\n📊 Created {len(nodes) + 1} nodes with 0 lines of inheritance code!")
    print("🚀 Ready for more complex examples!")
    
    # Optional: Save nodes to JSON for inspection
    output_file = Path(__file__).parent / "output" / "created_nodes.json"
    output_file.parent.mkdir(exist_ok=True)
    
    nodes_data = []
    for node in nodes + [custom_node]:
        nodes_data.append({
            "node_id": node.node_id,
            "labels": [label.value for label in node.labels],
            "properties": node.properties,
            "behavior_count": len(node.behaviors),
            "validation_status": node.validation_status.value
        })
    
    with open(output_file, 'w') as f:
        json.dump(nodes_data, f, indent=2, default=str)
    
    print(f"\n💾 Node data saved to: {output_file}")


async def create_simple_config(config_path: Path) -> None:
    """
    Create a simple configuration file for the example.
    
    Args:
        config_path: Path where to save the configuration
    """
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    simple_config = {
        "version": "1.0",
        "metadata": {
            "name": "Simple ATLAS Configuration",
            "description": "Basic configuration for ATLAS Framework examples",
            "created": "2024-01-15T10:00:00Z"
        },
        "node_types": {
            "energy_term": {
                "description": "Basic energy terminology nodes",
                "labels": ["EnergyTerm", "TaxonomyNode"],
                "default_properties": {
                    "extraction_confidence": 0.8,
                    "validation_status": "pending"
                },
                "required_fields": ["term_name", "definition", "fuel_group"],
                "behaviors": [
                    {
                        "type": "computation",
                        "behavior_id": "basic_computation",
                        "description": "Basic computation for energy metrics",
                        "computation_function": "_compute_basic_metrics",
                        "cache_ttl": 300,
                        "priority": 100,
                        "parameters": {
                            "include_efficiency": True,
                            "include_environmental": True
                        }
                    }
                ]
            }
        },
        "global_settings": {
            "default_cache_ttl": 300,
            "max_behavior_execution_time": 60,
            "validation_strictness": "medium"
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(simple_config, f, indent=2)
    
    print(f"📝 Created simple configuration at: {config_path}")


if __name__ == "__main__":
    """
    Run the simple example.
    
    This demonstrates the core ATLAS Framework concepts without complexity.
    """
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Example interrupted by user")
    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"\n❌ Example failed: {e}")
        raise

