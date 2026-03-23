import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Base parameters
k = 1.0
c = 1.0
dt = 0.001
T = 100.0
N = int(T/dt)
t = np.linspace(0, T, N)
n_trajectories = 30

sigma_values = [0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 1.5, 2.0]
alpha_values = [1.5, 2.0, 3.0]  # the three test cases

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Is C ≈ 0.8 Alpha-Dependent or Alpha-Independent?\nPrefactor Stability Test Across α = 1.5, 2.0, 3.0',
             fontsize=13, fontweight='bold')

results = {}  # store all results for analysis

for alpha in alpha_values:
    theoretical_bounds = []
    empirical_bounds = []
    empirical_ratios = []
    regime_depths = []

    for sigma in sigma_values:
        theoretical_bound = (sigma**2 / (2*k*c))**(1/(alpha+1))
        theoretical_bounds.append(theoretical_bound)
        regime_depths.append(sigma**2/(2*k*c))

        steady_stds = []
        for _ in range(n_trajectories):
            x = np.zeros(N)
            x[0] = 0.01
            for j in range(1, N):
                drift = -k * c * abs(x[j-1])**alpha * np.sign(x[j-1])
                diffusion = sigma * np.random.normal(0, np.sqrt(dt))
                x[j] = x[j-1] + drift * dt + diffusion
            steady_stds.append(np.std(x[int(0.8*N):]))

        empirical_bound = np.mean(steady_stds)
        empirical_bounds.append(empirical_bound)
        empirical_ratios.append(empirical_bound / theoretical_bound)

    results[alpha] = {
        'theoretical': theoretical_bounds,
        'empirical': empirical_bounds,
        'ratios': empirical_ratios,
        'regime_depths': regime_depths
    }

# ============================================================
# PLOT 1: Ratio curves for all three alpha values
# ============================================================
ax1 = axes[0, 0]
colors = {1.5: 'blue', 2.0: 'green', 3.0: 'red'}
for alpha in alpha_values:
    ratios = results[alpha]['ratios']
    mean_C = np.mean(ratios)
    ax1.plot(sigma_values, ratios, 'o-', color=colors[alpha], linewidth=2,
             markersize=8, label=f'α={alpha}, mean C={mean_C:.3f}')

ax1.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5, label='Theoretical (C=1.0)')
ax1.axhline(y=0.8, color='gray', linestyle=':', linewidth=1.5, label='C=0.80 reference')
ax1.set_xlabel('Noise magnitude σ')
ax1.set_ylabel('Empirical prefactor C')
ax1.set_title('Prefactor C Across Alpha Values\n(Is C≈0.8 general or parameter-specific?)')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.5, 1.1)

# ============================================================
# PLOT 2: C vs regime depth for all alpha values
# ============================================================
ax2 = axes[0, 1]
for alpha in alpha_values:
    ratios = results[alpha]['ratios']
    regime_depths = results[alpha]['regime_depths']
    ax2.plot(regime_depths, ratios, 'o-', color=colors[alpha], linewidth=2,
             markersize=8, label=f'α={alpha}')

ax2.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5, label='C=1.0')
ax2.axhline(y=0.8, color='gray', linestyle=':', linewidth=1.5, label='C=0.80')
ax2.axvline(x=1.0, color='orange', linestyle=':', linewidth=2, label='Regime boundary')
ax2.set_xlabel('Regime depth σ²/(2kc)')
ax2.set_ylabel('Empirical prefactor C')
ax2.set_title('C vs Regime Depth\n(Does C shift at regime boundary?)')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0.5, 1.1)

# ============================================================
# PLOT 3: Absolute bounds comparison across all alpha
# ============================================================
ax3 = axes[1, 0]
for alpha in alpha_values:
    theo = results[alpha]['theoretical']
    emp = results[alpha]['empirical']
    ax3.plot(sigma_values, theo, '--', color=colors[alpha], linewidth=1.5, alpha=0.6)
    ax3.plot(sigma_values, emp, 'o-', color=colors[alpha], linewidth=2,
             markersize=6, label=f'α={alpha} empirical')

