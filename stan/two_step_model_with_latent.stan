data {
  int<lower=0> N;                // number of data rows
  vector[N] exec_score;          // "founder execution state"
  vector[N] idea_score;          // "idea quality state"
  int<lower=0, upper=1> invest[N]; // action of investing
}

parameters {
  real alpha0;
  real alpha_exec;
  real alpha_idea;
  
  // Latent states
  int<lower=1, upper=K> state[N]; // K latent states
  real mu_alpha_exec[K];
  real mu_alpha_idea[K];
  real<lower=0> sigma_alpha_exec;
  real<lower=0> sigma_alpha_idea;
}

model {
  // Priors
  alpha0 ~ normal(0, 2);
  
  mu_alpha_exec ~ normal(0, 2);
  mu_alpha_idea ~ normal(0, 2);
  sigma_alpha_exec ~ cauchy(0, 2);
  sigma_alpha_idea ~ cauchy(0, 2);
  
  for (n in 1:N) {
    // Hierarchical priors for latent states
    alpha_exec = mu_alpha_exec[state[n]] + sigma_alpha_exec * normal_rng(0, 1);
    alpha_idea = mu_alpha_idea[state[n]] + sigma_alpha_idea * normal_rng(0, 1);
    
    // Logistic regression
    invest[n] ~ bernoulli_logit(alpha0 + alpha_exec * exec_score[n] + alpha_idea * idea_score[n]);
  }
}
