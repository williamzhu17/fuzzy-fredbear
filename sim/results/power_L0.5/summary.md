# Stage 1 simulation results

R = 200 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 0.5.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [5.0e-03 2.5e-03 1.5e-03 1.0e-03 5.0e-04 2.5e-04 1.0e-04 5.0e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 154 [145-164] | 375 [361-396] | 669 [648-690] | 90 [80-102] | 0.72 / 0.88 / 0.90 | 0.00 / 0.00 / 0.00 | 0.80 / 0.02 / 0.09 |
| calib | 177 [162-187] | 404 [383-420] | 685 [661-708] | 73 [64-84] | 0.85 / 0.90 / 0.87 | 0.00 / 0.00 / 0.00 | 0.80 / 0.05 / 0.16 |
| transfer | 203 [193-212] | 440 [422-455] | 733 [712-750] | 29 [26-33] | 0.98 / 0.94 / 0.91 | 1.00 / 1.00 / 1.00 | 0.73 / 0.03 / 0.42 |
| bmcs_cal | 198 [186-207] | 430 [414-447] | 724 [700-743] | 37 [33-43] | 0.96 / 0.93 / 0.90 | 0.82 / 0.91 / 0.97 | 0.77 / 0.04 / 0.32 |
| bmcs_cal_r | 192 [182-202] | 435 [419-449] | 744 [728-761] | 20 [15-26] | 0.94 / 0.97 / 0.97 | 0.93 / 0.95 / 0.92 | 0.77 / 0.04 / 0.33 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.96 | 1.52e-55 |
| bmcs_cal_r vs calib | 0.82 | 4.41e-28 |
| bmcs_cal_r vs transfer | 0.44 | 0.106 |
| bmcs_cal_r vs bmcs_cal | 0.54 | 0.124 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.85 | 1.66e-33 |
| transfer vs fresh | 0.96 | 1.11e-57 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.0e-04 2.5e-03 1.5e-03 1.0e-03 5.0e-04 2.5e-04 5.0e-03 5.0e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 155 [145-166] | 378 [364-394] | 669 [649-690] | 91 [81-102] | 0.72 / 0.88 / 0.90 | 0.00 / 0.00 / 0.00 | 0.81 / 0.56 / 0.90 |
| calib | 181 [167-192] | 412 [394-427] | 699 [671-716] | 65 [57-77] | 0.87 / 0.91 / 0.87 | 0.00 / 0.00 / 0.00 | 0.81 / 0.72 / 0.91 |
| transfer | 74 [67-82] | 186 [174-200] | 355 [332-392] | 404 [370-428] | 0.00 / 0.10 / 0.28 | 1.00 / 1.00 / 1.00 | 0.81 / 0.60 / 0.72 |
| bmcs_cal | 172 [156-187] | 400 [381-424] | 677 [655-710] | 74 [63-91] | 0.83 / 0.90 / 0.86 | 0.03 / 0.01 / 0.04 | 0.81 / 0.57 / 0.86 |
| bmcs_cal_r | 168 [152-180] | 404 [378-419] | 702 [670-725] | 55 [40-75] | 0.75 / 0.90 / 0.90 | 0.05 / 0.01 / 0.04 | 0.81 / 0.61 / 0.91 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.71 | 3.53e-12 |
| bmcs_cal_r vs calib | 0.41 | 0.00336 |
| bmcs_cal_r vs transfer | 0.99 | 1.76e-64 |
| bmcs_cal_r vs bmcs_cal | 0.50 | 0.9 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.00 | 9.46e-67 |
| transfer vs fresh | 0.00 | 9.46e-67 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 2.5 [2.0-3.5], never: 0/200
- calib: 2.0 [1.5-2.7], never: 0/200
- transfer: 167.7 [58.5-240.0], never: 93/200
- bmcs_cal: 2.2 [1.7-3.4], never: 0/200
- bmcs_cal_r: 2.5 [1.9-4.0], never: 3/200

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.e-03 5.e-04 3.e-04 2.e-04 1.e-04 5.e-05 2.e-05 1.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 18 [14-22] | 51 [43-60] | 99 [88-110] | 52 [46-60] | 0.33 / 0.57 / 0.67 | 0.00 / 0.00 / 0.00 | 0.82 / 0.73 / 0.73 |
| calib | 16 [12-19] | 38 [33-45] | 72 [64-83] | 80 [74-84] | 0.24 / 0.35 / 0.43 | 0.00 / 0.00 / 0.00 | 0.82 / 0.60 / 0.48 |
| transfer | 32 [27-37] | 67 [60-73] | 113 [103-122] | 40 [37-43] | 0.63 / 0.58 / 0.63 | 1.00 / 1.00 / 1.00 | 0.82 / 0.84 / 0.85 |
| bmcs_cal | 26 [22-32] | 60 [52-69] | 104 [94-116] | 46 [43-51] | 0.55 / 0.56 / 0.59 | 0.79 / 0.89 / 0.89 | 0.82 / 0.80 / 0.83 |
| bmcs_cal_r | 31 [25-37] | 73 [66-81] | 130 [118-139] | 21 [15-26] | 0.70 / 0.81 / 0.83 | 0.75 / 0.82 / 0.82 | 0.82 / 0.74 / 0.72 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.89 | 2.28e-41 |
| bmcs_cal_r vs calib | 0.98 | 5.04e-61 |
| bmcs_cal_r vs transfer | 0.67 | 5.38e-09 |
| bmcs_cal_r vs bmcs_cal | 0.78 | 8.27e-22 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.98 | 4.69e-62 |
| transfer vs fresh | 0.83 | 9.49e-30 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00125 0.00075 0.0005  0.00025 0.0001 ]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 56 [51-62] | 134 [124-143] | 235 [221-249] | 68 [61-77] | 0.26 / 0.36 / 0.40 | 0.00 / 0.00 / 0.00 | 0.51 / 0.22 / 0.29 |
| calib | 56 [50-64] | 131 [120-142] | 229 [214-241] | 78 [68-87] | 0.28 / 0.33 / 0.36 | 0.00 / 0.00 / 0.00 | 0.51 / 0.24 / 0.19 |
| transfer | 70 [64-76] | 150 [140-162] | 253 [240-271] | 46 [40-53] | 0.48 / 0.45 / 0.47 | 1.00 / 1.00 / 1.00 | 0.50 / 0.41 / 0.60 |
| bmcs_cal | 66 [57-72] | 145 [134-156] | 249 [233-262] | 55 [49-62] | 0.43 / 0.44 / 0.45 | 0.77 / 0.89 / 0.89 | 0.51 / 0.29 / 0.41 |
| bmcs_cal_r | 66 [59-73] | 152 [141-163] | 261 [246-275] | 43 [33-53] | 0.46 / 0.52 / 0.53 | 0.75 / 0.84 / 0.83 | 0.51 / 0.32 / 0.52 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.82 | 2.3e-27 |
| bmcs_cal_r vs calib | 0.83 | 9.43e-30 |
| bmcs_cal_r vs transfer | 0.53 | 0.244 |
| bmcs_cal_r vs bmcs_cal | 0.62 | 0.000134 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 5.45e-27 |
| transfer vs fresh | 0.79 | 3.24e-24 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.00075 0.00175 0.0015  0.002   0.00125 0.0005  0.00025 0.0001 ]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 57 [50-62] | 137 [125-144] | 239 [223-251] | 66 [59-77] | 0.28 / 0.39 / 0.41 | 0.00 / 0.00 / 0.00 | 0.51 / 0.29 / 0.37 |
| calib | 54 [49-63] | 128 [120-141] | 225 [210-243] | 77 [67-87] | 0.27 / 0.34 / 0.36 | 0.00 / 0.00 / 0.00 | 0.51 / 0.32 / 0.29 |
| transfer | 64 [57-70] | 142 [134-152] | 244 [232-258] | 60 [54-68] | 0.28 / 0.34 / 0.35 | 1.00 / 1.00 / 1.00 | 0.51 / 0.44 / 0.56 |
| bmcs_cal | 58 [53-64] | 136 [125-145] | 235 [222-250] | 69 [63-77] | 0.27 / 0.33 / 0.35 | 0.60 / 0.73 / 0.77 | 0.51 / 0.29 / 0.33 |
| bmcs_cal_r | 61 [54-68] | 143 [133-154] | 250 [234-265] | 56 [44-65] | 0.31 / 0.40 / 0.42 | 0.63 / 0.71 / 0.72 | 0.51 / 0.34 / 0.54 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.64 | 4.7e-06 |
| bmcs_cal_r vs calib | 0.72 | 2.03e-13 |
| bmcs_cal_r vs transfer | 0.50 | 0.961 |
| bmcs_cal_r vs bmcs_cal | 0.64 | 4.7e-06 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.73 | 1.12e-14 |
| transfer vs fresh | 0.64 | 1.81e-06 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 20.5 [9.6-240.0], never: 62/200
- calib: 47.9 [7.9-240.0], never: 88/200
- transfer: 35.0 [7.4-240.0], never: 80/200
- bmcs_cal: 23.7 [7.6-240.0], never: 82/200
- bmcs_cal_r: 19.0 [5.9-240.0], never: 68/200
