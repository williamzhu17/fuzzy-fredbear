# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 0.2.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 47 [40-54] | 126 [116-134] | 232 [224-238] | 72 [66-78] | 0.47 / 0.72 / 0.78 | 0.00 / 0.00 / 0.00 | 0.80 / 0.43 / 0.61 |
| calib | 38 [33-46] | 108 [98-122] | 206 [182-220] | 105 [98-112] | 0.39 / 0.58 / 0.64 | 0.00 / 0.00 / 0.00 | 0.81 / 0.36 / 0.26 |
| transfer | 66 [60-72] | 150 [140-156] | 254 [243-263] | 49 [46-55] | 0.75 / 0.74 / 0.76 | 1.00 / 1.00 / 1.00 | 0.79 / 0.78 / 0.89 |
| mix50_cal | 58 [48-66] | 131 [117-134] | 231 [212-246] | 79 [73-86] | 0.60 / 0.65 / 0.70 | 0.50 / 0.50 / 0.50 | 0.80 / 0.40 / 0.33 |
| mix50_cal_r | 69 [58-77] | 158 [150-171] | 272 [264-280] | 32 [23-36] | 0.79 / 0.89 / 0.90 | 0.50 / 0.50 / 0.50 | 0.81 / 0.57 / 0.70 |
| bmcs_cal_r | 69 [65-76] | 164 [154-170] | 280 [270-294] | 23 [20-30] | 0.82 / 0.90 / 0.90 | 0.84 / 0.88 / 0.86 | 0.81 / 0.64 / 0.72 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.94 | 1.57e-08 |
| bmcs_cal_r vs calib | 0.99 | 3.82e-10 |
| bmcs_cal_r vs transfer | 0.77 | 0.000687 |
| bmcs_cal_r vs mix50_cal | 0.93 | 4.37e-08 |
| bmcs_cal_r vs mix50_cal_r | 0.54 | 0.554 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.95 | 4.62e-09 |
| transfer vs fresh | 0.88 | 3.48e-07 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.00000e-03 3.69104e-04 1.45322e-03 2.17457e-04 1.66817e-04 9.48626e-05
 2.38137e-05 7.67737e-06]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 48 [42-52] | 130 [125-140] | 242 [229-254] | 66 [59-70] | 0.45 / 0.68 / 0.73 | 0.00 / 0.00 / 0.00 | 0.82 / 0.44 / 0.59 |
