# NPT Full Planck Likelihood: Setup Guide

## Overview

This directory contains everything needed to run a full MCMC analysis of the NPT 
completion-deficit dark energy model against Planck 2018, BAO, and weak lensing data.

## Prerequisites

- Python 3.8+
- gcc/g++ compiler
- ~5GB disk space (for Planck data)
- 4+ CPU cores recommended
- MPI (optional but recommended for parallel chains)

## Step-by-Step Setup

### 1. Install Cobaya

```bash
pip install cobaya
```

### 2. Install Planck Likelihood Data

```bash
cobaya-install planck_2018_highl_plik.TTTEEE_lite
cobaya-install planck_2018_lowl.TT
cobaya-install planck_2018_lowl.EE
cobaya-install planck_2018_lensing.clik
```

This downloads ~2GB of data from the Planck Legacy Archive.

### 3. Build Modified CLASS

```bash
# Clone CLASS
git clone https://github.com/lesgourg/class_public.git
cd class_public

# Apply NPT modifications
cp /path/to/npt-dark-energy/class-modification/background.c source/background.c
cp /path/to/npt-dark-energy/class-modification/input.c source/input.c

# Build C executable
make class -j4

# Build Python wrapper
pip install -e python/
```

Verify: `python -c "from classy import Class; print('OK')"`

### 4. Run the MCMC

Quick test (few hundred samples):
```bash
cobaya-run npt_planck_mcmc.yaml --force
```

Production run with MPI:
```bash
mpirun -n 8 cobaya-run npt_planck_mcmc.yaml
```

### 5. Analyze Results

```bash
# Check convergence
cobaya-get-chains chains/npt_planck --Rminus1

# Plot posteriors  
pip install getdist
python -c "
from getdist.mcsamples import loadMCSamples
samples = loadMCSamples('chains/npt_planck')
print(samples.getTable().tableTex())
"
```

## Expected Results

Based on the compressed-likelihood grid scan, the MCMC should find a 
posterior peaked near:

| Parameter | Expected best-fit | Prior range |
|-----------|------------------|-------------|
| H₀       | ~67 km/s/Mpc     | [60, 80]    |
| ω_b      | ~0.02237         | [0.019, 0.025] |
| ω_cdm    | ~0.115           | [0.09, 0.15] |
| Nᵢ       | ~2.9             | [2.5, 5.0]  |
| n_s      | ~0.965           | [0.9, 1.05] |
| τ_reio   | ~0.054           | [0.01, 0.12] |

Derived quantities at best-fit:
- age ≈ 13.82 Gyr
- σ₈ ≈ 0.779
- S₈ ≈ 0.786
- 100θ_s ≈ 1.040

## Key Questions the MCMC Will Answer

1. **Does the ΔAIC survive the full Planck likelihood?**
   Compressed likelihoods give ΔAIC = -41.6. This may shrink substantially.

2. **Does the S₈ improvement persist in a joint fit?**
   At compressed level, S₈ = 0.786 (0.3σ from DES Y6).

3. **Is the age tension truly resolved?**
   Compressed fit gives 13.82 Gyr. Full Planck may shift this.

4. **What is the posterior on Nᵢ?**
   Is it well-constrained, or does the data allow a wide range?

## Runtime Estimates

| Configuration | Cores | Time to convergence |
|--------------|-------|-------------------|
| Lite Planck  | 4     | ~2-3 days         |
| Lite Planck  | 8     | ~1-2 days         |
| Full Planck  | 4     | ~5-7 days         |
| Full Planck  | 8     | ~3-4 days         |

## Troubleshooting

**CLASS shooting fails for low Nᵢ:**
The shooting algorithm may not converge for Nᵢ < 2.5. If the MCMC 
proposes such values, CLASS will raise an error. The sampler will 
reject these points automatically (-∞ log-likelihood).

**Memory issues:**
The Planck likelihood requires ~1GB RAM per chain. With 8 MPI chains, 
you need ~8GB total.

**Slow convergence:**
If Rminus1 doesn't decrease after 10,000 samples, try:
- Narrowing the prior on Nᵢ to [2.6, 4.0]
- Adjusting the proposal scale for Nᵢ
- Running a shorter chain first to learn the proposal
