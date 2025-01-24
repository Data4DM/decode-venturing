
data {
  int<lower=0> N;                // number of data rows
  vector[N] exec_score;          // "founder execution state"
  vector[N] idea_score;          // "idea quality state"
  int<lower=0, upper=1> invest[N]; // action of investing
}
parameters {
  // Suppose we want to model how these states (exec, idea) link to invest
  real alpha0;
  real alpha_exec;
  real alpha_idea;
}
model {
  // Priors
  alpha0 ~ normal(0,2);
  alpha_exec ~ normal(0,2);
  alpha_idea ~ normal(0,2);

  // Logistic link
  invest ~ bernoulli_logit(alpha0 + alpha_exec * exec_score + alpha_idea * idea_score);
}
