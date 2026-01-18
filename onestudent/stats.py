"""Statistics Tracking for Success Rates"""

import json
from pathlib import Path
from typing import Dict


class Stats:
    """Track verification success rates by organization"""
    
    def __init__(self):
        self.file = Path(__file__).parent / "stats.json"
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load stats from file"""
        if self.file.exists():
            try:
                return json.loads(self.file.read_text())
            except:
                pass
        return {"total": 0, "success": 0, "failed": 0, "orgs": {}}
    
    def _save(self):
        """Save stats to file"""
        try:
            self.file.write_text(json.dumps(self.data, indent=2))
        except Exception as e:
            print(f"Warning: Could not save stats: {e}")
    
    def record(self, org_name: str, success: bool):
        """
        Record verification result
        
        Args:
            org_name: Organization/university name
            success: Whether verification succeeded
        """
        self.data["total"] += 1
        self.data["success" if success else "failed"] += 1
        
        if org_name not in self.data["orgs"]:
            self.data["orgs"][org_name] = {"success": 0, "failed": 0}
        self.data["orgs"][org_name]["success" if success else "failed"] += 1
        self._save()
    
    def get_rate(self, org_name: str = None) -> float:
        """
        Get success rate percentage
        
        Args:
            org_name: Specific organization or None for overall
            
        Returns:
            Success rate as percentage (0-100)
        """
        if org_name:
            o = self.data["orgs"].get(org_name, {})
            total = o.get("success", 0) + o.get("failed", 0)
            return o.get("success", 0) / total * 100 if total else 50.0
        return self.data["success"] / self.data["total"] * 100 if self.data["total"] else 0.0
    
    def get_stats_summary(self) -> str:
        """Get human-readable stats summary"""
        if self.data["total"] == 0:
            return "No verifications yet"
        
        return (
            f"Total: {self.data['total']} | "
            f"✅ {self.data['success']} | "
            f"❌ {self.data['failed']} | "
            f"Success Rate: {self.get_rate():.1f}%"
        )


# Global stats instance
stats = Stats()


def select_university_weighted(universities: list) -> dict:
    """
    Select university with weighted random selection
    
    Args:
        universities: List of university dicts with 'weight' key
        
    Returns:
        Selected university dict
    """
    import random
    
    # Calculate adjusted weights based on historical success rates
    weights = []
    for uni in universities:
        # Base weight * (actual success rate / 50 as baseline)
        adjusted_weight = uni["weight"] * (stats.get_rate(uni["name"]) / 50)
        weights.append(max(1, adjusted_weight))  # Minimum weight of 1
    
    # Weighted random selection
    total = sum(weights)
    r = random.uniform(0, total)
    
    cumulative = 0
    for uni, weight in zip(universities, weights):
        cumulative += weight
        if r <= cumulative:
            return uni
    
    # Fallback to first university
    return universities[0]
