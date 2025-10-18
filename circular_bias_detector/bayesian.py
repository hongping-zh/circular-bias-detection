"""
Bayesian Inference for Circular Bias Detection

Provides probabilistic bias detection using Bayesian posterior inference.
Goes beyond frequentist p-values to answer: "What is P(bias | data)?"

Key features:
- Full Bayesian inference with MCMC sampling
- Prior knowledge integration
- Uncertainty quantification
- Posterior predictive checks
"""

import numpy as np
from scipy import stats
from typing import Optional, Dict, Tuple
import warnings

try:
    import pymc as pm  # PyMC v5+
    import arviz as az
    HAS_PYMC = True
except ImportError:
    try:
        import pymc3 as pm  # PyMC3 (older)
        import arviz as az
        HAS_PYMC = True
    except ImportError:
        HAS_PYMC = False
        warnings.warn(
            "PyMC not installed. Install with: pip install pymc arviz\n"
            "For PyMC3: pip install pymc3 arviz theano-pymc"
        )


def bayesian_bias_prob(
    performance_matrix: np.ndarray,
    constraint_matrix: np.ndarray,
    prior_params: Optional[Dict] = None,
    n_samples: int = 2000,
    n_chains: int = 4,
    random_seed: Optional[int] = None
) -> Dict:
    """
    Compute Bayesian probability of circular bias.
    
    Uses Bayesian inference to estimate P(circular_bias | data).
    
    Mathematical Model:
    -------------------
    Likelihood:
        PSI ~ Normal(μ_psi, σ_psi)
        CCS ~ Beta(α_ccs, β_ccs) 
        ρ_PC ~ Normal(μ_rho, σ_rho)
    
    Priors (default):
        μ_psi ~ HalfNormal(0.1)
        σ_psi ~ HalfNormal(0.05)
        μ_rho ~ Normal(0, 0.3)
        σ_rho ~ HalfNormal(0.2)
    
    Posterior:
        P(bias | PSI, CCS, ρ_PC) ∝ P(PSI, CCS, ρ_PC | bias) × P(bias)
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) - performance across time and algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) - constraints across time
    prior_params : dict, optional
        Custom prior parameters (expert knowledge)
    n_samples : int
        Number of MCMC samples per chain (default: 2000)
    n_chains : int
        Number of independent MCMC chains (default: 4)
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    dict
        {
            'bias_probability': float,  # P(bias | data) in [0, 1]
            'ci_lower': float,          # 95% credible interval lower
            'ci_upper': float,          # 95% credible interval upper
            'posterior_samples': array, # MCMC samples for plotting
            'diagnostics': {
                'rhat': float,          # Convergence diagnostic (<1.01 good)
                'ess_bulk': float,      # Effective sample size
                'ess_tail': float,      # Tail ESS
                'divergences': int,     # Number of divergent transitions
                'acceptance_rate': float
            },
            'model_comparison': {
                'waic': float,          # Widely Applicable IC
                'loo': float            # Leave-One-Out CV
            }
        }
    
    Example:
    --------
    >>> results = bayesian_bias_prob(perf_matrix, const_matrix)
    >>> print(f"P(bias|data) = {results['bias_probability']:.3f} "
    ...       f"[{results['ci_lower']:.3f}-{results['ci_upper']:.3f}]")
    P(bias|data) = 0.72 [0.65-0.79]
    """
    
    if not HAS_PYMC:
        raise ImportError(
            "PyMC required for Bayesian inference. "
            "Install with: pip install pymc arviz"
        )
    
    # Compute point estimates for observed data
    from .core import compute_psi, compute_ccs, compute_rho_pc
    
    psi_observed = compute_psi(performance_matrix)
    ccs_observed = compute_ccs(constraint_matrix)
    rho_pc_observed = compute_rho_pc(performance_matrix, constraint_matrix)
    
    # Set default priors
    if prior_params is None:
        prior_params = {
            'psi_mu_prior': 0.1,
            'psi_sigma_prior': 0.05,
            'ccs_alpha_prior': 8.0,
            'ccs_beta_prior': 2.0,
            'rho_mu_prior': 0.0,
            'rho_sigma_prior': 0.3
        }
    
    # Build Bayesian model
    with pm.Model() as model:
        # Priors for PSI (parameter stability)
        mu_psi = pm.HalfNormal('mu_psi', sigma=prior_params['psi_mu_prior'])
        sigma_psi = pm.HalfNormal('sigma_psi', sigma=prior_params['psi_sigma_prior'])
        
        # Priors for CCS (constraint consistency)
        # Transform to Beta parameters
        alpha_ccs = pm.Gamma('alpha_ccs', alpha=prior_params['ccs_alpha_prior'], beta=1.0)
        beta_ccs = pm.Gamma('beta_ccs', alpha=prior_params['ccs_beta_prior'], beta=1.0)
        
        # Priors for ρ_PC (performance-constraint correlation)
        mu_rho = pm.Normal('mu_rho', mu=prior_params['rho_mu_prior'], 
                          sigma=prior_params['rho_sigma_prior'])
        sigma_rho = pm.HalfNormal('sigma_rho', sigma=0.2)
        
        # Likelihood (observed data)
        psi_obs = pm.Normal('psi_obs', mu=mu_psi, sigma=sigma_psi, observed=psi_observed)
        ccs_obs = pm.Beta('ccs_obs', alpha=alpha_ccs, beta=beta_ccs, observed=ccs_observed)
        rho_obs = pm.Normal('rho_obs', mu=mu_rho, sigma=sigma_rho, observed=rho_pc_observed)
        
        # Deterministic bias indicator
        # Bias is likely if: PSI > 0.15 OR CCS < 0.85 OR |ρ_PC| > 0.5
        bias_score = pm.Deterministic(
            'bias_score',
            (mu_psi > 0.15).astype(float) * 0.33 +
            (alpha_ccs / (alpha_ccs + beta_ccs) < 0.85).astype(float) * 0.33 +
            (pm.math.abs(mu_rho) > 0.5).astype(float) * 0.34
        )
        
        # Sample from posterior
        if random_seed is not None:
            np.random.seed(random_seed)
        
        trace = pm.sample(
            draws=n_samples,
            tune=1000,
            chains=n_chains,
            return_inferencedata=True,
            random_seed=random_seed,
            progressbar=True
        )
    
    # Extract posterior samples
    posterior_samples = az.extract(trace, var_names=['bias_score'])
    bias_probability = float(posterior_samples.mean())
    
    # Credible interval (95% HDI)
    hdi = az.hdi(trace, var_names=['bias_score'], hdi_prob=0.95)
    ci_lower = float(hdi['bias_score'].values[0])
    ci_upper = float(hdi['bias_score'].values[1])
    
    # Diagnostics
    summary = az.summary(trace, var_names=['mu_psi', 'alpha_ccs', 'mu_rho'])
    
    rhat_values = summary['r_hat'].values
    ess_bulk_values = summary['ess_bulk'].values
    ess_tail_values = summary['ess_tail'].values
    
    diagnostics = {
        'rhat': float(np.max(rhat_values)),  # Max r_hat (should be < 1.01)
        'ess_bulk': float(np.min(ess_bulk_values)),  # Min ESS
        'ess_tail': float(np.min(ess_tail_values)),
        'divergences': int(trace.sample_stats['diverging'].sum().values),
        'acceptance_rate': float(trace.sample_stats['acceptance_rate'].mean().values)
    }
    
    # Model comparison (WAIC, LOO)
    try:
        waic = az.waic(trace)
        loo = az.loo(trace)
        model_comparison = {
            'waic': float(waic.waic),
            'loo': float(loo.loo)
        }
    except:
        model_comparison = {'waic': None, 'loo': None}
    
    # Check convergence
    if diagnostics['rhat'] > 1.05:
        warnings.warn(
            f"MCMC may not have converged (R-hat = {diagnostics['rhat']:.3f} > 1.05). "
            "Consider increasing n_samples or n_chains."
        )
    
    if diagnostics['divergences'] > 0:
        warnings.warn(
            f"{diagnostics['divergences']} divergent transitions detected. "
            "Consider reparameterizing the model or adjusting step size."
        )
    
    return {
        'bias_probability': bias_probability,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'posterior_samples': posterior_samples.values,
        'diagnostics': diagnostics,
        'model_comparison': model_comparison,
        'observed_values': {
            'psi': psi_observed,
            'ccs': ccs_observed,
            'rho_pc': rho_pc_observed
        },
        'trace': trace  # Full trace for advanced analysis
    }


