#!/usr/bin/env python3

"""
2sim_based_2step_calib.py
- Reads simulated or real investor response data (vc_investor_responses.csv).
- Prepares data for a multi-logit or 2-step Stan model (observation->states->action).
- Fits the Stan model, saves results.
"""

import os
import pandas as pd
import numpy as np
from cmdstanpy import CmdStanModel

# Example Stan code snippet: observation->states->action.
PATH_TO_VC_RESP = "decode-venturing/vc_investor_responses.csv"
PATH_TO_STAN_CODE = "decode-venturing/stan/two_step_model.stan" 
PATH_TO_POSTERIOR_CSV = "decode-venturing/two_step_stan_output"


def main():
    # 1) Read the investor response data
    df = pd.read_csv(PATH_TO_VC_RESP)
    print("Loaded responses shape:", df.shape)

    # 2) Build Stan data
    # We'll treat each row as one observation
    # Let "execution_score" and "idea_score" be the states
    # Let "would_invest" be the 0/1 outcome
    stan_data = {
        "N": len(df),
        "exec_score": df["execution_score"].astype(float).values,
        "idea_score": df["idea_score"].astype(float).values,
        "invest": df["would_invest"].astype(int).values
    }

    # 3) Compile & sample
    model = CmdStanModel(stan_file=PATH_TO_STAN_CODE)
    fit = model.sample(
        data=stan_data,
        chains=2,
        parallel_chains=2,
        iter_sampling=500,
        iter_warmup=200,
        seed=123
    )

    # 4) Save results or print summary
    print(fit.summary())

    # Optionally save posterior draws to a CSV
    fit.save_csvfiles(PATH_TO_POSTERIOR_CSV)

if __name__ == "__main__":
    main()
