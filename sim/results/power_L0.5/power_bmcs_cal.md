# Power check (results_power_L0.5, successes at 1h, N=5000, 2000 reps, Holm over 5 comparisons per scenario, alpha=0.05)

Full-sample A12 and MWU p use all trials. Detection columns: fraction of reps with Holm-adjusted p < alpha and A12 > 0.5 (x wins) / A12 < 0.5 (y wins).

| scenario | comparison | R | full A12 | full p | n=10: x wins / y wins |
|---|---|---|---|---|---|
| no_shift | bmcs_cal vs transfer | 200 | 0.41 | 0.0011 | 0.00 / 0.06 |
| no_shift | bmcs_cal vs calib | 200 | 0.77 | 3e-21 | 0.40 / 0.00 |
| no_shift | bmcs_cal vs fresh | 200 | 0.93 | 2.8e-50 | 0.96 / 0.00 |
| no_shift | transfer vs calib | 200 | 0.85 | 1.7e-33 | 0.67 / 0.00 |
| no_shift | transfer vs fresh | 200 | 0.96 | 5.5e-58 | 0.99 / 0.00 |
| reversal | bmcs_cal vs transfer | 200 | 1.00 | 5.2e-67 | 1.00 / 0.00 |
| reversal | bmcs_cal vs calib | 200 | 0.41 | 0.0026 | 0.00 / 0.04 |
| reversal | bmcs_cal vs fresh | 200 | 0.72 | 4.3e-14 | 0.25 / 0.00 |
| reversal | transfer vs calib | 200 | 0.00 | 5.1e-67 | 0.00 / 1.00 |
| reversal | transfer vs fresh | 200 | 0.00 | 4.7e-67 | 0.00 / 1.00 |
| saturation | bmcs_cal vs transfer | 200 | 0.34 | 5e-08 | 0.00 / 0.11 |
| saturation | bmcs_cal vs calib | 200 | 0.94 | 3.4e-52 | 0.97 / 0.00 |
| saturation | bmcs_cal vs fresh | 200 | 0.70 | 1.3e-12 | 0.21 / 0.00 |
| saturation | transfer vs calib | 200 | 0.98 | 2.3e-62 | 1.00 / 0.00 |
| saturation | transfer vs fresh | 200 | 0.83 | 9.5e-30 | 0.55 / 0.00 |
| close_no_shift | bmcs_cal vs transfer | 200 | 0.42 | 0.0049 | 0.00 / 0.02 |
| close_no_shift | bmcs_cal vs calib | 200 | 0.74 | 2.3e-17 | 0.22 / 0.00 |
| close_no_shift | bmcs_cal vs fresh | 200 | 0.72 | 7.2e-14 | 0.18 / 0.00 |
| close_no_shift | transfer vs calib | 200 | 0.81 | 2.7e-27 | 0.42 / 0.00 |
| close_no_shift | transfer vs fresh | 200 | 0.79 | 3.2e-24 | 0.35 / 0.00 |
| close_reversal | bmcs_cal vs transfer | 200 | 0.36 | 1.4e-06 | 0.00 / 0.05 |
| close_reversal | bmcs_cal vs calib | 200 | 0.60 | 0.0006 | 0.02 / 0.00 |
| close_reversal | bmcs_cal vs fresh | 200 | 0.49 | 0.86 | 0.00 / 0.00 |
| close_reversal | transfer vs calib | 200 | 0.73 | 5.6e-15 | 0.14 / 0.00 |
| close_reversal | transfer vs fresh | 200 | 0.64 | 1.8e-06 | 0.05 / 0.00 |
