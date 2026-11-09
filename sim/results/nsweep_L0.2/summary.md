# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 0.2.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 47 [41-58] | 130 [119-139] | 234 [220-250] | 71 [66-82] | 0.50 / 0.71 / 0.78 | 0.00 / 0.00 / 0.00 | 0.51 / 0.14 / 0.08 |
| transfer | 57 [51-60] | 138 [128-148] | 245 [226-254] | 60 [54-68] | 0.58 / 0.74 / 0.79 | 1.00 / 1.00 / 1.00 | 0.49 / 0.26 / 0.19 |
| bmcs_cal | 53 [46-60] | 137 [123-142] | 242 [225-254] | 65 [57-72] | 0.55 / 0.73 / 0.78 | 0.79 / 0.82 / 0.81 | 0.50 / 0.22 / 0.15 |
| bmcs_cal_r | 62 [51-70] | 146 [135-162] | 264 [242-280] | 36 [26-48] | 0.70 / 0.86 / 0.88 | 0.70 / 0.75 / 0.73 | 0.50 / 0.35 / 0.33 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.75 | 0.00285 |
| bmcs_cal_r vs transfer | 0.67 | 0.025 |
| bmcs_cal_r vs bmcs_cal | 0.70 | 0.0148 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.64 | 0.0593 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 43 [39-50] | 119 [100-129] | 218 [199-226] | 83 [78-92] | 0.46 / 0.67 / 0.73 | 0.00 / 0.00 / 0.00 | 0.67 / 0.22 / 0.13 |
| transfer | 56 [52-61] | 134 [125-143] | 237 [228-250] | 59 [56-63] | 0.63 / 0.73 / 0.78 | 1.00 / 1.00 / 1.00 | 0.65 / 0.52 / 0.45 |
| bmcs_cal | 60 [48-66] | 136 [127-146] | 236 [221-258] | 66 [54-71] | 0.61 / 0.73 / 0.77 | 0.84 / 0.89 / 0.86 | 0.66 / 0.43 / 0.34 |
| bmcs_cal_r | 68 [62-73] | 159 [151-168] | 275 [261-285] | 32 [23-38] | 0.75 / 0.87 / 0.89 | 0.81 / 0.85 / 0.84 | 0.66 / 0.52 / 0.53 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.97 | 1.08e-09 |
| bmcs_cal_r vs transfer | 0.87 | 1.39e-06 |
| bmcs_cal_r vs bmcs_cal | 0.82 | 2.26e-05 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 1.12e-05 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 38 [33-46] | 108 [98-122] | 206 [182-220] | 105 [98-112] | 0.39 / 0.58 / 0.64 | 0.00 / 0.00 / 0.00 | 0.81 / 0.36 / 0.26 |
| transfer | 66 [60-72] | 150 [140-156] | 254 [243-263] | 49 [46-55] | 0.75 / 0.74 / 0.76 | 1.00 / 1.00 / 1.00 | 0.79 / 0.78 / 0.89 |
| bmcs_cal | 66 [58-69] | 144 [136-154] | 246 [238-256] | 57 [54-62] | 0.70 / 0.71 / 0.74 | 0.87 / 0.94 / 0.94 | 0.81 / 0.65 / 0.81 |
| bmcs_cal_r | 69 [65-76] | 164 [154-170] | 280 [270-294] | 23 [20-30] | 0.82 / 0.90 / 0.90 | 0.84 / 0.88 / 0.86 | 0.81 / 0.64 / 0.72 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.99 | 2.29e-10 |
| bmcs_cal_r vs transfer | 0.77 | 0.000343 |
| bmcs_cal_r vs bmcs_cal | 0.83 | 1.82e-05 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.95 | 2.31e-09 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 39 [32-45] | 97 [89-104] | 165 [146-179] | 143 [135-154] | 0.35 / 0.43 / 0.43 | 0.00 / 0.00 / 0.00 | 0.87 / 0.53 / 0.51 |
| transfer | 78 [71-86] | 162 [151-171] | 264 [248-280] | 43 [36-46] | 0.90 / 0.74 / 0.70 | 1.00 / 1.00 / 1.00 | 0.86 / 0.67 / 0.95 |
| bmcs_cal | 70 [63-76] | 155 [141-162] | 253 [242-266] | 50 [46-58] | 0.84 / 0.72 / 0.68 | 0.90 / 0.98 / 0.98 | 0.87 / 0.68 / 0.95 |
| bmcs_cal_r | 71 [63-78] | 165 [153-184] | 285 [262-305] | 16 [10-19] | 0.87 / 0.95 / 0.94 | 0.85 / 0.92 / 0.88 | 0.87 / 0.68 / 0.84 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 1.00 | 1.09e-10 |
| bmcs_cal_r vs transfer | 0.57 | 0.383 |
| bmcs_cal_r vs bmcs_cal | 0.72 | 0.00619 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 1.00 | 3.84e-11 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.00000e-03 3.69104e-04 1.45322e-03 2.17457e-04 1.66817e-04 9.48626e-05
 2.38137e-05 7.67737e-06]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 46 [40-55] | 116 [104-130] | 216 [202-237] | 85 [77-92] | 0.36 / 0.54 / 0.62 | 0.00 / 0.00 / 0.00 | 0.50 / 0.18 / 0.12 |