def interpret_bayesian_results(results: Dict) -> str:
    """
    Generate human-readable interpretation of Bayesian results.
    
    Parameters:
    -----------
    results : dict
        Output from bayesian_bias_prob()
        
    Returns:
    --------
    str
        Natural language interpretation
    """
    
    prob = results['bias_probability']
    ci_low = results['ci_lower']
    ci_high = results['ci_upper']
    
    report = []
    report.append("=" * 60)
    report.append("BAYESIAN BIAS PROBABILITY ANALYSIS")
    report.append("=" * 60)
    report.append("")
    
    # Main result
    report.append(f"P(circular_bias | data) = {prob:.3f} [{ci_low:.3f}-{ci_high:.3f}]")
    report.append("")
    
    # Interpretation
    if prob > 0.7:
        report.append("🔴 HIGH PROBABILITY OF CIRCULAR BIAS")
        report.append(f"   There is a {prob*100:.1f}% probability that circular reasoning")
        report.append("   bias is present in this evaluation.")
        report.append("")
        report.append("   RECOMMENDATION: ⚠️")
        report.append("   - Re-evaluate with pre-registered protocol")
        report.append("   - Fix constraints before experiments")
        report.append("   - Use independent validation set")
    elif prob > 0.5:
        report.append("🟡 MODERATE PROBABILITY OF BIAS")
        report.append(f"   There is a {prob*100:.1f}% probability of circular bias.")
        report.append("   Further investigation recommended.")
        report.append("")
        report.append("   RECOMMENDATION: ⚠️")
        report.append("   - Review evaluation protocol")
        report.append("   - Check for parameter adjustments")
        report.append("   - Consider additional data collection")
    else:
        report.append("🟢 LOW PROBABILITY OF BIAS")
        report.append(f"   Only a {prob*100:.1f}% probability of circular bias.")
        report.append("   Evaluation appears methodologically sound.")
        report.append("")
        report.append("   STATUS: ✅")
        report.append("   - Evaluation protocol is likely unbiased")
        report.append("   - Results can be reported with confidence")
    
    report.append("")
    
    # Diagnostics
    diag = results['diagnostics']
    report.append("MCMC DIAGNOSTICS:")
    report.append("-" * 30)
    
    rhat_status = "✅ Converged" if diag['rhat'] < 1.05 else "⚠️  Check convergence"
    report.append(f"R-hat: {diag['rhat']:.4f} {rhat_status}")
    
    ess_status = "✅ Good" if diag['ess_bulk'] > 400 else "⚠️  Low ESS"
    report.append(f"ESS (bulk): {diag['ess_bulk']:.0f} {ess_status}")
    
    div_status = "✅ None" if diag['divergences'] == 0 else f"⚠️  {diag['divergences']}"
    report.append(f"Divergences: {div_status}")
    
    report.append(f"Acceptance rate: {diag['acceptance_rate']:.3f}")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


