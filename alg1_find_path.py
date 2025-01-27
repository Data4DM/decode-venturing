import numpy as np
import pandas as pd
from typing import Dict, List
from dataclasses import dataclass

# using [Investor Classification Framework for Pathfinding](https://claude.ai/chat/37933b85-ebce-4099-9886-196ad36ec653)
@dataclass
class Investor:
    id: str
    capacity: float
    idea_weight: float
    execution_weight: float

@dataclass
class Founder:
    id: str
    capital_needed: float
    idea_signals: Dict[str, float]
    execution_signals: Dict[str, float]

class PathFindingAlgorithm:
    def __init__(self, investors: List[Investor], founders: List[Founder]):
        self.investors = investors
        self.founders = founders
        self.state_space = ['idea', 'execution']
        self.matches = pd.DataFrame()
        
    def compute_benefit(self, investor: Investor, founder: Founder) -> float:
        idea_score = sum(founder.idea_signals.values()) * investor.idea_weight
        execution_score = sum(founder.execution_signals.values()) * investor.execution_weight
        return idea_score + execution_score
    
    def find_paths(self, max_iterations: int = 10, epsilon: float = 0.01):
        # Initialize matching distribution
        n_investors = len(self.investors)
        n_founders = len(self.founders)
        pi = np.ones((n_investors, n_founders)) / (n_investors * n_founders)
        
        for t in range(max_iterations):
            # Step 2: Primal (Path-Finding)
            benefits = np.zeros((n_investors, n_founders))
            for i, investor in enumerate(self.investors):
                for f, founder in enumerate(self.founders):
                    benefits[i,f] = self.compute_benefit(investor, founder)
            
            # Optimize matching (simplified version)
            pi_new = self._optimize_matching(pi, benefits)
            
            # Step 3: State Elicitation/Certification
            certified_paths = self._certify_paths(pi_new)
            
            # Step 4: Augment state space if needed
            if not all(certified_paths):
                self._augment_state_space()
                continue
                
            if np.all(np.abs(pi_new - pi) < epsilon):
                break
                
            pi = pi_new
            
        self.matches = self._convert_to_dataframe(pi)
        return self.matches
    
    def _optimize_matching(self, pi, benefits):
        # Simplified matching optimization
        # In practice, use linear programming solver
        return pi * benefits / np.sum(pi * benefits)
    
    def _certify_paths(self, pi):
        # Check if matches satisfy investor constraints
        return [True] * pi.shape[0]  # Simplified
    
    def _augment_state_space(self):
        # Add more granular signal interpretation
        self.state_space.append('market_validation')
    
    def _convert_to_dataframe(self, pi):
        matches = []
        for i, investor in enumerate(self.investors):
            for f, founder in enumerate(self.founders):
                if pi[i,f] > 0.01:  # Threshold
                    matches.append({
                        'investor_id': investor.id,
                        'founder_id': founder.id,
                        'match_probability': pi[i,f],
                        'idea_score': sum(founder.idea_signals.values()),
                        'execution_score': sum(founder.execution_signals.values())
                    })
        return pd.DataFrame(matches)

    def elicit_states(self, match_data):
        """Analyze patterns in successful/failed matches"""
        pattern_data = []
        for _, match in match_data.iterrows():
            successful = match['successful']
            # Extract patterns in investor preferences
            pattern = {
                'investor_type': match['investor_type'],
                'sector': match['sector'],
                'stage': match['stage'],
                'success': successful
            }
            pattern_data.append(pattern)
        
        return pd.DataFrame(pattern_data)