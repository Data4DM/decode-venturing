
data {
  int<lower=0> N;             // number of observations
  int<lower=0> K;             // number of predictors
  matrix[N, K] X;             // predictor matrix
  int<lower=0,upper=1> y[N];  // binary outcome
}

parameters {
  vector[K] beta;             // coefficients
}

model {
  beta ~ normal(0, 5);        // prior
  y ~ bernoulli_logit(X * beta);  // likelihood
}

generated quantities {
  vector[N] log_lik;
  for (n in 1:N)
    log_lik[n] = bernoulli_logit_lpmf(y[n] | X[n] * beta);

  vector[K] odds_ratio;
  for (k in 1:K)
    odds_ratio[k] = exp(beta[k]);
}
