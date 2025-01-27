"""
calibration algorithm (from investor's perspective). 
the need of this procedure is explained as follows: 
Imagine you're playing a video game where you need to match heroes with the right teammates. 
The game shows you a percentage score for each potential team-up, like "90% good match!" But if that number isn't calibrated properly, 
you might keep picking teams that look great on paper but lose in actual battles. In the startup world, this matters most when founders 
are trying to match with investors based on their team's background - like having PhDs or previous startup experience. 
A well-calibrated system means if it tells you "you have an 80% chance of matching with science-focused investors because of your PhD," that prediction should be trustworthy 
because looking at past similar cases, about 80% of PhD teams actually did get investment from those investors. This helps founders make better decisions about which 
investors to approach instead of wasting time on matches that look good but rarely work out in reality."

"""
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression

class InvestorCalibration:
    def __init__(self, n_bins=10, epsilon=0.05):
        self.n_bins = n_bins
        self.epsilon = epsilon
        self.bin_edges = np.linspace(0, 1, n_bins + 1)
        self.calibration_map = None
        
    def fit(self, predicted_probs: np.array, actual_outcomes: np.array):
        """Fit calibration model using historical data"""
        
        # Step 1: Bin probabilities
        bin_indices = np.digitize(predicted_probs, self.bin_edges) - 1
        
        # Step 2: Compute empirical frequencies
        self.bin_frequencies = []
        for bin_idx in range(self.n_bins):
            mask = bin_indices == bin_idx
            if np.any(mask):
                freq = np.mean(actual_outcomes[mask])
                self.bin_frequencies.append(freq)
            else:
                self.bin_frequencies.append(np.nan)
                
        # Step 3: Measure calibration error
        bin_midpoints = (self.bin_edges[:-1] + self.bin_edges[1:]) / 2
        calibration_errors = np.abs(
            np.array(self.bin_frequencies) - bin_midpoints
        )
        
        # Step 4: Fit isotonic regression for calibration
        ir = IsotonicRegression(out_of_bounds='clip')
        valid_mask = ~np.isnan(self.bin_frequencies)
        if np.any(valid_mask):
            self.calibration_map = ir.fit(
                bin_midpoints[valid_mask],
                np.array(self.bin_frequencies)[valid_mask]
            )
            
    def calibrate(self, predicted_probs: np.array) -> np.array:
        """Apply calibration to new predictions"""
        if self.calibration_map is None:
            return predicted_probs
        return self.calibration_map.predict(predicted_probs)
    
    def plot_reliability(self, predicted_probs, actual_outcomes):
        """Generate reliability diagram data"""
        bin_indices = np.digitize(predicted_probs, self.bin_edges) - 1
        plot_data = []
        
        for bin_idx in range(self.n_bins):
            mask = bin_indices == bin_idx
            if np.any(mask):
                mean_predicted = np.mean(predicted_probs[mask])
                mean_actual = np.mean(actual_outcomes[mask])
                n_samples = np.sum(mask)
                
                plot_data.append({
                    'bin_start': self.bin_edges[bin_idx],
                    'bin_end': self.bin_edges[bin_idx + 1],
                    'predicted_prob': mean_predicted,
                    'actual_freq': mean_actual,
                    'n_samples': n_samples
                })
                
        return pd.DataFrame(plot_data)

    def get_calibration_stats(self):
        """Return calibration metrics"""
        valid_freqs = [f for f in self.bin_frequencies if not np.isnan(f)]
        if not valid_freqs:
            return {}
            
        bin_midpoints = (self.bin_edges[:-1] + self.bin_edges[1:]) / 2
        valid_bins = ~np.isnan(self.bin_frequencies)
        
        return {
            'max_calibration_error': np.max(np.abs(
                np.array(valid_freqs) - bin_midpoints[valid_bins]
            )),
            'mean_calibration_error': np.mean(np.abs(
                np.array(valid_freqs) - bin_midpoints[valid_bins]
            )),
            'n_reliable_bins': len(valid_freqs)
        }