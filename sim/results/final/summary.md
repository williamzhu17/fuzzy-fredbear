# Final Stage 1 sweep

R = 30 trials per cell, T = 1,000,000, N = 5000, levels [1.0, 0.5, 0.2], 8 designed scenarios + 84 rank-sweep transitions (6 draws per rho, rho in 1,0.8,0.5,0.2,0,-0.5,-1). Outcome: successes at 1h unless noted. 'adaptive' = bmcs_cal_r, '50/50' = mix50_cal_r, 'adaptive (unscaled)' = bmcs_cal. Significance is two-sided MWU at 0.05; 'unadj.' marks counts without multiplicity correction.


## A. Designed scenarios

Median successes. The last column is the adaptive controller vs transfer / calib / fresh / 50/50 (A12; * = significant after Holm over these 4 comparisons in the cell).

| L | scenario | fresh | calib | shuffled | transfer | adaptive (unscaled) | adaptive | 50/50 | adaptive vs T / C / F / 50/50 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | no_shift | 816 | 882 | 730 | 896 | 895 | 876 | 856 | 0.38 / 0.52 / 0.93* / 0.61 |
| 1 | reversal | 802 | 871 | 450 | 418 | 864 | 834 | 806 | 1.00* / 0.30* / 0.75* / 0.67* |
| 1 | mild_shift | 797 | 866 | 678 | 900 | 896 | 880 | 874 | 0.44 / 0.69* / 0.97* / 0.63 |
| 1 | saturation | 128 | 110 | 84 | 156 | 145 | 170 | 162 | 0.69* / 0.98* / 0.94* / 0.61 |
| 1 | close_no_shift | 282 | 298 | 294 | 340 | 340 | 324 | 314 | 0.34 / 0.77* / 0.92* / 0.64 |
| 1 | close_reversal | 290 | 306 | 290 | 302 | 310 | 300 | 297 | 0.44 / 0.45 / 0.66 / 0.50 |
| 1 | late_riser | 293 | 318 | 302 | 336 | 334 | 314 | 322 | 0.30* / 0.51 / 0.70* / 0.43 |
| 1 | depletion | 219 | 208 | 199 | 233 | 227 | 235 | 224 | 0.47 / 0.77* / 0.74* / 0.64 |
| 0.5 | no_shift | 373 | 412 | 340 | 438 | 431 | 433 | 422 | 0.43 / 0.67 / 0.95* / 0.62 |
| 0.5 | reversal | 377 | 409 | 300 | 185 | 404 | 404 | 397 | 1.00* / 0.48 / 0.80* / 0.62 |
| 0.5 | mild_shift | 382 | 414 | 319 | 443 | 434 | 442 | 427 | 0.45 / 0.80* / 0.94* / 0.68* |
| 0.5 | saturation | 55 | 35 | 36 | 64 | 65 | 77 | 72 | 0.74* / 0.99* / 0.88* / 0.54 |
| 0.5 | close_no_shift | 136 | 124 | 132 | 150 | 139 | 152 | 148 | 0.52 / 0.90* / 0.75* / 0.55 |
| 0.5 | close_reversal | 132 | 132 | 124 | 148 | 136 | 146 | 143 | 0.50 / 0.75* / 0.70* / 0.50 |
| 0.5 | late_riser | 140 | 142 | 136 | 158 | 148 | 160 | 154 | 0.61 / 0.91* / 0.86* / 0.65 |
| 0.5 | depletion | 102 | 104 | 110 | 120 | 118 | 119 | 120 | 0.45 / 0.77* / 0.79* / 0.52 |
| 0.2 | no_shift | 125 | 103 | 116 | 150 | 146 | 163 | 156 | 0.73* / 1.00* / 0.95* / 0.62 |
| 0.2 | reversal | 126 | 110 | 90 | 62 | 106 | 141 | 148 | 0.99* / 0.79* / 0.70* / 0.45 |
| 0.2 | mild_shift | 126 | 116 | 104 | 150 | 150 | 159 | 157 | 0.73* / 0.99* / 0.97* / 0.59 |
| 0.2 | saturation | 13 | 12 | 10 | 22 | 19 | 26 | 24 | 0.68* / 0.95* / 0.86* / 0.59 |
| 0.2 | close_no_shift | 48 | 41 | 44 | 53 | 50 | 57 | 52 | 0.61 / 0.91* / 0.77* / 0.63 |
| 0.2 | close_reversal | 48 | 39 | 43 | 51 | 45 | 55 | 54 | 0.64 / 0.85* / 0.69* / 0.56 |
| 0.2 | late_riser | 47 | 49 | 46 | 59 | 50 | 63 | 58 | 0.61 / 0.89* / 0.91* / 0.65 |
| 0.2 | depletion | 43 | 42 | 42 | 50 | 44 | 46 | 48 | 0.35 / 0.67 / 0.61 / 0.43 |