ax3.set_xlabel('Noise magnitude σ')
ax3.set_ylabel('Confinement radius |x_∞|')
ax3.set_title('Absolute Bounds: Empirical (solid) vs Theory (dashed)\nAll Three Alpha Values')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# ============================================================
# PLOT 4: C stability — boxplot style summary
# ============================================================
ax4 = axes[1, 1]
C_values_by_alpha = [results[alpha]['ratios'] for alpha in alpha_values]
C_means = [np.mean(r) for r in C_values_by_alpha]
C_stds = [np.std(r) for r in C_values_by_alpha]

bars = ax4.bar([str(a) for a in alpha_values], C_means,
               color=[colors[a] for a in alpha_values],
               alpha=0.7, width=0.4)
ax4.errorbar([str(a) for a in alpha_values], C_means, yerr=C_stds,
             fmt='none', color='black', capsize=8, linewidth=2)
ax4.axhline(y=0.8, color='gray', linestyle=':', linewidth=2, label='C=0.80 reference')
ax4.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5, label='C=1.0 theoretical')
ax4.set_xlabel('Alpha value')
ax4.set_ylabel('Mean prefactor C ± std')
ax4.set_title('C Stability Summary\n(Error bars = std across sigma values)')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim(0.5, 1.1)

for bar, mean, std in zip(bars, C_means, C_stds):
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + std + 0.01,
             f'C={mean:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/simulation4_prefactor.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# PRINT FULL RESULTS
# ============================================================
print("=" * 70)
print("PREFACTOR STABILITY TEST — IS C≈0.8 ALPHA-INDEPENDENT?")
print("=" * 70)
print(f"Parameters: k={k}, c={c}, x₀=0.01, T={T}, n_traj={n_trajectories}")
print()

for alpha in alpha_values:
    ratios = results[alpha]['ratios']
    mean_C = np.mean(ratios)
    std_C = np.std(ratios)
    min_C = np.min(ratios)
    max_C = np.max(ratios)
    print(f"α = {alpha}:")
    print(f"  Mean C = {mean_C:.4f} ± {std_C:.4f}")
    print(f"  Range  = [{min_C:.4f}, {max_C:.4f}]")
    print(f"  {'σ':>6} {'Theory':>10} {'Empirical':>10} {'C':>8} {'Regime':>15}")
    for i, sigma in enumerate(sigma_values):
        regime = "noise dom." if results[alpha]['regime_depths'][i] >= 1 else "restore dom."
        print(f"  {sigma:>6.1f} {results[alpha]['theoretical'][i]:>10.4f} "
              f"{results[alpha]['empirical'][i]:>10.4f} "
              f"{ratios[i]:>8.3f} {regime:>15}")
    print()

print("=" * 70)
print("VERDICT")
print("=" * 70)
all_C = [c for alpha in alpha_values for c in results[alpha]['ratios']]
overall_mean = np.mean(all_C)
overall_std = np.std(all_C)

C_means = [np.mean(results[alpha]['ratios']) for alpha in alpha_values]
C_spread = max(C_means) - min(C_means)

print(f"Overall mean C across all α and σ: {overall_mean:.4f} ± {overall_std:.4f}")
print(f"Mean C per α: {dict(zip(alpha_values, [round(np.mean(results[a]['ratios']),4) for a in alpha_values]))}")
print(f"Spread between α values: {C_spread:.4f}")
print()

if C_spread < 0.05:
    print("RESULT: C IS ALPHA-INDEPENDENT within this parameter range.")
    print(f"C ≈ {overall_mean:.2f} is a stable empirical constant, not α-specific.")
    print("This is the STRONGER result. Worth stating in the paper.")
elif C_spread < 0.10:
    print("RESULT: C shows mild α-dependence but remains close to 0.8.")
    print("State C ≈ 0.8 with a note that it shifts slightly with α.")
else:
    print("RESULT: C IS ALPHA-DEPENDENT. Do not state as general constant.")
    print(f"Report separately: C(α=1.5)={np.mean(results[1.5]['ratios']):.3f}, "
          f"C(α=2.0)={np.mean(results[2.0]['ratios']):.3f}, "
          f"C(α=3.0)={np.mean(results[3.0]['ratios']):.3f}")