| transfer | 60 [55-65] | 142 [136-150] | 248 [231-264] | 58 [53-64] | 0.56 / 0.70 / 0.74 | 1.00 / 1.00 / 1.00 | 0.49 / 0.25 / 0.18 |
| bmcs_cal | 58 [52-63] | 138 [125-148] | 242 [231-256] | 64 [58-72] | 0.52 / 0.66 / 0.71 | 0.79 / 0.82 / 0.80 | 0.50 / 0.21 / 0.15 |
| bmcs_cal_r | 64 [57-72] | 148 [139-165] | 262 [248-278] | 36 [25-52] | 0.62 / 0.68 / 0.72 | 0.71 / 0.74 / 0.73 | 0.50 / 0.36 / 0.37 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.91 | 1.58e-07 |
| bmcs_cal_r vs transfer | 0.63 | 0.0932 |
| bmcs_cal_r vs bmcs_cal | 0.70 | 0.0173 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.87 | 1.14e-06 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 43 [36-49] | 116 [103-126] | 215 [204-222] | 86 [81-99] | 0.37 / 0.56 / 0.63 | 0.00 / 0.00 / 0.00 | 0.69 / 0.30 / 0.19 |
| transfer | 66 [58-73] | 145 [136-157] | 248 [234-264] | 51 [44-58] | 0.68 / 0.73 / 0.77 | 1.00 / 1.00 / 1.00 | 0.66 / 0.49 / 0.43 |
| bmcs_cal | 59 [52-67] | 140 [133-151] | 246 [235-258] | 58 [50-65] | 0.62 / 0.72 / 0.75 | 0.81 / 0.87 / 0.84 | 0.68 / 0.41 / 0.32 |
| bmcs_cal_r | 68 [63-78] | 158 [152-171] | 276 [268-299] | 27 [20-36] | 0.75 / 0.86 / 0.86 | 0.78 / 0.82 / 0.80 | 0.68 / 0.51 / 0.56 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.97 | 1.31e-09 |
| bmcs_cal_r vs transfer | 0.77 | 0.000408 |
| bmcs_cal_r vs bmcs_cal | 0.83 | 2.4e-05 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.89 | 2.01e-07 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 45 [38-52] | 116 [103-128] | 210 [194-220] | 93 [84-108] | 0.42 / 0.55 / 0.60 | 0.00 / 0.00 / 0.00 | 0.83 / 0.37 / 0.32 |
| transfer | 70 [66-76] | 156 [148-169] | 261 [250-269] | 42 [39-46] | 0.81 / 0.76 / 0.76 | 1.00 / 1.00 / 1.00 | 0.80 / 0.73 / 0.86 |
| bmcs_cal | 68 [57-70] | 148 [138-155] | 252 [238-266] | 52 [47-61] | 0.71 / 0.72 / 0.74 | 0.84 / 0.94 / 0.94 | 0.81 / 0.59 / 0.77 |
| bmcs_cal_r | 71 [65-81] | 165 [152-169] | 278 [265-290] | 21 [14-27] | 0.81 / 0.87 / 0.87 | 0.84 / 0.87 / 0.84 | 0.81 / 0.61 / 0.77 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.99 | 2.54e-10 |
| bmcs_cal_r vs transfer | 0.60 | 0.186 |
| bmcs_cal_r vs bmcs_cal | 0.77 | 0.000838 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.98 | 1.68e-10 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 38 [28-46] | 89 [77-102] | 160 [140-184] | 141 [124-156] | 0.32 / 0.39 / 0.39 | 0.00 / 0.00 / 0.00 | 0.87 / 0.56 / 0.55 |
| transfer | 80 [71-83] | 165 [156-173] | 272 [250-287] | 35 [31-44] | 0.94 / 0.78 / 0.73 | 1.00 / 1.00 / 1.00 | 0.87 / 0.60 / 0.97 |
| bmcs_cal | 71 [65-78] | 152 [141-161] | 255 [236-272] | 43 [35-60] | 0.87 / 0.75 / 0.71 | 0.88 / 0.96 / 0.97 | 0.88 / 0.61 / 0.95 |
| bmcs_cal_r | 78 [69-84] | 170 [162-177] | 298 [277-303] | 13 [10-16] | 0.90 / 0.96 / 0.96 | 0.88 / 0.94 / 0.92 | 0.88 / 0.54 / 0.78 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 1.00 | 8.99e-11 |
| bmcs_cal_r vs transfer | 0.63 | 0.0946 |
| bmcs_cal_r vs bmcs_cal | 0.80 | 0.000105 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 1.00 | 3.49e-11 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [4.e-05 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 2.e-03 2.e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 49 [40-55] | 124 [113-133] | 232 [223-246] | 74 [68-84] | 0.49 / 0.73 / 0.78 | 0.00 / 0.00 / 0.00 | 0.54 / 0.32 / 0.26 |
| transfer | 44 [35-51] | 114 [103-127] | 218 [201-232] | 86 [75-95] | 0.40 / 0.67 / 0.74 | 1.00 / 1.00 / 1.00 | 0.52 / 0.16 / 0.13 |
| bmcs_cal | 44 [38-50] | 124 [106-131] | 226 [198-236] | 80 [72-92] | 0.45 / 0.68 / 0.75 | 0.34 / 0.32 / 0.31 | 0.53 / 0.20 / 0.14 |
| bmcs_cal_r | 54 [41-68] | 138 [122-156] | 250 [222-269] | 52 [31-63] | 0.54 / 0.77 / 0.80 | 0.37 / 0.35 / 0.36 | 0.53 / 0.47 / 0.49 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.71 | 0.00635 |
| bmcs_cal_r vs transfer | 0.79 | 0.000311 |
| bmcs_cal_r vs bmcs_cal | 0.72 | 0.00635 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.37 | 0.0758 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 5.2 [3.6-6.5], never: 0/30
- transfer: 7.2 [5.9-10.7], never: 0/30
- bmcs_cal: 6.0 [4.4-9.0], never: 0/30
- bmcs_cal_r: 3.9 [2.2-9.5], never: 1/30

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 43 [36-52] | 114 [107-124] | 211 [199-231] | 88 [77-102] | 0.41 / 0.64 / 0.71 | 0.00 / 0.00 / 0.00 | 0.70 / 0.61 / 0.58 |
| transfer | 29 [24-35] | 93 [78-109] | 180 [159-206] | 123 [96-151] | 0.18 / 0.48 / 0.58 | 1.00 / 1.00 / 1.00 | 0.70 / 0.39 / 0.32 |
| bmcs_cal | 37 [35-47] | 107 [99-119] | 205 [194-223] | 95 [88-109] | 0.37 / 0.61 / 0.69 | 0.20 / 0.18 / 0.20 | 0.69 / 0.42 / 0.32 |
| bmcs_cal_r | 57 [48-65] | 146 [134-154] | 256 [233-267] | 45 [35-62] | 0.58 / 0.80 / 0.85 | 0.24 / 0.22 / 0.26 | 0.69 / 0.70 / 0.73 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.82 | 2.12e-05 |
| bmcs_cal_r vs transfer | 0.89 | 4.58e-07 |
| bmcs_cal_r vs bmcs_cal | 0.86 | 2.74e-06 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.24 | 0.00051 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 9.5 [4.9-15.1], never: 0/30
- transfer: 21.2 [9.9-41.9], never: 2/30
- bmcs_cal: 10.7 [5.5-14.2], never: 0/30
- bmcs_cal_r: 3.8 [2.5-7.7], never: 0/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 40 [34-54] | 110 [98-126] | 203 [191-221] | 101 [87-110] | 0.44 / 0.61 / 0.67 | 0.00 / 0.00 / 0.00 | 0.81 / 0.89 / 0.91 |
| transfer | 22 [16-25] | 62 [50-76] | 128 [114-147] | 181 [160-189] | 0.02 / 0.21 / 0.34 | 1.00 / 1.00 / 1.00 | 0.81 / 0.77 / 0.73 |
| bmcs_cal | 37 [30-48] | 104 [91-122] | 192 [174-210] | 106 [98-127] | 0.39 / 0.58 / 0.64 | 0.08 / 0.06 / 0.08 | 0.81 / 0.85 / 0.82 |
| bmcs_cal_r | 56 [43-62] | 148 [128-161] | 262 [239-278] | 46 [31-67] | 0.53 / 0.80 / 0.81 | 0.16 / 0.10 / 0.13 | 0.81 / 0.89 / 0.87 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.79 | 0.000128 |
| bmcs_cal_r vs transfer | 0.98 | 5.55e-10 |
| bmcs_cal_r vs bmcs_cal | 0.81 | 7.37e-05 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.02 | 2.04e-10 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 6.9 [4.1-14.6], never: 0/30
- transfer: 152.3 [31.8-240.0], never: 13/30
- bmcs_cal: 7.3 [5.2-14.7], never: 0/30
- bmcs_cal_r: 4.9 [2.4-10.4], never: 1/30

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 36 [30-42] | 92 [80-104] | 160 [138-172] | 143 [138-158] | 0.33 / 0.42 / 0.42 | 0.00 / 0.00 / 0.00 | 0.87 / 0.94 / 0.93 |
| transfer | 13 [11-16] | 40 [33-45] | 75 [66-84] | 228 [227-229] | 0.00 / 0.00 / 0.03 | 1.00 / 1.00 / 1.00 | 0.89 / 0.93 / 0.95 |
| bmcs_cal | 34 [26-40] | 90 [74-98] | 154 [135-169] | 146 [134-160] | 0.36 / 0.41 / 0.41 | 0.06 / 0.00 / 0.01 | 0.88 / 0.95 / 0.93 |
| bmcs_cal_r | 50 [43-56] | 144 [132-152] | 258 [238-272] | 48 [33-57] | 0.55 / 0.88 / 0.88 | 0.06 / 0.01 / 0.01 | 0.88 / 0.94 / 0.87 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.95 | 2.8e-09 |
| bmcs_cal_r vs transfer | 1.00 | 8.49e-11 |
| bmcs_cal_r vs bmcs_cal | 0.95 | 2.8e-09 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.01 | 4.68e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 12.2 [9.8-31.6], never: 6/30
- transfer: 240.0 [240.0-240.0], never: 30/30
- bmcs_cal: 13.9 [5.7-65.0], never: 6/30
- bmcs_cal_r: 6.8 [4.4-8.8], never: 1/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [4.0e-04 2.0e-04 1.2e-04 8.0e-05 4.0e-05 2.0e-05 8.0e-06 4.0e-06]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 5 [4-9] | 14 [12-19] | 26 [22-31] | 34 [32-36] | 0.21 / 0.31 / 0.38 | 0.00 / 0.00 / 0.00 | 0.54 / 0.40 / 0.31 |
| transfer | 8 [5-10] | 20 [14-22] | 33 [29-40] | 27 [25-29] | 0.32 / 0.40 / 0.48 | 1.00 / 1.00 / 1.00 | 0.52 / 0.40 / 0.38 |
| bmcs_cal | 8 [6-10] | 19 [16-22] | 34 [28-37] | 30 [27-32] | 0.27 / 0.36 / 0.43 | 0.64 / 0.73 / 0.72 | 0.53 / 0.41 / 0.35 |
| bmcs_cal_r | 10 [8-13] | 26 [18-28] | 44 [35-50] | 15 [12-18] | 0.46 / 0.63 / 0.68 | 0.64 / 0.70 / 0.71 | 0.53 / 0.35 / 0.32 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.83 | 2.88e-05 |
| bmcs_cal_r vs transfer | 0.70 | 0.008 |
| bmcs_cal_r vs bmcs_cal | 0.72 | 0.00611 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.70 | 0.0083 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 6 [3-7] | 14 [10-17] | 24 [21-29] | 37 [35-39] | 0.18 / 0.25 / 0.31 | 0.00 / 0.00 / 0.00 | 0.70 / 0.58 / 0.49 |
| transfer | 9 [7-10] | 21 [17-23] | 36 [30-41] | 26 [24-27] | 0.39 / 0.42 / 0.49 | 1.00 / 1.00 / 1.00 | 0.70 / 0.59 / 0.60 |
| bmcs_cal | 8 [6-10] | 19 [17-21] | 32 [28-38] | 29 [27-30] | 0.34 / 0.39 / 0.45 | 0.66 / 0.76 / 0.76 | 0.71 / 0.60 / 0.57 |
| bmcs_cal_r | 8 [7-11] | 25 [18-27] | 44 [36-48] | 18 [12-25] | 0.45 / 0.58 / 0.67 | 0.65 / 0.74 / 0.77 | 0.71 / 0.54 / 0.47 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.89 | 7.67e-07 |
| bmcs_cal_r vs transfer | 0.64 | 0.0598 |
| bmcs_cal_r vs bmcs_cal | 0.70 | 0.0177 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 8.66e-06 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 6 [3-7] | 12 [10-16] | 20 [17-24] | 40 [38-41] | 0.17 / 0.20 / 0.23 | 0.00 / 0.00 / 0.00 | 0.82 / 0.74 / 0.68 |
| transfer | 12 [10-15] | 23 [20-26] | 40 [38-43] | 22 [21-23] | 0.54 / 0.45 / 0.47 | 1.00 / 1.00 / 1.00 | 0.82 / 0.81 / 0.80 |
| bmcs_cal | 10 [8-13] | 21 [17-23] | 33 [29-42] | 25 [24-27] | 0.43 / 0.41 / 0.44 | 0.69 / 0.82 / 0.86 | 0.83 / 0.80 / 0.82 |
| bmcs_cal_r | 11 [6-13] | 25 [18-31] | 49 [37-54] | 15 [11-20] | 0.54 / 0.63 / 0.69 | 0.64 / 0.74 / 0.77 | 0.83 / 0.77 / 0.72 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.86 | 5.23e-06 |
| bmcs_cal_r vs transfer | 0.57 | 0.354 |
| bmcs_cal_r vs bmcs_cal | 0.64 | 0.13 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.95 | 2.29e-09 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 5 [3-7] | 11 [9-13] | 19 [15-21] | 42 [42-43] | 0.14 / 0.16 / 0.17 | 0.00 / 0.00 / 0.00 | 0.87 / 0.84 / 0.83 |
| transfer | 15 [12-19] | 29 [26-31] | 46 [41-48] | 16 [15-17] | 0.77 / 0.54 / 0.48 | 1.00 / 1.00 / 1.00 | 0.88 / 0.91 / 0.94 |
| bmcs_cal | 13 [9-16] | 25 [20-28] | 40 [34-44] | 21 [19-23] | 0.59 / 0.49 / 0.44 | 0.69 / 0.82 / 0.84 | 0.88 / 0.95 / 0.94 |
| bmcs_cal_r | 12 [8-14] | 26 [22-32] | 46 [40-53] | 13 [10-16] | 0.65 / 0.72 / 0.72 | 0.68 / 0.78 / 0.75 | 0.88 / 0.94 / 0.90 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.99 | 1.27e-10 |
| bmcs_cal_r vs transfer | 0.42 | 0.296 |
| bmcs_cal_r vs bmcs_cal | 0.61 | 0.285 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 1.00 | 2.74e-11 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [8.e-04 7.e-04 6.e-04 5.e-04 3.e-04 2.e-04 1.e-04 4.e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 19 [17-22] | 44 [41-50] | 80 [75-86] | 39 [36-43] | 0.17 / 0.25 / 0.29 | 0.00 / 0.00 / 0.00 | 0.26 / 0.14 / 0.10 |
| transfer | 23 [18-25] | 52 [45-55] | 85 [80-93] | 35 [31-38] | 0.24 / 0.31 / 0.33 | 1.00 / 1.00 / 1.00 | 0.26 / 0.19 / 0.15 |
| bmcs_cal | 21 [17-24] | 48 [44-53] | 85 [81-89] | 36 [34-39] | 0.22 / 0.28 / 0.31 | 0.60 / 0.67 / 0.67 | 0.26 / 0.16 / 0.13 |
| bmcs_cal_r | 23 [19-25] | 50 [45-56] | 92 [87-100] | 29 [24-32] | 0.26 / 0.34 / 0.38 | 0.60 / 0.65 / 0.65 | 0.26 / 0.24 / 0.24 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.69 | 0.0311 |
| bmcs_cal_r vs transfer | 0.48 | 0.818 |
| bmcs_cal_r vs bmcs_cal | 0.56 | 0.781 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.68 | 0.0164 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 18 [16-21] | 46 [40-49] | 80 [73-87] | 42 [39-46] | 0.18 / 0.25 / 0.28 | 0.00 / 0.00 / 0.00 | 0.38 / 0.24 / 0.18 |
| transfer | 22 [17-25] | 54 [49-57] | 91 [85-96] | 32 [30-34] | 0.26 / 0.30 / 0.33 | 1.00 / 1.00 / 1.00 | 0.38 / 0.37 / 0.30 |
| bmcs_cal | 20 [17-27] | 50 [45-55] | 84 [81-95] | 35 [32-38] | 0.25 / 0.29 / 0.32 | 0.66 / 0.74 / 0.72 | 0.37 / 0.29 / 0.24 |
| bmcs_cal_r | 24 [20-28] | 56 [49-65] | 98 [94-109] | 26 [22-33] | 0.32 / 0.39 / 0.42 | 0.63 / 0.68 / 0.69 | 0.37 / 0.36 / 0.38 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.85 | 9.03e-06 |
| bmcs_cal_r vs transfer | 0.61 | 0.126 |
| bmcs_cal_r vs bmcs_cal | 0.69 | 0.02 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.82 | 2.08e-05 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 19 [14-21] | 42 [38-50] | 76 [70-83] | 45 [42-47] | 0.18 / 0.23 / 0.24 | 0.00 / 0.00 / 0.00 | 0.52 / 0.37 / 0.30 |
| transfer | 26 [22-29] | 54 [51-58] | 92 [83-96] | 30 [28-32] | 0.32 / 0.29 / 0.32 | 1.00 / 1.00 / 1.00 | 0.52 / 0.67 / 0.71 |
| bmcs_cal | 21 [18-26] | 50 [46-57] | 89 [84-96] | 34 [32-36] | 0.28 / 0.29 / 0.31 | 0.69 / 0.81 / 0.80 | 0.51 / 0.52 / 0.52 |
| bmcs_cal_r | 22 [20-30] | 52 [44-64] | 95 [83-106] | 27 [18-30] | 0.32 / 0.38 / 0.38 | 0.63 / 0.69 / 0.70 | 0.51 / 0.57 / 0.60 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.78 | 0.000454 |
| bmcs_cal_r vs transfer | 0.50 | 0.959 |
| bmcs_cal_r vs bmcs_cal | 0.57 | 0.749 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 9.96e-06 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 18 [15-22] | 42 [36-45] | 70 [66-76] | 52 [50-53] | 0.15 / 0.17 / 0.17 | 0.00 / 0.00 / 0.00 | 0.68 / 0.61 / 0.58 |
| transfer | 30 [26-34] | 60 [57-65] | 98 [94-106] | 23 [21-26] | 0.47 / 0.33 / 0.31 | 1.00 / 1.00 / 1.00 | 0.68 / 0.81 / 0.94 |
| bmcs_cal | 28 [23-32] | 57 [50-64] | 93 [88-104] | 29 [26-32] | 0.40 / 0.32 / 0.30 | 0.73 / 0.89 / 0.93 | 0.68 / 0.71 / 0.86 |
| bmcs_cal_r | 26 [20-32] | 56 [52-63] | 102 [93-109] | 21 [15-24] | 0.44 / 0.48 / 0.47 | 0.66 / 0.75 / 0.76 | 0.68 / 0.72 / 0.76 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.93 | 2.39e-08 |
| bmcs_cal_r vs transfer | 0.41 | 0.467 |
| bmcs_cal_r vs bmcs_cal | 0.53 | 0.684 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.94 | 4.06e-09 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [3.e-04 7.e-04 6.e-04 8.e-04 5.e-04 2.e-04 1.e-04 4.e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 20 [17-24] | 48 [40-58] | 85 [76-91] | 39 [36-41] | 0.21 / 0.28 / 0.31 | 0.00 / 0.00 / 0.00 | 0.26 / 0.15 / 0.11 |
| transfer | 20 [16-23] | 50 [43-56] | 86 [81-90] | 34 [32-37] | 0.22 / 0.29 / 0.32 | 1.00 / 1.00 / 1.00 | 0.26 / 0.18 / 0.14 |
| bmcs_cal | 21 [18-23] | 48 [41-55] | 87 [76-94] | 37 [35-40] | 0.22 / 0.25 / 0.30 | 0.57 / 0.62 / 0.62 | 0.26 / 0.16 / 0.12 |
| bmcs_cal_r | 22 [18-27] | 56 [43-62] | 93 [81-104] | 27 [21-35] | 0.30 / 0.37 / 0.40 | 0.55 / 0.58 / 0.60 | 0.26 / 0.26 / 0.24 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.65 | 0.0823 |
| bmcs_cal_r vs transfer | 0.59 | 0.214 |
| bmcs_cal_r vs bmcs_cal | 0.67 | 0.0735 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.56 | 0.455 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 240.0 [40.2-240.0], never: 18/30
- transfer: 240.0 [29.6-240.0], never: 16/30
- bmcs_cal: 240.0 [92.2-240.0], never: 19/30
- bmcs_cal_r: 15.2 [2.5-196.3], never: 7/30

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 21 [18-24] | 48 [42-54] | 82 [76-91] | 40 [37-42] | 0.20 / 0.26 / 0.29 | 0.00 / 0.00 / 0.00 | 0.38 / 0.25 / 0.19 |
| transfer | 22 [18-25] | 50 [47-54] | 85 [81-92] | 35 [32-37] | 0.22 / 0.28 / 0.32 | 1.00 / 1.00 / 1.00 | 0.39 / 0.34 / 0.29 |
| bmcs_cal | 19 [17-23] | 46 [40-52] | 83 [74-92] | 38 [35-40] | 0.19 / 0.24 / 0.28 | 0.61 / 0.67 / 0.65 | 0.39 / 0.31 / 0.23 |
| bmcs_cal_r | 24 [18-26] | 49 [44-56] | 87 [83-97] | 31 [22-34] | 0.25 / 0.33 / 0.36 | 0.55 / 0.61 / 0.62 | 0.39 / 0.41 / 0.40 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.54 | 0.983 |
| bmcs_cal_r vs transfer | 0.45 | 0.983 |
| bmcs_cal_r vs bmcs_cal | 0.60 | 0.534 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.61 | 0.153 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 240.0 [39.1-240.0], never: 18/30
- transfer: 240.0 [39.4-240.0], never: 20/30
- bmcs_cal: 240.0 [142.4-240.0], never: 22/30
- bmcs_cal_r: 32.4 [8.1-240.0], never: 11/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 18 [13-22] | 41 [38-52] | 82 [69-88] | 45 [41-47] | 0.18 / 0.24 / 0.25 | 0.00 / 0.00 / 0.00 | 0.51 / 0.41 / 0.38 |
| transfer | 24 [20-30] | 54 [47-60] | 86 [79-101] | 34 [31-37] | 0.23 / 0.25 / 0.26 | 1.00 / 1.00 / 1.00 | 0.51 / 0.65 / 0.65 |
| bmcs_cal | 19 [17-24] | 46 [42-50] | 80 [75-88] | 40 [37-42] | 0.19 / 0.22 / 0.25 | 0.61 / 0.71 / 0.72 | 0.51 / 0.50 / 0.51 |
| bmcs_cal_r | 22 [20-25] | 54 [50-58] | 92 [85-100] | 29 [22-34] | 0.24 / 0.31 / 0.34 | 0.55 / 0.60 / 0.61 | 0.51 / 0.61 / 0.63 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.77 | 0.000837 |
| bmcs_cal_r vs transfer | 0.49 | 0.929 |
| bmcs_cal_r vs bmcs_cal | 0.72 | 0.00601 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.78 | 0.000204 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 240.0 [113.0-240.0], never: 22/30
- transfer: 240.0 [240.0-240.0], never: 24/30
- bmcs_cal: 240.0 [240.0-240.0], never: 26/30
- bmcs_cal_r: 66.0 [9.9-240.0], never: 14/30

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 18 [16-21] | 42 [37-46] | 66 [63-78] | 51 [49-52] | 0.17 / 0.17 / 0.18 | 0.00 / 0.00 / 0.00 | 0.65 / 0.61 / 0.64 |
| transfer | 23 [21-25] | 52 [50-56] | 88 [82-92] | 34 [34-36] | 0.17 / 0.23 / 0.21 | 1.00 / 1.00 / 1.00 | 0.65 / 0.84 / 0.91 |
| bmcs_cal | 21 [17-25] | 50 [42-54] | 81 [74-87] | 43 [39-47] | 0.15 / 0.19 / 0.20 | 0.59 / 0.72 / 0.77 | 0.65 / 0.69 / 0.83 |
| bmcs_cal_r | 22 [19-25] | 52 [46-58] | 96 [85-104] | 30 [25-34] | 0.22 / 0.32 / 0.34 | 0.56 / 0.61 / 0.63 | 0.65 / 0.76 / 0.89 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.78 | 0.000724 |
| bmcs_cal_r vs transfer | 0.48 | 0.841 |
| bmcs_cal_r vs bmcs_cal | 0.61 | 0.255 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.86 | 1.8e-06 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 240.0 [240.0-240.0], never: 29/30
- transfer: 240.0 [240.0-240.0], never: 29/30
- bmcs_cal: 240.0 [240.0-240.0], never: 30/30
- bmcs_cal_r: 240.0 [12.8-240.0], never: 16/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [8.e-04 7.e-04 6.e-04 3.e-04 3.e-04 2.e-04 1.e-04 4.e-05]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 19 [16-23] | 49 [45-56] | 108 [101-117] | 73 [65-79] | 0.20 / 0.21 / 0.35 | 0.00 / 0.00 / 0.00 | 0.27 / 0.15 / 0.10 |
| transfer | 20 [16-25] | 51 [46-57] | 114 [102-124] | 67 [64-75] | 0.22 / 0.21 / 0.35 | 1.00 / 1.00 / 1.00 | 0.27 / 0.19 / 0.14 |
| bmcs_cal | 19 [16-21] | 48 [43-55] | 108 [98-116] | 70 [64-74] | 0.22 / 0.20 / 0.36 | 0.62 / 0.67 / 0.67 | 0.26 / 0.17 / 0.13 |
| bmcs_cal_r | 22 [17-26] | 55 [50-59] | 118 [107-126] | 64 [55-71] | 0.26 / 0.21 / 0.36 | 0.60 / 0.63 / 0.66 | 0.26 / 0.23 / 0.22 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.69 | 0.0334 |
| bmcs_cal_r vs transfer | 0.63 | 0.0769 |
| bmcs_cal_r vs bmcs_cal | 0.68 | 0.0334 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.56 | 0.399 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 20 [16-23] | 50 [46-53] | 108 [98-116] | 76 [67-82] | 0.17 / 0.19 / 0.34 | 0.00 / 0.00 / 0.00 | 0.39 / 0.24 / 0.16 |
| transfer | 21 [18-26] | 54 [47-59] | 114 [98-122] | 68 [63-71] | 0.28 / 0.22 / 0.33 | 1.00 / 1.00 / 1.00 | 0.38 / 0.36 / 0.29 |
| bmcs_cal | 20 [17-23] | 52 [47-55] | 114 [98-127] | 68 [62-74] | 0.24 / 0.20 / 0.36 | 0.68 / 0.77 / 0.75 | 0.39 / 0.30 / 0.24 |
| bmcs_cal_r | 23 [19-28] | 58 [52-64] | 115 [107-129] | 66 [57-76] | 0.34 / 0.19 / 0.26 | 0.63 / 0.70 / 0.71 | 0.39 / 0.38 / 0.37 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.80 | 0.000233 |
| bmcs_cal_r vs transfer | 0.64 | 0.0581 |
| bmcs_cal_r vs bmcs_cal | 0.71 | 0.00961 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.64 | 0.0591 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 20 [17-24] | 46 [41-54] | 98 [92-110] | 79 [77-86] | 0.17 / 0.17 / 0.29 | 0.00 / 0.00 / 0.00 | 0.52 / 0.38 / 0.31 |
| transfer | 26 [22-30] | 58 [53-66] | 113 [103-123] | 69 [66-74] | 0.33 / 0.19 / 0.26 | 1.00 / 1.00 / 1.00 | 0.52 / 0.66 / 0.65 |
| bmcs_cal | 24 [21-27] | 55 [50-62] | 112 [101-121] | 74 [69-78] | 0.28 / 0.20 / 0.26 | 0.67 / 0.81 / 0.81 | 0.52 / 0.53 / 0.51 |
| bmcs_cal_r | 26 [22-29] | 62 [54-65] | 120 [110-126] | 64 [58-70] | 0.37 / 0.20 / 0.30 | 0.70 / 0.78 / 0.79 | 0.52 / 0.59 / 0.58 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.87 | 1.98e-06 |
| bmcs_cal_r vs transfer | 0.58 | 0.297 |
| bmcs_cal_r vs bmcs_cal | 0.67 | 0.0527 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 4.11e-05 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 19 [17-23] | 46 [39-52] | 90 [82-96] | 93 [90-95] | 0.17 / 0.16 / 0.21 | 0.00 / 0.00 / 0.00 | 0.63 / 0.53 / 0.54 |
| transfer | 30 [25-33] | 63 [59-70] | 118 [110-127] | 65 [63-68] | 0.43 / 0.22 / 0.22 | 1.00 / 1.00 / 1.00 | 0.63 / 0.83 / 0.90 |
| bmcs_cal | 24 [20-28] | 54 [49-62] | 102 [96-118] | 72 [69-75] | 0.35 / 0.21 / 0.22 | 0.70 / 0.85 / 0.91 | 0.63 / 0.72 / 0.88 |
| bmcs_cal_r | 24 [20-32] | 59 [52-68] | 118 [109-130] | 63 [54-70] | 0.41 / 0.19 / 0.26 | 0.74 / 0.82 / 0.84 | 0.63 / 0.75 / 0.82 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.88 | 1.33e-06 |
| bmcs_cal_r vs transfer | 0.33 | 0.0419 |
| bmcs_cal_r vs bmcs_cal | 0.63 | 0.0808 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.98 | 2.37e-10 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [8.e-04 7.e-04 6.e-04 5.e-04 3.e-04 2.e-04 1.e-04 4.e-05]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 17 [15-22] | 44 [37-47] | 72 [67-79] | 23 [20-25] | 0.15 / 0.20 / 0.26 | 0.00 / 0.00 / 0.00 | 0.26 / 0.15 / 0.11 |
| transfer | 21 [17-24] | 47 [41-52] | 79 [69-84] | 20 [18-24] | 0.16 / 0.15 / 0.23 | 1.00 / 1.00 / 1.00 | 0.26 / 0.18 / 0.14 |
| bmcs_cal | 20 [17-23] | 46 [40-51] | 75 [70-83] | 22 [20-25] | 0.16 / 0.19 / 0.24 | 0.61 / 0.66 / 0.65 | 0.26 / 0.16 / 0.12 |
| bmcs_cal_r | 20 [16-23] | 46 [41-51] | 80 [73-83] | 19 [14-21] | 0.17 / 0.22 / 0.26 | 0.60 / 0.64 / 0.65 | 0.26 / 0.23 / 0.23 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.62 | 0.339 |
| bmcs_cal_r vs transfer | 0.47 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.54 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.0481 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 19 [16-21] | 40 [37-45] | 70 [64-75] | 26 [24-27] | 0.14 / 0.15 / 0.20 | 0.00 / 0.00 / 0.00 | 0.38 / 0.23 / 0.18 |
| transfer | 21 [19-24] | 46 [41-52] | 74 [69-83] | 20 [18-23] | 0.20 / 0.23 / 0.26 | 1.00 / 1.00 / 1.00 | 0.37 / 0.35 / 0.31 |
| bmcs_cal | 20 [16-20] | 42 [39-46] | 72 [69-78] | 24 [19-25] | 0.17 / 0.21 / 0.26 | 0.64 / 0.73 / 0.71 | 0.37 / 0.31 / 0.25 |
| bmcs_cal_r | 21 [18-23] | 47 [41-49] | 78 [69-83] | 18 [14-22] | 0.16 / 0.23 / 0.28 | 0.60 / 0.66 / 0.68 | 0.37 / 0.37 / 0.37 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.67 | 0.0623 |
| bmcs_cal_r vs transfer | 0.48 | 0.795 |
| bmcs_cal_r vs bmcs_cal | 0.67 | 0.0623 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.68 | 0.0142 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 17 [13-21] | 38 [36-42] | 68 [62-73] | 28 [26-29] | 0.14 / 0.18 / 0.20 | 0.00 / 0.00 / 0.00 | 0.50 / 0.39 / 0.33 |
| transfer | 24 [20-25] | 50 [46-54] | 80 [74-86] | 17 [16-19] | 0.23 / 0.22 / 0.25 | 1.00 / 1.00 / 1.00 | 0.51 / 0.65 / 0.66 |
| bmcs_cal | 21 [18-22] | 44 [41-48] | 74 [68-80] | 21 [19-23] | 0.20 / 0.20 / 0.24 | 0.67 / 0.76 / 0.75 | 0.50 / 0.53 / 0.51 |
| bmcs_cal_r | 22 [19-26] | 47 [42-52] | 78 [74-85] | 18 [12-22] | 0.19 / 0.20 / 0.25 | 0.62 / 0.71 / 0.72 | 0.50 / 0.57 / 0.61 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.82 | 5.83e-05 |
| bmcs_cal_r vs transfer | 0.42 | 0.314 |
| bmcs_cal_r vs bmcs_cal | 0.61 | 0.314 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.90 | 9.1e-08 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 18 [14-23] | 38 [34-48] | 67 [56-72] | 32 [31-33] | 0.16 / 0.16 / 0.16 | 0.00 / 0.00 / 0.00 | 0.66 / 0.58 / 0.56 |
| transfer | 25 [24-29] | 53 [50-57] | 83 [78-90] | 13 [12-16] | 0.28 / 0.27 / 0.26 | 1.00 / 1.00 / 1.00 | 0.66 / 0.81 / 0.93 |
| bmcs_cal | 20 [17-24] | 44 [40-50] | 72 [65-78] | 19 [17-21] | 0.23 / 0.24 / 0.23 | 0.67 / 0.82 / 0.86 | 0.66 / 0.73 / 0.84 |
| bmcs_cal_r | 22 [18-25] | 46 [42-52] | 82 [73-89] | 13 [11-18] | 0.19 / 0.28 / 0.35 | 0.62 / 0.71 / 0.74 | 0.66 / 0.73 / 0.80 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.73 | 0.00496 |
| bmcs_cal_r vs transfer | 0.26 | 0.00496 |
| bmcs_cal_r vs bmcs_cal | 0.58 | 0.31 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.90 | 8.43e-08 |