## B. Every policy against the hindsight-best fixed prior

For each scenario x level cell, the best fixed prior is whichever of fresh / calib / transfer has the highest median in that cell (chosen in hindsight, so no real policy can beat it on average). Ratio = policy median / best-fixed median. 'within 5%' = share of cells with ratio >= 0.95. worse / better = cells where the policy is significantly below / above the best fixed prior (unadj.).


**all cells**

| L | policy | median ratio | 10th pct | worst | within 5% | worse / better | 4h median ratio |
|---|---|---|---|---|---|---|---|
| 1 | fresh | 0.922 | 0.861 | 0.815 | 8% | 86 / 0 | 0.949 |
| 1 | calib | 1.000 | 0.907 | 0.702 | 78% | 34 / 0 | 1.000 |
| 1 | shuffled | 0.853 | 0.535 | 0.475 | 12% | 72 / 0 | 0.888 |
| 1 | transfer | 0.937 | 0.474 | 0.286 | 48% | 49 / 0 | 0.934 |
| 1 | adaptive (unscaled) | 0.985 | 0.933 | 0.735 | 82% | 21 / 0 | 0.989 |
| 1 | adaptive | 0.962 | 0.918 | 0.877 | 68% | 53 / 1 | 0.982 |
| 1 | 50/50 | 0.941 | 0.896 | 0.834 | 40% | 79 / 0 | 0.966 |
| 0.5 | fresh | 0.928 | 0.856 | 0.831 | 29% | 68 / 0 | 0.964 |
| 0.5 | calib | 0.958 | 0.863 | 0.543 | 51% | 40 / 0 | 0.964 |
| 0.5 | shuffled | 0.854 | 0.678 | 0.566 | 15% | 73 / 0 | 0.882 |
| 0.5 | transfer | 0.985 | 0.584 | 0.452 | 52% | 44 / 0 | 0.977 |
| 0.5 | adaptive (unscaled) | 0.971 | 0.922 | 0.861 | 71% | 28 / 1 | 0.968 |
| 0.5 | adaptive | 0.995 | 0.963 | 0.910 | 97% | 6 / 5 | 1.012 |
| 0.5 | 50/50 | 0.982 | 0.944 | 0.906 | 85% | 21 / 1 | 1.001 |
| 0.2 | fresh | 1.000 | 0.811 | 0.591 | 61% | 28 / 0 | 1.000 |
| 0.2 | calib | 0.859 | 0.729 | 0.545 | 7% | 75 / 0 | 0.861 |
| 0.2 | shuffled | 0.776 | 0.595 | 0.455 | 5% | 78 / 0 | 0.816 |
| 0.2 | transfer | 0.970 | 0.496 | 0.364 | 53% | 38 / 0 | 0.950 |
| 0.2 | adaptive (unscaled) | 0.887 | 0.820 | 0.743 | 22% | 58 / 0 | 0.906 |
| 0.2 | adaptive | 1.087 | 1.001 | 0.914 | 96% | 0 / 47 | 1.091 |
| 0.2 | 50/50 | 1.065 | 0.981 | 0.919 | 97% | 0 / 37 | 1.072 |

**designed only**

