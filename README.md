# Null Phase Transition: Completion-Deficit Dark Energy

A minimal late-time dark energy model consisting of GR + a canonical scalar field with a Starobinsky-shaped potential of fixed functional form.

## The Model

```
S = ∫d⁴x √(-g) [ R/(16πG) - ½(∂N)² - V(N) ]

V(N) = V₀ (1 - e^{-αN})²,  α = √(2/3)
```

The exponent coefficient α = √(2/3) is fixed by the connection to Starobinsky R² gravity. The only free parameter is the amplitude V₀, set by the observed dark energy density. The initial field value Nᵢ controls branch selection.

## Key Results (CLASS Boltzmann Solver)

### Branch scan (fixed Planck-like background parameters)

| Model | Nᵢ | σ₈ | S₈ | w₀ | Age (Gyr) |
|-------|-----|------|------|--------|-----------|
| ΛCDM | — | 0.812 | 0.827 | −1.000 | 13.76 |
| NPT | 3.0 | 0.805 | 0.820 | −0.996 | 13.66 |
| NPT | 2.9 | 0.802 | 0.817 | −0.995 | 13.61 |
| NPT | 2.8 | 0.797 | 0.811 | −0.994 | 13.52 |
| NPT | 2.7 | 0.789 | 0.803 | −0.993 | 13.40 |

### Joint fit (H₀, ω_cdm, Nᵢ free; compressed Planck + BAO + DES Y6 likelihoods)

| H₀ | ω_cdm | Nᵢ | σ₈ | S₈ | Age (Gyr) | ΔAIC vs ΛCDM |
|----|--------|-----|------|------|-----------|--------------|
| **67** | **0.115** | **2.9** | **0.779** | **0.786** | **13.82** | **−41.6** |

The joint best-fit resolves the age tension (13.82 Gyr consistent with Planck's 13.80 ± 0.02 Gyr), places S₈ within 0.3σ of DES Y6 (0.789 ± 0.012), and preserves the CMB angular scale (100θₛ = 1.040). The ΔAIC = −41.6 (after +2 penalty for Nᵢ) is computed against compressed likelihoods and requires confirmation against the full Planck Cℓ spectrum.

## Predictions (Timestamped: April 2026)

### Structural (shared with canonical quintessence)
- **S1**: w(z) ≥ −1 at all redshifts
- **S2**: Gravitational slip η = Φ/Ψ = 1 exactly
- **S3**: Scale-independent linear growth modification
- **S4**: Sound speed c_s² = 1

### Shape-specific (unique to Starobinsky form)
- **P1**: Thawing coefficient p = 1.30 (vs quadratic 1.50, exponential 2.00)
- **P2**: w(a) curvature w₂ < 0 beyond CPL (|w₂| ~ 0.003 in CLASS solution; unlikely to be observationally accessible with current surveys)
- **P3**: σ₈ shifted toward lensing-preferred values

### Falsification conditions
- **F1**: w < −1 definitively measured → model ruled out
- **F2**: η ≠ 1 at high significance → modified gravity favored
- **F3**: Scale-dependent growth → f(R)-type models favored
- **F4**: p outside [0.8, 1.8] → Starobinsky shape excluded
- **F5**: w = −1 exactly (σ < 0.01) at multiple z → ΛCDM, not thawing

## Observational Timeline

| Experiment | Date | Tests | Decisive for |
|-----------|------|-------|-------------|
| Euclid DR1 | Oct 2026 | Preliminary η | Slip (S2) |
| DESI full | 2027–2028 | Tightened w₀, wₐ | p coefficient (P1) |
| Euclid DR2 | Mar 2029 | η at ~5% | Slip decisive |
| Combined | ~2030 | DESI+Euclid+Rubin | All predictions |

## Repository Structure

```
├── paper/
│   └── NPT_M1_Final.docx          # Working paper (M1 minimal model)
├── class-modification/
│   ├── background.c                 # Modified CLASS source with NPT potential
│   ├── input.c                      # Patched shooting algorithm
│   └── npt_run.ini                  # Reference CLASS input file
├── analysis/
│   └── class_results_summary.txt    # Extracted CLASS outputs
└── README.md
```

## CLASS Implementation

The NPT potential is implemented by modifying three functions in `source/background.c` of CLASS v3.3.4:

```c
double V_scf(struct background *pba, double phi) {
  double V_0 = pba->scf_parameters[0];
  double alpha = 0.816496580927726; /* sqrt(2/3) */
  double e = exp(-alpha * phi);
  return V_0 * (1.0 - e) * (1.0 - e);
}
```

V₀ is tuned by CLASS's shooting algorithm to satisfy the closure equation. α = √(2/3) is hardcoded.

## Physical Interpretation

The field N is interpreted as a **completion deficit**: a measure of residual Lorentzian structure of spacetime, with N = 0 corresponding to the de Sitter vacuum. Dark energy is the thermodynamic signature of incomplete relaxation toward this ground state. This interpretation motivates the potential shape but the observational predictions are independent of it.

## Status

- **Working paper quality**: Strong
- **CLASS implementation**: Operational (v3.3.4, modified background.c)
- **Pipeline validation**: Partial (branch scan + compressed-likelihood joint fit complete; full Planck Cℓ MCMC pending)
- **Honest confidence**: ~30–55% on minimal M1 as a serious late-time model

## Citation

```
Thurlow, A. (2026). Late-Time Dark Energy from a Canonical Completion-Deficit 
Scalar Field. 528 Labs Working Paper.
```

## Acknowledgments

Computational assistance and mathematical development performed in collaboration with Claude (Anthropic). The CLASS Boltzmann solver was modified to implement the completion-deficit potential.

## License

MIT
