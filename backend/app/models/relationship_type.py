from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON
from datetime import datetime
from .base import Base


class RelationshipType(Base):
    __tablename__ = "relationship_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Extensibility and organization
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    
    # Relationship calculation rules stored as JSON
    # Example: {"opposite": "child", "spouse_relation": "step-parent", "sibling_relation": "aunt_uncle"}
    calculation_rules = Column(JSON, nullable=True)
    
    # Relationship characteristics
    is_reciprocal = Column(Boolean, default=False, nullable=False)  # True for relationships like "spouse", "sibling"
    generation_offset = Column(Integer, default=0, nullable=False)  # -1 for parent, +1 for child, 0 for spouse/sibling
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        status = "active" if self.is_active else "inactive"
        reciprocal = "reciprocal" if self.is_reciprocal else "directional"
        return f"<RelationshipType('{self.display_name}' [{self.name}] - {status}, {reciprocal}, gen_offset={self.generation_offset})>"

    def __str__(self):
        return f"{self.display_name} ({self.name})"

    @classmethod
    def get_default_relationship_types(cls):
        """Return default relationship types to seed the database"""
        return [
            {
                "name": "parent",
                "display_name": "Parent",
                "description": "Biological or adoptive parent",
                "generation_offset": -1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "child",
                    "spouse_relation": "step_parent",
                    "sibling_relation": "aunt_uncle",
                    "parent_relation": "grandparent"
                },
                "sort_order": 1
            },
            {
                "name": "child",
                "display_name": "Child", 
                "description": "Biological or adoptive child",
                "generation_offset": 1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "parent",
                    "spouse_relation": "step_child",
                    "sibling_relation": "niece_nephew",
                    "child_relation": "grandchild"
                },
                "sort_order": 2
            },
            {
                "name": "spouse",
                "display_name": "Spouse",
                "description": "Married partner",
                "generation_offset": 0,
                "is_reciprocal": True,
                "calculation_rules": {
                    "opposite": "spouse",
                    "parent_relation": "parent_in_law",
                    "child_relation": "step_child",
                    "sibling_relation": "sibling_in_law"
                },
                "sort_order": 3
            },
            {
                "name": "sibling",
                "display_name": "Sibling",
                "description": "Brother or sister",
                "generation_offset": 0,
                "is_reciprocal": True,
                "calculation_rules": {
                    "opposite": "sibling",
                    "parent_relation": "aunt_uncle",
                    "child_relation": "niece_nephew",
                    "spouse_relation": "sibling_in_law"
                },
                "sort_order": 4
            },
            {
                "name": "grandparent",
                "display_name": "Grandparent",
                "description": "Parent's parent",
                "generation_offset": -2,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "grandchild",
                    "spouse_relation": "step_grandparent",
                    "sibling_relation": "great_aunt_uncle"
                },
                "sort_order": 5
            },
            {
                "name": "grandchild",
                "display_name": "Grandchild",
                "description": "Child's child",
                "generation_offset": 2,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "grandparent",
                    "spouse_relation": "step_grandchild"
                },
                "sort_order": 6
            },
            {
                "name": "step_parent",
                "display_name": "Step Parent",
                "description": "Spouse's child from previous relationship",
                "generation_offset": -1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "step_child"
                },
                "sort_order": 7
            },
            {
                "name": "step_child",
                "display_name": "Step Child",
                "description": "Spouse's child from previous relationship",
                "generation_offset": 1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "step_parent"
                },
                "sort_order": 8
            },
            {
                "name": "aunt_uncle",
                "display_name": "Aunt/Uncle",
                "description": "Parent's sibling",
                "generation_offset": -1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "niece_nephew",
                    "spouse_relation": "aunt_uncle_in_law"
                },
                "sort_order": 9
            },
            {
                "name": "niece_nephew",
                "display_name": "Niece/Nephew",
                "description": "Sibling's child",
                "generation_offset": 1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "aunt_uncle"
                },
                "sort_order": 10
            },
            {
                "name": "guardian",
                "display_name": "Guardian",
                "description": "Legal guardian or caregiver",
                "generation_offset": -1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "ward"
                },
                "sort_order": 11
            },
            {
                "name": "ward",
                "display_name": "Ward",
                "description": "Person under guardianship",
                "generation_offset": 1,
                "is_reciprocal": False,
                "calculation_rules": {
                    "opposite": "guardian"
                },
                "sort_order": 12
            }
        ]