| L | policy | median ratio | 10th pct | worst | within 5% | worse / better | 4h median ratio |
|---|---|---|---|---|---|---|---|
| 1 | fresh | 0.898 | 0.828 | 0.824 | 0% | 8 / 0 | 0.947 |
| 1 | calib | 0.955 | 0.823 | 0.702 | 50% | 6 / 0 | 0.966 |
| 1 | shuffled | 0.835 | 0.530 | 0.517 | 0% | 7 / 0 | 0.882 |
| 1 | transfer | 1.000 | 0.835 | 0.480 | 88% | 1 / 0 | 1.000 |
| 1 | adaptive (unscaled) | 0.996 | 0.961 | 0.929 | 88% | 1 / 0 | 0.998 |
| 1 | adaptive | 0.978 | 0.949 | 0.936 | 88% | 3 / 1 | 0.993 |
| 1 | 50/50 | 0.962 | 0.925 | 0.922 | 75% | 5 / 0 | 0.980 |
| 0.5 | fresh | 0.875 | 0.853 | 0.853 | 0% | 8 / 0 | 0.928 |
| 0.5 | calib | 0.897 | 0.741 | 0.543 | 12% | 7 / 0 | 0.944 |
| 0.5 | shuffled | 0.809 | 0.674 | 0.566 | 0% | 8 / 0 | 0.866 |
| 0.5 | transfer | 1.000 | 0.836 | 0.452 | 88% | 1 / 0 | 1.000 |
| 0.5 | adaptive (unscaled) | 0.983 | 0.925 | 0.922 | 62% | 1 / 0 | 0.970 |
| 0.5 | adaptive | 0.996 | 0.988 | 0.986 | 100% | 0 / 1 | 1.004 |
| 0.5 | 50/50 | 0.974 | 0.965 | 0.964 | 100% | 2 / 1 | 0.995 |
| 0.2 | fresh | 0.843 | 0.735 | 0.591 | 12% | 6 / 0 | 0.948 |
| 0.2 | calib | 0.774 | 0.644 | 0.545 | 0% | 8 / 0 | 0.836 |
| 0.2 | shuffled | 0.774 | 0.618 | 0.455 | 0% | 8 / 0 | 0.822 |
| 0.2 | transfer | 1.000 | 0.848 | 0.494 | 88% | 1 / 0 | 1.000 |
| 0.2 | adaptive (unscaled) | 0.877 | 0.840 | 0.839 | 25% | 4 / 0 | 0.917 |
| 0.2 | adaptive | 1.077 | 1.016 | 0.921 | 88% | 0 / 4 | 1.104 |
| 0.2 | 50/50 | 1.042 | 0.964 | 0.941 | 88% | 0 / 2 | 1.072 |

**rank sweep only**

| L | policy | median ratio | 10th pct | worst | within 5% | worse / better | 4h median ratio |
|---|---|---|---|---|---|---|---|
| 1 | fresh | 0.923 | 0.863 | 0.815 | 8% | 78 / 0 | 0.949 |
| 1 | calib | 1.000 | 0.916 | 0.872 | 81% | 28 / 0 | 1.000 |
| 1 | shuffled | 0.853 | 0.537 | 0.475 | 13% | 65 / 0 | 0.889 |
| 1 | transfer | 0.900 | 0.465 | 0.286 | 44% | 48 / 0 | 0.897 |
| 1 | adaptive (unscaled) | 0.984 | 0.933 | 0.735 | 81% | 20 / 0 | 0.989 |
| 1 | adaptive | 0.961 | 0.917 | 0.877 | 67% | 50 / 0 | 0.981 |
| 1 | 50/50 | 0.939 | 0.894 | 0.834 | 37% | 74 / 0 | 0.965 |
| 0.5 | fresh | 0.932 | 0.858 | 0.831 | 32% | 60 / 0 | 0.966 |
| 0.5 | calib | 0.969 | 0.868 | 0.815 | 55% | 33 / 0 | 0.967 |
| 0.5 | shuffled | 0.856 | 0.679 | 0.602 | 17% | 65 / 0 | 0.882 |
| 0.5 | transfer | 0.938 | 0.584 | 0.466 | 49% | 43 / 0 | 0.953 |
| 0.5 | adaptive (unscaled) | 0.970 | 0.921 | 0.861 | 71% | 27 / 1 | 0.968 |
| 0.5 | adaptive | 0.995 | 0.962 | 0.910 | 96% | 6 / 4 | 1.017 |
| 0.5 | 50/50 | 0.985 | 0.943 | 0.906 | 83% | 19 / 0 | 1.004 |
| 0.2 | fresh | 1.000 | 0.821 | 0.759 | 65% | 22 / 0 | 1.000 |
| 0.2 | calib | 0.862 | 0.736 | 0.667 | 7% | 67 / 0 | 0.864 |
| 0.2 | shuffled | 0.785 | 0.597 | 0.502 | 6% | 70 / 0 | 0.816 |
| 0.2 | transfer | 0.953 | 0.493 | 0.364 | 50% | 37 / 0 | 0.929 |
| 0.2 | adaptive (unscaled) | 0.888 | 0.819 | 0.743 | 21% | 54 / 0 | 0.903 |
| 0.2 | adaptive | 1.090 | 1.003 | 0.914 | 96% | 0 / 43 | 1.088 |
| 0.2 | 50/50 | 1.068 | 0.990 | 0.919 | 98% | 0 / 35 | 1.072 |

