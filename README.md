# decode-venturing

## 1sim_vc_responses.py

| File Name | Path | Type | Description | Input/Output |
|------------|------|------|-------------|---------------|
| **VC Design Grid.csv** | `decode-venturing/VC Design Grid.csv` | Input (CSV) | Template file with startup scenario parameters | **Input**: Scenario templates <br> **Output**: Generates 10 detailed startup descriptions per template |
| **Pmarca Blog Archives.pdf** | `decode-venturing/Pmarca Blog Archives.pdf` | Input (PDF) | Marc Andreessen's investment philosophy | **Input**: Training data for Marc's investment style
| **bill gurley.md** | `decode-venturing/bill gurley.md` | Input (MD) | Bill Gurley's investment approach | **Input**: Training data for Bill's investment style |
| **embeddings.csv** | `embeddings.csv` | Output (CSV) | Vector representations of startup descriptions | **Contains**: Numerical embeddings for similarity analysis |
| **cosine_similarity.csv** | `cosine_similarity.csv` | Output (CSV) | Startup similarity matrix | **Contains**: Pairwise similarity scores between all startups |
| **vc_investor_responses.csv** | `decode-venturing/vc_investor_responses.csv` | Output (CSV) | Investment decisions | **Contains**: Execution score (1-10), Market score (1-10), Investment decision (Yes/No), Reasoning |

## 2sim_based_2step_calib.py

| File Name | Path | Type | Description | Input/Output |
|------------|------|------|-------------|---------------|
| **vc_investor_responses.csv** | `decoding_decision/vc_investor_responses.csv` | Input (CSV) | Investment decisions data | **Input**: Execution/Market scores, Investment decisions |
| **two_step_model.stan** | `decoding_decision/stan/two_step_model.stan` | Input (Stan) | Statistical model specification | **Input**: Stan model code for two-step calibration |
| **two_step_stan_output** | `decoding_decision/two_step_stan_output` | Output (CSV) | Model fitting results | **Contains**: Parameter posterior distributions |

## 3plot_diagnostics.py

| File Name | Path | Type | Description | Input/Output |
|------------|------|------|-------------|---------------|
| **vc_investor_responses.csv** | `decoding_decision/vc_investor_responses.csv` | Input (CSV) | Investment decisions data | **Input**: Raw investment decisions |
| **two_step_stan_output** | `decoding_decision/two_step_stan_output` | Input (CSV) | Model results | **Input**: Parameter posterior distributions |
| **calibration_plot.png** | Generated during runtime | Output (PNG) | Diagnostic visualization | **Shows**: Predicted vs actual investment probabilities |
| **heatmap_plot.png** | Generated during runtime | Output (PNG) | Diagnostic visualization | **Shows**: Investment probability by execution/idea scores |