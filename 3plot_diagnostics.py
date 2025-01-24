#!/usr/bin/env python3

"""
3plot_diagnostics.py
- Loads investor response data + a saved Stan posterior to produce diagnostic plots:
  1) A calibration scatter + binned line
  2) A 2D pivot heatmap of (execution_score, idea_score) vs. invests
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cmdstanpy import from_csv

# Path to your Stan output folder or CSV
PATH_TO_VC_RESP = "decode-venturing/vc_investor_responses.csv"
PATH_TO_POSTERIOR_CSV = "decode-venturing/two_step_stan_output"

def main():
    # 1) Load the data
    df = pd.read_csv(PATH_TO_VC_RESP)

    # 2) Load Stan fit
    fit = from_csv(PATH_TO_POSTERIOR_CSV)
    draws = fit.draws_pd()

    # 3) Extract posterior means
    alpha0_mean = draws["alpha0"].mean()
    alpha_exec_mean = draws["alpha_exec"].mean()
    alpha_idea_mean = draws["alpha_idea"].mean()
    print("Posterior means:", alpha0_mean, alpha_exec_mean, alpha_idea_mean)

    # 4) Compute predicted probabilities via logistic
    #    (We treat execution_score & idea_score as continuous inputs)
    linpred = alpha0_mean + alpha_exec_mean * df["execution_score"] + alpha_idea_mean * df["idea_score"]
    df["pred_prob"] = 1.0 / (1.0 + np.exp(-linpred))

    # 5) SCATTER PLOT: predicted prob vs actual invests
    plt.figure(figsize=(7,5))
    
    # (A) Add a tiny jitter to y so the 0/1 points can be seen better
    #     because they all line up exactly at 0 or 1 otherwise
    y_jitter = np.random.uniform(-0.02, 0.02, size=len(df))
    y_vals = df["would_invest"] + y_jitter
    
    plt.scatter(df["pred_prob"], y_vals, alpha=0.4, label="Individual Observations")
    
    plt.xlabel("Predicted Probability of Invest")
    plt.ylabel("Actual would_invest (0/1)")
    plt.title("Calibration: Predicted vs. Actual")
    
    # (B) Also plot a "binned" calibration curve 
    #     We'll bucket the predicted probability into bins, compute average y
    num_bins = 10
    df["bin"] = pd.cut(df["pred_prob"], bins=np.linspace(0,1,num_bins+1), include_lowest=True)
    bin_means = df.groupby("bin").agg({
        "pred_prob": "mean",
        "would_invest": "mean"
    }).reset_index()
    
    plt.plot(bin_means["pred_prob"], bin_means["would_invest"], color="red", marker="o", label="Binned Calibration")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 6) 2D PIVOT TABLE: (execution_score, idea_score) -> mean invests
    #    Then heatmap it.
    pivot_df = df.groupby(["execution_score", "idea_score"], as_index=False)["would_invest"].mean()
    # Use pivot(index=..., columns=..., values=...)
    pivot_table = pivot_df.pivot(index="execution_score", columns="idea_score", values="would_invest")

    plt.figure(figsize=(7,5))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Mean Probability of Invest by (Execution, Idea)")
    plt.xlabel("Idea Score")
    plt.ylabel("Execution Score")
    plt.tight_layout()
    plt.show()

    print("Done. See updated calibration + pivot heatmap in the output.")

if __name__ == "__main__":
    main()