## C. Rank sweep split by whether transfer helps

Regime from the transfer / calib median ratio in the cell: helps > 1.05, neutral 0.95-1.05, hurts < 0.95. Cells show the median over cells of each policy's median relative to calib; then the adaptive controller's win / tie / loss counts (unadj.) against 50/50 and against transfer, and its mean P(T) at 1h.

| L | regime | cells | fresh | shuffled | transfer | adaptive (unscaled) | adaptive | 50/50 | adaptive vs 50/50 W/T/L | adaptive vs transfer W/T/L | P(T) 1h |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | helps | 17 | 0.94 | 0.95 | 1.09 | 1.07 | 1.03 | 1.02 | 3/14/0 | 0/4/13 | 0.67 |
| 1 | neutral | 20 | 0.93 | 0.75 | 1.02 | 1.02 | 1.00 | 0.99 | 9/11/0 | 0/12/8 | 0.78 |
| 1 | hurts | 47 | 0.94 | 0.88 | 0.68 | 0.98 | 0.96 | 0.94 | 13/34/0 | 39/7/1 | 0.12 |
| 0.5 | helps | 30 | 0.97 | 0.92 | 1.10 | 1.07 | 1.09 | 1.09 | 5/25/0 | 0/29/1 | 0.75 |
| 0.5 | neutral | 14 | 0.96 | 0.88 | 1.00 | 0.98 | 1.02 | 1.02 | 1/13/0 | 3/11/0 | 0.53 |
| 0.5 | hurts | 40 | 0.95 | 0.90 | 0.71 | 0.98 | 1.01 | 1.00 | 5/35/0 | 38/2/0 | 0.09 |
| 0.2 | helps | 43 | 1.11 | 0.93 | 1.22 | 1.12 | 1.31 | 1.28 | 3/40/0 | 25/18/0 | 0.66 |
| 0.2 | neutral | 5 | 1.07 | 0.91 | 0.98 | 0.98 | 1.12 | 1.14 | 0/5/0 | 3/2/0 | 0.40 |
| 0.2 | hurts | 36 | 1.13 | 0.91 | 0.67 | 0.96 | 1.27 | 1.24 | 2/33/1 | 36/0/0 | 0.10 |

## D. Adaptive controller head-to-head, all cells

Win / tie / loss (significant unadj.), median of per-cell median ratios, and the range of that ratio.

| L | adaptive vs | W / T / L | median ratio | range |
|---|---|---|---|---|
| 1 | fresh | 63 / 29 / 0 | 1.047 | 0.93-1.33 |
| 1 | calib | 13 / 48 / 31 | 0.977 | 0.89-1.56 |
| 1 | shuffled | 61 / 31 / 0 | 1.109 | 0.91-2.04 |
| 1 | transfer | 41 / 27 / 24 | 1.009 | 0.88-3.35 |
| 1 | adaptive (unscaled) | 2 / 68 / 22 | 0.979 | 0.91-1.25 |
| 1 | 50/50 | 26 / 66 / 0 | 1.020 | 0.93-1.15 |
| 0.5 | fresh | 67 / 25 / 0 | 1.085 | 0.95-1.40 |
| 0.5 | calib | 42 / 45 / 5 | 1.045 | 0.91-2.20 |
| 0.5 | shuffled | 74 / 18 / 0 | 1.171 | 0.95-2.11 |
| 0.5 | transfer | 43 / 48 / 1 | 1.039 | 0.95-2.19 |
| 0.5 | adaptive (unscaled) | 21 / 70 / 1 | 1.019 | 0.96-1.18 |
| 0.5 | 50/50 | 13 / 79 / 0 | 1.015 | 0.90-1.09 |
| 0.2 | fresh | 66 / 26 / 0 | 1.155 | 0.98-1.96 |
| 0.2 | calib | 87 / 5 / 0 | 1.291 | 1.05-2.12 |
| 0.2 | shuffled | 87 / 5 / 0 | 1.376 | 1.01-2.55 |
| 0.2 | transfer | 68 / 24 / 0 | 1.141 | 0.91-3.23 |
| 0.2 | adaptive (unscaled) | 81 / 11 / 0 | 1.198 | 1.02-1.54 |
| 0.2 | 50/50 | 6 / 85 / 1 | 1.009 | 0.88-1.14 |

