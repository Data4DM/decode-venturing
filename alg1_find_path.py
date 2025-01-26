#!/usr/bin/env python3

import os
import time
import pandas as pd
from itertools import product
from VCSimulator import VCSimulator  # Assuming VCSimulator is in VCSimulator.py
from subprocess import run

class PathFindingAlgorithm:
    def __init__(self, api_key: str, design_grid_path: str, vc_context_files: dict):
        """
        Initialize the Path-Finding Algorithm.

        :param api_key: OpenAI API key.
        :param design_grid_path: Path to the CSV file containing startup prompts.
        :param vc_context_files: Dictionary mapping VC names to their context file paths.
        """
        self.simulator = VCSimulator(api_key)
        self.design_grid_path = design_grid_path
        self.vc_context_files = vc_context_files
        self.vc_contexts = {vc: self.simulator.load_vc_context(path) 
                            for vc, path in vc_context_files.items()}
    
    def generate_startups(self):
        """Generate startup descriptions."""
        print("Generating startup descriptions...")
        startups_df = self.simulator.generate_startup_descriptions(self.design_grid_path)
        startups_df.to_csv('path_finding_startups.csv', index=False)
        print("Startup descriptions generated and saved to 'path_finding_startups.csv'.")
        return startups_df
    
    def simulate_vc_responses(self, startups_df):
        """Simulate VC responses for each startup."""
        all_vc_responses = []
        for vc_name, context in self.vc_contexts.items():
            print(f"Simulating responses from {vc_name}...")
            responses = self.simulator.get_vc_responses(startups_df, context, vc_name)
            all_vc_responses.append(responses)
        combined_responses = pd.concat(all_vc_responses)
        combined_responses.to_csv('path_finding_vc_responses.csv', index=False)
        print("VC responses simulated and saved to 'path_finding_vc_responses.csv'.")
        return combined_responses
    
    def calibrate_model(self):
        """Calibrate the model using the two-step calibration script."""
        print("Calibrating model using two-step calibration...")
        # Assuming the two-step calibration script is executable and in the same directory
        run(["python3", "2sim_based_2step_calib.py"], check=True)
        print("Calibration completed.")
    
    def plot_diagnostics(self):
        """Plot calibration diagnostics."""
        print("Plotting calibration diagnostics...")
        run(["python3", "3plot_diagnostics.py"], check=True)
        print("Diagnostics plotted.")
    
    def adjust_strategy(self):
        """
        Adjust the path based on calibration results.
        This is a placeholder for strategy adjustment logic.
        For example, prioritize startups with higher predicted investment probabilities.
        """
        print("Adjusting strategy based on calibration results...")
        # Load calibration results
        calibrated_df = pd.read_csv('decode-venturing/two_step_stan_output.csv')
        # Example adjustment: Select top 10% startups based on predicted probabilities
        # (This requires extracting posterior means from calibration)
        # Placeholder implementation:
        # TODO: Implement actual strategy adjustment based on calibration
        print("Strategy adjusted. (Implementation pending)")
    
    def run(self, iterations=5):
        """Run the Path-Finding Algorithm for a specified number of iterations."""
        for i in range(iterations):
            print(f"\n--- Iteration {i+1} ---")
            # Step 1: Generate startups
            startups_df = self.generate_startups()
            
            # Step 2: Simulate VC responses
            vc_responses = self.simulate_vc_responses(startups_df)
            
            # Step 3: Calibrate model
            self.calibrate_model()
            
            # Step 4: Plot diagnostics
            self.plot_diagnostics()
            
            # Step 5: Adjust strategy based on calibration
            self.adjust_strategy()
            
            print(f"--- Iteration {i+1} completed ---\n")
            time.sleep(2)  # Pause between iterations

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    design_grid_path = 'VC Design Grid.csv'
    vc_context_files = {
        "Marc Andreessen": 'Pmarca Blog Archives.pdf',
        "Bill Gurley": 'bill gurley.md'
    }
    
    path_finder = PathFindingAlgorithm(api_key, design_grid_path, vc_context_files)
    path_finder.run(iterations=3)  # Run for 3 iterations as an example

if __name__ == "__main__":
    main()
