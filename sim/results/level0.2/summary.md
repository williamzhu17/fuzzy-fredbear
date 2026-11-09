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
| bmcs_cal | 66 [58-69] | 144 [136-154] | 246 [238-256] | 57 [54-62] | 0.70 / 0.71 / 0.74 | 0.87 / 0.94 / 0.94 | 0.81 / 0.65 / 0.81 |
| bmcs_cf | 66 [59-73] | 147 [139-158] | 254 [246-264] | 54 [49-60] | 0.72 / 0.74 / 0.76 | 0.89 / 0.95 / 0.94 | 0.79 / 0.61 / 0.84 |
| bmcs_cal_r | 69 [65-76] | 164 [154-170] | 280 [270-294] | 23 [20-30] | 0.82 / 0.90 / 0.90 | 0.84 / 0.88 / 0.86 | 0.81 / 0.64 / 0.72 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.83 | 5.68e-05 |
| bmcs_cal vs calib | 0.93 | 7.14e-08 |
| bmcs_cal vs transfer | 0.40 | 0.401 |
| bmcs_cal vs mix50_cal | 0.76 | 0.00148 |
| bmcs_cal vs bmcs_cf | 0.43 | 0.401 |
| bmcs_cal vs bmcs_cal_r | 0.17 | 4.55e-05 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.87 | 3.92e-06 |
| bmcs_cf vs calib | 0.95 | 1.38e-08 |
| bmcs_cf vs transfer | 0.48 | 0.75 |
| bmcs_cf vs mix50_cal | 0.81 | 0.000138 |
| bmcs_cf vs bmcs_cal | 0.57 | 0.703 |
| bmcs_cf vs bmcs_cal_r | 0.22 | 0.000711 |

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
| bmcs_cal | 68 [57-70] | 148 [138-155] | 252 [238-266] | 52 [47-61] | 0.71 / 0.72 / 0.74 | 0.84 / 0.94 / 0.94 | 0.81 / 0.59 / 0.77 |
| bmcs_cf | 62 [56-69] | 144 [134-152] | 254 [237-262] | 52 [47-58] | 0.71 / 0.71 / 0.74 | 0.88 / 0.93 / 0.93 | 0.81 / 0.60 / 0.82 |
| bmcs_cal_r | 71 [65-81] | 165 [152-169] | 278 [265-290] | 21 [14-27] | 0.81 / 0.87 / 0.87 | 0.84 / 0.87 / 0.84 | 0.81 / 0.61 / 0.77 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.79 | 0.000471 |
| bmcs_cal vs calib | 0.93 | 7.5e-08 |
| bmcs_cal vs transfer | 0.32 | 0.0299 |
| bmcs_cal vs mix50_cal | 0.74 | 0.00341 |
| bmcs_cal vs bmcs_cf | 0.58 | 0.287 |
| bmcs_cal vs bmcs_cal_r | 0.23 | 0.00168 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.74 | 0.00502 |
| bmcs_cf vs calib | 0.90 | 4.56e-07 |
| bmcs_cf vs transfer | 0.24 | 0.00221 |
| bmcs_cf vs mix50_cal | 0.69 | 0.0201 |
| bmcs_cf vs bmcs_cal | 0.42 | 0.287 |
| bmcs_cf vs bmcs_cal_r | 0.18 | 0.000128 |

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
| bmcs_cal | 37 [30-48] | 104 [91-122] | 192 [174-210] | 106 [98-127] | 0.39 / 0.58 / 0.64 | 0.08 / 0.06 / 0.08 | 0.81 / 0.85 / 0.82 |
| bmcs_cf | 42 [32-52] | 118 [108-136] | 225 [213-241] | 78 [69-85] | 0.46 / 0.72 / 0.78 | 0.10 / 0.06 / 0.07 | 0.81 / 0.86 / 0.84 |
| bmcs_cal_r | 56 [43-62] | 148 [128-161] | 262 [239-278] | 46 [31-67] | 0.53 / 0.80 / 0.81 | 0.16 / 0.10 / 0.13 | 0.81 / 0.89 / 0.87 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.25 | 0.00236 |
| bmcs_cal vs calib | 0.41 | 0.246 |
| bmcs_cal vs transfer | 0.95 | 1.32e-08 |
| bmcs_cal vs mix50_cal | 0.80 | 0.00023 |
| bmcs_cal vs bmcs_cf | 0.32 | 0.0359 |
| bmcs_cal vs bmcs_cal_r | 0.19 | 0.000184 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.40 | 0.333 |
| bmcs_cf vs calib | 0.60 | 0.333 |
| bmcs_cf vs transfer | 0.97 | 2.5e-09 |
| bmcs_cf vs mix50_cal | 0.91 | 2.05e-07 |
| bmcs_cf vs bmcs_cal | 0.68 | 0.0539 |
| bmcs_cf vs bmcs_cal_r | 0.26 | 0.00532 |

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
- bmcs_cal: 7.3 [5.2-14.7], never: 0/30
- bmcs_cf: 6.3 [4.5-9.6], never: 0/30
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
| bmcs_cal | 10 [8-13] | 21 [17-23] | 33 [29-42] | 25 [24-27] | 0.43 / 0.41 / 0.44 | 0.69 / 0.82 / 0.86 | 0.83 / 0.80 / 0.82 |
| bmcs_cf | 8 [6-10] | 19 [16-22] | 36 [31-38] | 26 [24-27] | 0.42 / 0.42 / 0.46 | 0.66 / 0.81 / 0.82 | 0.82 / 0.80 / 0.82 |
| bmcs_cal_r | 11 [6-13] | 25 [18-31] | 49 [37-54] | 15 [11-20] | 0.54 / 0.63 / 0.69 | 0.64 / 0.74 / 0.77 | 0.83 / 0.77 / 0.72 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.71 | 0.0304 |
| bmcs_cal vs calib | 0.86 | 9.9e-06 |
| bmcs_cal vs transfer | 0.38 | 0.195 |
| bmcs_cal vs mix50_cal | 0.66 | 0.138 |
| bmcs_cal vs bmcs_cf | 0.60 | 0.202 |
| bmcs_cal vs bmcs_cal_r | 0.36 | 0.195 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.63 | 0.274 |
| bmcs_cf vs calib | 0.82 | 8.74e-05 |
| bmcs_cf vs transfer | 0.27 | 0.01 |
| bmcs_cf vs mix50_cal | 0.56 | 0.463 |
| bmcs_cf vs bmcs_cal | 0.40 | 0.405 |
| bmcs_cf vs bmcs_cal_r | 0.29 | 0.021 |

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
| bmcs_cal | 21 [18-26] | 50 [46-57] | 89 [84-96] | 34 [32-36] | 0.28 / 0.29 / 0.31 | 0.69 / 0.81 / 0.80 | 0.51 / 0.52 / 0.52 |
| bmcs_cf | 22 [20-26] | 51 [46-56] | 88 [83-93] | 33 [31-35] | 0.28 / 0.29 / 0.32 | 0.70 / 0.81 / 0.79 | 0.51 / 0.52 / 0.63 |
| bmcs_cal_r | 22 [20-30] | 52 [44-64] | 95 [83-106] | 27 [18-30] | 0.32 / 0.38 / 0.38 | 0.63 / 0.69 / 0.70 | 0.51 / 0.57 / 0.60 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.61 | 0.473 |
| bmcs_cal vs calib | 0.74 | 0.00818 |
| bmcs_cal vs transfer | 0.38 | 0.473 |
| bmcs_cal vs mix50_cal | 0.74 | 0.00818 |
| bmcs_cal vs bmcs_cf | 0.48 | 0.79 |
| bmcs_cal vs bmcs_cal_r | 0.43 | 0.749 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.63 | 0.308 |
| bmcs_cf vs calib | 0.76 | 0.00255 |
| bmcs_cf vs transfer | 0.40 | 0.527 |
| bmcs_cf vs mix50_cal | 0.75 | 0.00418 |
| bmcs_cf vs bmcs_cal | 0.52 | 0.909 |
| bmcs_cf vs bmcs_cal_r | 0.44 | 0.909 |

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
| bmcs_cal | 19 [17-24] | 46 [42-50] | 80 [75-88] | 40 [37-42] | 0.19 / 0.22 / 0.25 | 0.61 / 0.71 / 0.72 | 0.51 / 0.50 / 0.51 |
| bmcs_cf | 22 [17-26] | 49 [43-56] | 90 [78-95] | 36 [35-37] | 0.22 / 0.27 / 0.28 | 0.64 / 0.70 / 0.70 | 0.51 / 0.54 / 0.61 |
| bmcs_cal_r | 22 [20-25] | 54 [50-58] | 92 [85-100] | 29 [22-34] | 0.24 / 0.31 / 0.34 | 0.55 / 0.60 / 0.61 | 0.51 / 0.61 / 0.63 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.46 | 1 |
| bmcs_cal vs calib | 0.59 | 0.625 |
| bmcs_cal vs transfer | 0.28 | 0.018 |
| bmcs_cal vs mix50_cal | 0.48 | 1 |
| bmcs_cal vs bmcs_cf | 0.39 | 0.563 |
| bmcs_cal vs bmcs_cal_r | 0.28 | 0.018 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.58 | 0.607 |
| bmcs_cf vs calib | 0.70 | 0.0526 |
| bmcs_cf vs transfer | 0.38 | 0.584 |
| bmcs_cf vs mix50_cal | 0.58 | 0.607 |
| bmcs_cf vs bmcs_cal | 0.61 | 0.584 |
| bmcs_cf vs bmcs_cal_r | 0.39 | 0.584 |

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
- bmcs_cal: 240.0 [240.0-240.0], never: 26/30
- bmcs_cf: 240.0 [121.4-240.0], never: 21/30
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
| bmcs_cal | 24 [21-27] | 55 [50-62] | 112 [101-121] | 74 [69-78] | 0.28 / 0.20 / 0.26 | 0.67 / 0.81 / 0.81 | 0.52 / 0.53 / 0.51 |
| bmcs_cf | 22 [17-23] | 50 [44-55] | 107 [101-119] | 70 [67-74] | 0.24 / 0.19 / 0.31 | 0.67 / 0.77 / 0.77 | 0.52 / 0.55 / 0.59 |
| bmcs_cal_r | 26 [22-29] | 62 [54-65] | 120 [110-126] | 64 [58-70] | 0.37 / 0.20 / 0.30 | 0.70 / 0.78 / 0.79 | 0.52 / 0.59 / 0.58 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.55 | 0.566 |
| bmcs_cal vs calib | 0.75 | 0.0064 |
| bmcs_cal vs transfer | 0.42 | 0.566 |
| bmcs_cal vs mix50_cal | 0.65 | 0.164 |
| bmcs_cal vs bmcs_cf | 0.62 | 0.306 |
| bmcs_cal vs bmcs_cal_r | 0.33 | 0.132 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.43 | 0.749 |
| bmcs_cf vs calib | 0.65 | 0.182 |
| bmcs_cf vs transfer | 0.30 | 0.044 |
| bmcs_cf vs mix50_cal | 0.52 | 0.773 |
| bmcs_cf vs bmcs_cal | 0.38 | 0.306 |
| bmcs_cf vs bmcs_cal_r | 0.24 | 0.00408 |

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
| bmcs_cal | 21 [18-22] | 44 [41-48] | 74 [68-80] | 21 [19-23] | 0.20 / 0.20 / 0.24 | 0.67 / 0.76 / 0.75 | 0.50 / 0.53 / 0.51 |
| bmcs_cf | 20 [17-23] | 45 [41-49] | 75 [72-80] | 20 [19-22] | 0.19 / 0.23 / 0.25 | 0.66 / 0.76 / 0.76 | 0.50 / 0.53 / 0.61 |
| bmcs_cal_r | 22 [19-26] | 47 [42-52] | 78 [74-85] | 18 [12-22] | 0.19 / 0.20 / 0.25 | 0.62 / 0.71 / 0.72 | 0.50 / 0.57 / 0.61 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.59 | 0.629 |
| bmcs_cal vs calib | 0.78 | 0.00104 |
| bmcs_cal vs transfer | 0.28 | 0.0198 |
| bmcs_cal vs mix50_cal | 0.60 | 0.629 |
| bmcs_cal vs bmcs_cf | 0.47 | 0.728 |
| bmcs_cal vs bmcs_cal_r | 0.39 | 0.629 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.61 | 0.508 |
| bmcs_cf vs calib | 0.80 | 0.000349 |
| bmcs_cf vs transfer | 0.31 | 0.0567 |
| bmcs_cf vs mix50_cal | 0.61 | 0.508 |
| bmcs_cf vs bmcs_cal | 0.53 | 0.728 |
| bmcs_cf vs bmcs_cal_r | 0.42 | 0.6 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.90 | 1.82e-07 |
| transfer vs fresh | 0.78 | 0.000158 |