## E. Prior check: does the old ranking itself matter?

Transfer against calib (right scale, no ranking) and shuffled (right scale and spread, wrong ranking), in rank-sweep cells where the old best operator is still best vs where it is not.

| L | old best kept? | cells | transfer vs calib W/T/L | transfer vs shuffled W/T/L | median T / C |
|---|---|---|---|---|---|
| 1 | yes | 26 | 22/4/0 | 25/1/0 | 1.04 |
| 1 | no | 58 | 6/4/48 | 11/18/29 | 0.73 |
| 0.5 | yes | 26 | 25/1/0 | 26/0/0 | 1.09 |
| 0.5 | no | 58 | 5/12/41 | 14/14/30 | 0.77 |
| 0.2 | yes | 26 | 24/2/0 | 25/1/0 | 1.33 |
| 0.2 | no | 58 | 12/11/35 | 14/15/29 | 0.80 |

## F. Simulated Stage 2: 6 random transitions, n trials per policy

Each repetition (2000) draws 6 distinct transitions from the rank sweep at one level and, for each, n trials per policy resampled with replacement from that cell's 30. Detection rates:

- **per-transition**: mean share of the 6 transitions where the comparison is significant in the stated direction after Holm over the 5-comparison family (adaptive vs transfer, calib, fresh; transfer vs calib, fresh) plus adaptive vs 50/50, i.e. 6 tests;
- **pooled**: share of repetitions where a Stouffer combination of the 6 signed MWU z-scores is significant (two-sided 0.05) in the stated direction.

'Population effect' is the mean A12 over all rank cells at that level (what the pooled test estimates). Resampling from 30 trials understates real variability; treat these as upper bounds.

| L | comparison | population A12 | n=10 per-transition | n=10 pooled | n=20 per-transition | n=20 pooled |
|---|---|---|---|---|---|---|
| 1 | adaptive > 50/50 | 0.59 | 0.08 | 0.42 | 0.18 | 0.65 |
| 1 | adaptive > transfer | 0.64 | 0.42 | 0.62 | 0.46 | 0.72 |
| 1 | adaptive > calib | 0.42 | 0.02 | 0.01 | 0.06 | 0.01 |
| 1 | adaptive > fresh | 0.71 | 0.32 | 0.89 | 0.52 | 0.96 |
| 1 | transfer > calib | 0.34 | 0.09 | 0.03 | 0.20 | 0.04 |
| 1 | transfer > fresh | 0.46 | 0.35 | 0.20 | 0.41 | 0.25 |
| 0.5 | adaptive > 50/50 | 0.55 | 0.04 | 0.20 | 0.10 | 0.31 |
| 0.5 | adaptive > transfer | 0.70 | 0.41 | 0.81 | 0.44 | 0.89 |
| 0.5 | adaptive > calib | 0.62 | 0.15 | 0.55 | 0.30 | 0.74 |
| 0.5 | adaptive > fresh | 0.72 | 0.33 | 0.93 | 0.53 | 0.97 |
| 0.5 | transfer > calib | 0.40 | 0.14 | 0.08 | 0.27 | 0.11 |
| 0.5 | transfer > fresh | 0.45 | 0.25 | 0.14 | 0.36 | 0.21 |
| 0.2 | adaptive > 50/50 | 0.52 | 0.04 | 0.09 | 0.08 | 0.15 |
| 0.2 | adaptive > transfer | 0.78 | 0.47 | 0.99 | 0.62 | 0.99 |
| 0.2 | adaptive > calib | 0.83 | 0.53 | 1.00 | 0.79 | 1.00 |
| 0.2 | adaptive > fresh | 0.72 | 0.32 | 0.95 | 0.51 | 0.99 |
| 0.2 | transfer > calib | 0.50 | 0.26 | 0.23 | 0.37 | 0.30 |
| 0.2 | transfer > fresh | 0.39 | 0.17 | 0.07 | 0.24 | 0.10 |
