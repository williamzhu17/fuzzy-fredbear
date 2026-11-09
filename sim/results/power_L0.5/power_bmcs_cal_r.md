# Power check (results_power_L0.5, successes at 1h, N=5000, 2000 reps, Holm over 5 comparisons per scenario, alpha=0.05)

Full-sample A12 and MWU p use all trials. Detection columns: fraction of reps with Holm-adjusted p < alpha and A12 > 0.5 (x wins) / A12 < 0.5 (y wins).

| scenario | comparison | R | full A12 | full p | n=10: x wins / y wins | n=20: x wins / y wins | n=30: x wins / y wins |
|---|---|---|---|---|---|---|---|
| no_shift | bmcs_cal_r vs transfer | 200 | 0.44 | 0.053 | 0.01 / 0.04 | 0.00 / 0.07 | 0.00 / 0.09 |
| no_shift | bmcs_cal_r vs calib | 200 | 0.82 | 1.5e-28 | 0.58 / 0.00 | 0.95 / 0.00 | 1.00 / 0.00 |
| no_shift | bmcs_cal_r vs fresh | 200 | 0.96 | 3.8e-56 | 0.99 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| no_shift | transfer vs calib | 200 | 0.85 | 1.7e-33 | 0.68 / 0.00 | 0.98 / 0.00 | 1.00 / 0.00 |
| no_shift | transfer vs fresh | 200 | 0.96 | 5.5e-58 | 0.99 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| reversal | bmcs_cal_r vs transfer | 200 | 0.99 | 4.4e-65 | 1.00 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| reversal | bmcs_cal_r vs calib | 200 | 0.41 | 0.0017 | 0.01 / 0.04 | 0.00 / 0.10 | 0.00 / 0.17 |
| reversal | bmcs_cal_r vs fresh | 200 | 0.71 | 1.2e-12 | 0.22 / 0.00 | 0.50 / 0.00 | 0.72 / 0.00 |
| reversal | transfer vs calib | 200 | 0.00 | 5.1e-67 | 0.00 / 1.00 | 0.00 / 1.00 | 0.00 / 1.00 |
| reversal | transfer vs fresh | 200 | 0.00 | 4.7e-67 | 0.00 / 1.00 | 0.00 / 1.00 | 0.00 / 1.00 |
| saturation | bmcs_cal_r vs transfer | 200 | 0.67 | 5.4e-09 | 0.17 / 0.00 | 0.46 / 0.00 | 0.61 / 0.00 |
| saturation | bmcs_cal_r vs calib | 200 | 0.98 | 1.3e-61 | 1.00 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| saturation | bmcs_cal_r vs fresh | 200 | 0.89 | 7.6e-42 | 0.85 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| saturation | transfer vs calib | 200 | 0.98 | 2.3e-62 | 1.00 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| saturation | transfer vs fresh | 200 | 0.83 | 9.5e-30 | 0.65 / 0.00 | 0.97 / 0.00 | 1.00 / 0.00 |
| close_no_shift | bmcs_cal_r vs transfer | 200 | 0.53 | 0.24 | 0.01 / 0.01 | 0.04 / 0.00 | 0.04 / 0.00 |
| close_no_shift | bmcs_cal_r vs calib | 200 | 0.83 | 2.4e-30 | 0.53 / 0.00 | 0.96 / 0.00 | 1.00 / 0.00 |
| close_no_shift | bmcs_cal_r vs fresh | 200 | 0.82 | 7.7e-28 | 0.49 / 0.00 | 0.94 / 0.00 | 1.00 / 0.00 |
| close_no_shift | transfer vs calib | 200 | 0.81 | 2.7e-27 | 0.48 / 0.00 | 0.93 / 0.00 | 0.99 / 0.00 |
| close_no_shift | transfer vs fresh | 200 | 0.79 | 3.2e-24 | 0.42 / 0.00 | 0.89 / 0.00 | 0.98 / 0.00 |
| close_reversal | bmcs_cal_r vs transfer | 200 | 0.50 | 0.96 | 0.01 / 0.00 | 0.00 / 0.00 | 0.01 / 0.01 |
| close_reversal | bmcs_cal_r vs calib | 200 | 0.72 | 5.1e-14 | 0.13 / 0.00 | 0.44 / 0.00 | 0.69 / 0.00 |
| close_reversal | bmcs_cal_r vs fresh | 200 | 0.64 | 1.6e-06 | 0.04 / 0.00 | 0.15 / 0.00 | 0.27 / 0.00 |
| close_reversal | transfer vs calib | 200 | 0.73 | 5.6e-15 | 0.14 / 0.00 | 0.48 / 0.00 | 0.73 / 0.00 |
| close_reversal | transfer vs fresh | 200 | 0.64 | 1.8e-06 | 0.05 / 0.00 | 0.15 / 0.00 | 0.27 / 0.00 |