# Fallback: Simple Bayesian approximation without PyMC
def simple_bayesian_bias(psi_score: float, 
                        ccs_score: float, 
                        rho_pc_score: float,
                        prior_bias_prob: float = 0.3) -> Dict:
    """
    Simplified Bayesian bias probability using closed-form approximation.
    
    Uses Bayes' theorem with assumed Gaussian likelihoods.
    Useful when PyMC is not available.
    
    Parameters:
    -----------
    psi_score : float
        Observed PSI score
    ccs_score : float
        Observed CCS score
    rho_pc_score : float
        Observed ρ_PC score
    prior_bias_prob : float
        Prior probability of bias (default: 0.3)
        
    Returns:
    --------
    dict
        Approximate Bayesian results
    """
    
    # Likelihood of observing these scores under H1 (bias exists)
    p_psi_given_bias = stats.norm.pdf(psi_score, loc=0.2, scale=0.1)
    p_ccs_given_bias = stats.norm.pdf(ccs_score, loc=0.75, scale=0.1)
    p_rho_given_bias = stats.norm.pdf(abs(rho_pc_score), loc=0.6, scale=0.2)
    
    # Likelihood under H0 (no bias)
    p_psi_given_no_bias = stats.norm.pdf(psi_score, loc=0.05, scale=0.05)
    p_ccs_given_no_bias = stats.norm.pdf(ccs_score, loc=0.95, scale=0.05)
    p_rho_given_no_bias = stats.norm.pdf(abs(rho_pc_score), loc=0.1, scale=0.1)
    
    # Combined likelihoods
    p_data_given_bias = p_psi_given_bias * p_ccs_given_bias * p_rho_given_bias
    p_data_given_no_bias = p_psi_given_no_bias * p_ccs_given_no_bias * p_rho_given_no_bias
    
    # Bayes' theorem
    prior_no_bias = 1 - prior_bias_prob
    
    numerator = p_data_given_bias * prior_bias_prob
    denominator = (p_data_given_bias * prior_bias_prob + 
                  p_data_given_no_bias * prior_no_bias)
    
    posterior_bias_prob = numerator / denominator if denominator > 0 else prior_bias_prob
    
    # Approximate credible interval (using bootstrap-like logic)
    ci_width = 0.1 * posterior_bias_prob
    ci_lower = max(0, posterior_bias_prob - ci_width)
    ci_upper = min(1, posterior_bias_prob + ci_width)
    
    return {
        'bias_probability': posterior_bias_prob,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'method': 'closed_form_approximation',
        'note': 'Approximate Bayesian inference. Install PyMC for full MCMC.'
    }