| calib | 45 [38-52] | 116 [103-128] | 210 [194-220] | 93 [84-108] | 0.42 / 0.55 / 0.60 | 0.00 / 0.00 / 0.00 | 0.83 / 0.37 / 0.32 |
| transfer | 70 [66-76] | 156 [148-169] | 261 [250-269] | 42 [39-46] | 0.81 / 0.76 / 0.76 | 1.00 / 1.00 / 1.00 | 0.80 / 0.73 / 0.86 |
| mix50_cal | 60 [53-66] | 132 [116-145] | 230 [208-245] | 72 [65-82] | 0.63 / 0.64 / 0.69 | 0.51 / 0.50 / 0.50 | 0.82 / 0.40 / 0.34 |
| mix50_cal_r | 70 [61-76] | 161 [148-167] | 281 [261-295] | 26 [20-32] | 0.78 / 0.86 / 0.87 | 0.50 / 0.50 / 0.50 | 0.81 / 0.58 / 0.74 |
| bmcs_cal_r | 71 [65-81] | 165 [152-169] | 278 [265-290] | 21 [14-27] | 0.81 / 0.87 / 0.87 | 0.84 / 0.87 / 0.84 | 0.81 / 0.61 / 0.77 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.94 | 1.38e-08 |
| bmcs_cal_r vs calib | 0.99 | 4.24e-10 |
| bmcs_cal_r vs transfer | 0.60 | 0.371 |
| bmcs_cal_r vs mix50_cal | 0.90 | 3.16e-07 |
| bmcs_cal_r vs mix50_cal_r | 0.57 | 0.371 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.98 | 3.35e-10 |
| transfer vs fresh | 0.92 | 3.3e-08 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [4.e-05 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 2.e-03 2.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 46 [41-51] | 125 [116-143] | 228 [214-244] | 69 [63-84] | 0.46 / 0.73 / 0.79 | 0.00 / 0.00 / 0.00 | 0.81 / 0.90 / 0.85 |
| calib | 40 [34-54] | 110 [98-126] | 203 [191-221] | 101 [87-110] | 0.44 / 0.61 / 0.67 | 0.00 / 0.00 / 0.00 | 0.81 / 0.89 / 0.91 |
| transfer | 22 [16-25] | 62 [50-76] | 128 [114-147] | 181 [160-189] | 0.02 / 0.21 / 0.34 | 1.00 / 1.00 / 1.00 | 0.81 / 0.77 / 0.73 |
| mix50_cal | 27 [23-35] | 81 [74-94] | 165 [142-179] | 140 [130-150] | 0.21 / 0.41 / 0.51 | 0.50 / 0.50 / 0.50 | 0.81 / 0.64 / 0.47 |
| mix50_cal_r | 55 [35-64] | 142 [103-159] | 260 [208-286] | 47 [32-91] | 0.51 / 0.73 / 0.77 | 0.50 / 0.50 / 0.50 | 0.81 / 0.89 / 0.90 |
| bmcs_cal_r | 56 [43-62] | 148 [128-161] | 262 [239-278] | 46 [31-67] | 0.53 / 0.80 / 0.81 | 0.16 / 0.10 / 0.13 | 0.81 / 0.89 / 0.87 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.70 | 0.0136 |
| bmcs_cal_r vs calib | 0.79 | 0.000384 |
| bmcs_cal_r vs transfer | 0.98 | 9.24e-10 |
| bmcs_cal_r vs mix50_cal | 0.94 | 1.9e-08 |
| bmcs_cal_r vs mix50_cal_r | 0.55 | 0.52 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.02 | 2.04e-10 |
| transfer vs fresh | 0.01 | 9.88e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 5.9 [4.5-8.8], never: 0/30
- calib: 6.9 [4.1-14.6], never: 0/30
- transfer: 152.3 [31.8-240.0], never: 13/30
- mix50_cal: 26.7 [13.3-44.2], never: 0/30
- mix50_cal_r: 3.9 [2.9-16.5], never: 2/30
- bmcs_cal_r: 4.9 [2.4-10.4], never: 1/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [4.0e-04 2.0e-04 1.2e-04 8.0e-05 4.0e-05 2.0e-05 8.0e-06 4.0e-06]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 6 [5-8] | 18 [13-20] | 31 [26-38] | 29 [27-33] | 0.23 / 0.38 / 0.45 | 0.00 / 0.00 / 0.00 | 0.82 / 0.81 / 0.78 |
| calib | 6 [3-7] | 12 [10-16] | 20 [17-24] | 40 [38-41] | 0.17 / 0.20 / 0.23 | 0.00 / 0.00 / 0.00 | 0.82 / 0.74 / 0.68 |
| transfer | 12 [10-15] | 23 [20-26] | 40 [38-43] | 22 [21-23] | 0.54 / 0.45 / 0.47 | 1.00 / 1.00 / 1.00 | 0.82 / 0.81 / 0.80 |
| mix50_cal | 8 [6-9] | 18 [14-21] | 28 [26-36] | 31 [30-32] | 0.35 / 0.33 / 0.36 | 0.50 / 0.50 / 0.50 | 0.83 / 0.81 / 0.78 |
| mix50_cal_r | 7 [6-11] | 19 [15-25] | 39 [32-46] | 21 [14-23] | 0.40 / 0.55 / 0.66 | 0.49 / 0.50 / 0.50 | 0.83 / 0.80 / 0.72 |
| bmcs_cal_r | 11 [6-13] | 25 [18-31] | 49 [37-54] | 15 [11-20] | 0.54 / 0.63 / 0.69 | 0.64 / 0.74 / 0.77 | 0.83 / 0.77 / 0.72 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.78 | 0.000787 |
| bmcs_cal_r vs calib | 0.86 | 8.71e-06 |
| bmcs_cal_r vs transfer | 0.57 | 0.354 |
| bmcs_cal_r vs mix50_cal | 0.75 | 0.00288 |
| bmcs_cal_r vs mix50_cal_r | 0.65 | 0.098 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.95 | 4.59e-09 |
| transfer vs fresh | 0.83 | 1.33e-05 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [8.e-04 7.e-04 6.e-04 5.e-04 3.e-04 2.e-04 1.e-04 4.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 20 [18-24] | 48 [41-52] | 84 [78-92] | 37 [35-41] | 0.20 / 0.26 / 0.27 | 0.00 / 0.00 / 0.00 | 0.51 / 0.45 / 0.49 |
| calib | 19 [14-21] | 42 [38-50] | 76 [70-83] | 45 [42-47] | 0.18 / 0.23 / 0.24 | 0.00 / 0.00 / 0.00 | 0.52 / 0.37 / 0.30 |
| transfer | 26 [22-29] | 54 [51-58] | 92 [83-96] | 30 [28-32] | 0.32 / 0.29 / 0.32 | 1.00 / 1.00 / 1.00 | 0.52 / 0.67 / 0.71 |
| mix50_cal | 20 [17-23] | 46 [41-48] | 76 [74-83] | 39 [38-41] | 0.24 / 0.24 / 0.26 | 0.49 / 0.50 / 0.50 | 0.52 / 0.43 / 0.39 |
| mix50_cal_r | 22 [18-24] | 55 [48-60] | 98 [92-105] | 26 [22-30] | 0.30 / 0.38 / 0.40 | 0.50 / 0.50 / 0.50 | 0.51 / 0.55 / 0.59 |
| bmcs_cal_r | 22 [20-30] | 52 [44-64] | 95 [83-106] | 27 [18-30] | 0.32 / 0.38 / 0.38 | 0.63 / 0.69 / 0.70 | 0.51 / 0.57 / 0.60 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.65 | 0.119 |
| bmcs_cal_r vs calib | 0.78 | 0.000756 |
| bmcs_cal_r vs transfer | 0.50 | 1 |
| bmcs_cal_r vs mix50_cal | 0.74 | 0.00486 |
| bmcs_cal_r vs mix50_cal_r | 0.48 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 1.99e-05 |
| transfer vs fresh | 0.72 | 0.00322 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [3.e-04 7.e-04 6.e-04 8.e-04 5.e-04 2.e-04 1.e-04 4.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 19 [15-21] | 46 [43-54] | 86 [76-93] | 35 [33-38] | 0.21 / 0.31 / 0.34 | 0.00 / 0.00 / 0.00 | 0.51 / 0.47 / 0.56 |
| calib | 18 [13-22] | 41 [38-52] | 82 [69-88] | 45 [41-47] | 0.18 / 0.24 / 0.25 | 0.00 / 0.00 / 0.00 | 0.51 / 0.41 / 0.38 |
| transfer | 24 [20-30] | 54 [47-60] | 86 [79-101] | 34 [31-37] | 0.23 / 0.25 / 0.26 | 1.00 / 1.00 / 1.00 | 0.51 / 0.65 / 0.65 |
| mix50_cal | 20 [17-24] | 46 [40-56] | 79 [69-90] | 43 [39-44] | 0.17 / 0.20 / 0.22 | 0.51 / 0.50 / 0.50 | 0.51 / 0.47 / 0.39 |
| mix50_cal_r | 22 [19-26] | 53 [44-58] | 90 [83-98] | 29 [26-35] | 0.21 / 0.31 / 0.34 | 0.50 / 0.49 / 0.50 | 0.51 / 0.60 / 0.66 |
| bmcs_cal_r | 22 [20-25] | 54 [50-58] | 92 [85-100] | 29 [22-34] | 0.24 / 0.31 / 0.34 | 0.55 / 0.60 / 0.61 | 0.51 / 0.61 / 0.63 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.69 | 0.0445 |
| bmcs_cal_r vs calib | 0.77 | 0.00139 |
| bmcs_cal_r vs transfer | 0.49 | 0.929 |
| bmcs_cal_r vs mix50_cal | 0.67 | 0.072 |
| bmcs_cal_r vs mix50_cal_r | 0.56 | 0.773 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.78 | 0.000408 |
| transfer vs fresh | 0.70 | 0.00842 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 198.8 [31.7-240.0], never: 15/30
- calib: 240.0 [113.0-240.0], never: 22/30
- transfer: 240.0 [240.0-240.0], never: 24/30
- mix50_cal: 240.0 [240.0-240.0], never: 28/30
- mix50_cal_r: 106.7 [18.0-240.0], never: 13/30
- bmcs_cal_r: 66.0 [9.9-240.0], never: 14/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [8.e-04 7.e-04 6.e-04 3.e-04 3.e-04 2.e-04 1.e-04 4.e-05]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 20 [19-23] | 53 [48-60] | 116 [99-126] | 69 [62-76] | 0.21 / 0.20 / 0.35 | 0.00 / 0.00 / 0.00 | 0.52 / 0.44 / 0.50 |
| calib | 20 [17-24] | 46 [41-54] | 98 [92-110] | 79 [77-86] | 0.17 / 0.17 / 0.29 | 0.00 / 0.00 / 0.00 | 0.52 / 0.38 / 0.31 |
| transfer | 26 [22-30] | 58 [53-66] | 113 [103-123] | 69 [66-74] | 0.33 / 0.19 / 0.26 | 1.00 / 1.00 / 1.00 | 0.52 / 0.66 / 0.65 |
| mix50_cal | 22 [19-25] | 50 [44-56] | 106 [93-116] | 77 [72-81] | 0.25 / 0.19 / 0.27 | 0.50 / 0.50 / 0.50 | 0.52 / 0.44 / 0.38 |
| mix50_cal_r | 21 [20-27] | 55 [45-61] | 112 [99-122] | 68 [60-75] | 0.33 / 0.20 / 0.27 | 0.51 / 0.50 / 0.50 | 0.52 / 0.57 / 0.59 |
| bmcs_cal_r | 26 [22-29] | 62 [54-65] | 120 [110-126] | 64 [58-70] | 0.37 / 0.20 / 0.30 | 0.70 / 0.78 / 0.79 | 0.52 / 0.59 / 0.58 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.72 | 0.0106 |
| bmcs_cal_r vs calib | 0.87 | 3.3e-06 |
| bmcs_cal_r vs transfer | 0.58 | 0.297 |
| bmcs_cal_r vs mix50_cal | 0.82 | 9.26e-05 |
| bmcs_cal_r vs mix50_cal_r | 0.70 | 0.0183 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 8.21e-05 |
| transfer vs fresh | 0.65 | 0.0473 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [8.e-04 7.e-04 6.e-04 5.e-04 3.e-04 2.e-04 1.e-04 4.e-05]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 16 [14-20] | 44 [39-46] | 73 [69-79] | 22 [19-24] | 0.15 / 0.20 / 0.24 | 0.00 / 0.00 / 0.00 | 0.50 / 0.45 / 0.51 |
| calib | 17 [13-21] | 38 [36-42] | 68 [62-73] | 28 [26-29] | 0.14 / 0.18 / 0.20 | 0.00 / 0.00 / 0.00 | 0.50 / 0.39 / 0.33 |
| transfer | 24 [20-25] | 50 [46-54] | 80 [74-86] | 17 [16-19] | 0.23 / 0.22 / 0.25 | 1.00 / 1.00 / 1.00 | 0.51 / 0.65 / 0.66 |
| mix50_cal | 19 [16-23] | 42 [38-47] | 72 [66-78] | 24 [22-25] | 0.19 / 0.21 / 0.25 | 0.50 / 0.50 / 0.50 | 0.50 / 0.45 / 0.40 |
| mix50_cal_r | 22 [18-26] | 46 [40-53] | 80 [73-85] | 17 [14-20] | 0.15 / 0.21 / 0.27 | 0.50 / 0.50 / 0.50 | 0.50 / 0.56 / 0.58 |
| bmcs_cal_r | 22 [19-26] | 47 [42-52] | 78 [74-85] | 18 [12-22] | 0.19 / 0.20 / 0.25 | 0.62 / 0.71 / 0.72 | 0.50 / 0.57 / 0.61 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.68 | 0.0571 |
| bmcs_cal_r vs calib | 0.82 | 9.71e-05 |
| bmcs_cal_r vs transfer | 0.42 | 0.628 |
| bmcs_cal_r vs mix50_cal | 0.68 | 0.0571 |
| bmcs_cal_r vs mix50_cal_r | 0.54 | 0.641 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.90 | 1.82e-07 |
| transfer vs fresh | 0.78 | 0.000158 |
