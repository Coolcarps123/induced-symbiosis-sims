# Induced Symbiosis Through Convexity
## Numerical Validation — Stochastic Confinement Bound

Repository for simulation code supporting the paper:
**Induced Symbiosis Through Convexity: A General Principle of Mechanism Design**
Carpenter Buday, Expona Research, 2026

---

### What This Repository Contains

Three simulation scripts validating the stochastic confinement bound
derived in §2.5b of the paper.

**simulation3_corrected.py**
Baseline validation. Confirms the theoretical bound
|x_∞| ~ (σ²/(2kc))^(1/(α+1)) holds empirically at k=c=1, α=2,
σ ∈ [0.1, 2.0]. Measures the empirical prefactor C across both
the restoring-force-dominant and noise-dominant regimes.

**simulation4_prefactor.py**
Alpha-dependence test. Runs the same validation across
α ∈ {1.5, 2.0, 3.0} to determine whether the prefactor C is
alpha-independent (a general constant) or alpha-dependent. Result:
C is alpha-dependent, decreasing monotonically with α.

**simulation5_complete_range.py**
Full parameter range. Extends to α = 3.5, completing coverage
of the paper's specified operational range α ∈ [1.5, 3.5].
Establishes the linear relationship C(α) ≈ −0.086α + 0.983.

---

### Key Results

| α    | Mean C | Safety Margin |
|------|--------|---------------|
| 1.5  | 0.863  | 13.7%         |
| 2.0  | 0.804  | 19.6%         |
| 3.0  | 0.717  | 28.3%         |
| 3.5  | 0.693  | 30.7%         |

The theoretical bound holds at all parameter combinations tested.
Higher convexity produces tighter empirical confinement relative
to the theoretical bound. The bound is most conservative in the
deep restoring-force-dominant regime (σ²/(2kc) ≪ 1) at high α.

Linear trend: C(α) ≈ −0.086α + 0.983

---

### Parameters

All simulations use:
- k = 1.0, c = 1.0
- x₀ = 0.01 (near-equilibrium initialisation)
- dt = 0.001, T = 100.0
- n_trajectories = 30 per σ value
- Steady-state window: t ∈ [80, 100]
- Regime boundary: σ = √(2kc) = √2 ≈ 1.414

---

### Dependencies

numpy
matplotlib

---

### Reproducing The Figures

```bash
python simulation3_corrected.py
python simulation4_prefactor.py
python simulation5_complete_range.py

Figures save to the working directory as PNG files.
