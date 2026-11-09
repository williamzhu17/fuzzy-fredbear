# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 0.5.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [5.0e-03 2.5e-03 1.5e-03 1.0e-03 5.0e-04 2.5e-04 1.0e-04 5.0e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 148 [135-157] | 368 [352-387] | 654 [637-678] | 99 [86-109] | 0.69 / 0.86 / 0.89 | 0.00 / 0.00 / 0.00 | 0.80 / 0.03 / 0.09 |
| calib | 182 [168-196] | 416 [400-430] | 700 [676-719] | 64 [57-80] | 0.87 / 0.91 / 0.87 | 0.00 / 0.00 / 0.00 | 0.80 / 0.04 / 0.17 |
| transfer | 201 [187-213] | 438 [430-459] | 739 [726-761] | 27 [25-32] | 0.98 / 0.94 / 0.91 | 1.00 / 1.00 / 1.00 | 0.73 / 0.03 / 0.41 |
| mix50_cal | 198 [182-204] | 428 [409-441] | 706 [691-724] | 51 [45-57] | 0.95 / 0.91 / 0.88 | 0.51 / 0.51 / 0.50 | 0.77 / 0.04 / 0.12 |
| bmcs_cal | 198 [186-205] | 428 [415-444] | 724 [700-740] | 39 [35-40] | 0.96 / 0.92 / 0.90 | 0.82 / 0.91 / 0.97 | 0.79 / 0.04 / 0.31 |
| bmcs_cf | 192 [184-198] | 420 [409-432] | 710 [694-729] | 44 [40-50] | 0.93 / 0.92 / 0.91 | 0.95 / 0.98 / 0.97 | 0.76 / 0.04 / 0.24 |
| bmcs_cal_r | 193 [183-208] | 434 [417-452] | 734 [719-754] | 22 [17-26] | 0.94 / 0.97 / 0.97 | 0.93 / 0.94 / 0.91 | 0.79 / 0.03 / 0.33 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.99 | 6.22e-10 |
| bmcs_cal vs calib | 0.64 | 0.25 |
| bmcs_cal vs transfer | 0.34 | 0.149 |
| bmcs_cal vs mix50_cal | 0.54 | 1 |
| bmcs_cal vs bmcs_cf | 0.61 | 0.454 |
| bmcs_cal vs bmcs_cal_r | 0.45 | 1 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.99 | 3.27e-10 |
| bmcs_cf vs calib | 0.54 | 0.567 |
| bmcs_cf vs transfer | 0.18 | 0.000133 |
| bmcs_cf vs mix50_cal | 0.42 | 0.567 |
| bmcs_cf vs bmcs_cal | 0.39 | 0.454 |
| bmcs_cf vs bmcs_cal_r | 0.32 | 0.0703 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 3.81e-05 |
| transfer vs fresh | 1.00 | 6.65e-11 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [5.00000e-03 9.22759e-04 3.63306e-03 5.43643e-04 4.17042e-04 2.37157e-04
 5.95342e-05 1.91934e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 150 [139-165] | 379 [354-390] | 676 [640-688] | 91 [83-105] | 0.63 / 0.79 / 0.82 | 0.00 / 0.00 / 0.00 | 0.82 / 0.07 / 0.13 |
| calib | 179 [168-192] | 404 [392-422] | 682 [656-708] | 64 [53-79] | 0.81 / 0.84 / 0.82 | 0.00 / 0.00 / 0.00 | 0.82 / 0.10 / 0.20 |
| transfer | 198 [191-214] | 440 [428-458] | 736 [720-760] | 23 [21-28] | 0.99 / 0.95 / 0.92 | 1.00 / 1.00 / 1.00 | 0.74 / 0.02 / 0.38 |
| mix50_cal | 198 [184-206] | 426 [408-441] | 716 [701-724] | 45 [42-50] | 0.96 / 0.91 / 0.88 | 0.50 / 0.50 / 0.50 | 0.79 / 0.02 / 0.11 |
| bmcs_cal | 202 [188-211] | 443 [427-456] | 730 [717-749] | 31 [25-38] | 0.98 / 0.94 / 0.91 | 0.82 / 0.89 / 0.96 | 0.78 / 0.02 / 0.27 |
| bmcs_cf | 196 [188-206] | 428 [412-450] | 730 [710-746] | 39 [35-43] | 0.94 / 0.93 / 0.91 | 0.95 / 0.98 / 0.96 | 0.79 / 0.02 / 0.21 |
| bmcs_cal_r | 196 [184-200] | 425 [414-444] | 740 [718-760] | 18 [17-24] | 0.95 / 0.97 / 0.96 | 0.93 / 0.94 / 0.90 | 0.78 / 0.03 / 0.30 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.96 | 4.41e-09 |
| bmcs_cal vs calib | 0.80 | 0.000337 |
| bmcs_cal vs transfer | 0.51 | 0.923 |
| bmcs_cal vs mix50_cal | 0.67 | 0.0826 |
| bmcs_cal vs bmcs_cf | 0.61 | 0.29 |
| bmcs_cal vs bmcs_cal_r | 0.63 | 0.224 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.93 | 4.44e-08 |
| bmcs_cf vs calib | 0.74 | 0.00818 |
| bmcs_cf vs transfer | 0.39 | 0.581 |
| bmcs_cf vs mix50_cal | 0.57 | 0.766 |
| bmcs_cf vs bmcs_cal | 0.39 | 0.581 |
| bmcs_cf vs bmcs_cal_r | 0.53 | 0.766 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.82 | 1.92e-05 |
| transfer vs fresh | 0.97 | 7.59e-10 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.0e-04 2.5e-03 1.5e-03 1.0e-03 5.0e-04 2.5e-04 5.0e-03 5.0e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 160 [147-166] | 375 [366-394] | 669 [657-694] | 86 [76-95] | 0.75 / 0.89 / 0.91 | 0.00 / 0.00 / 0.00 | 0.81 / 0.53 / 0.90 |
| calib | 182 [170-197] | 402 [390-428] | 698 [673-714] | 69 [56-74] | 0.89 / 0.91 / 0.88 | 0.00 / 0.00 / 0.00 | 0.81 / 0.70 / 0.92 |
| transfer | 66 [60-76] | 189 [170-198] | 376 [348-402] | 398 [344-423] | 0.00 / 0.13 / 0.31 | 1.00 / 1.00 / 1.00 | 0.81 / 0.63 / 0.73 |
| mix50_cal | 140 [108-160] | 357 [311-381] | 632 [569-657] | 127 [107-175] | 0.57 / 0.79 / 0.78 | 0.49 / 0.49 / 0.50 | 0.81 / 0.15 / 0.19 |
| bmcs_cal | 167 [158-181] | 402 [382-410] | 674 [658-702] | 78 [68-90] | 0.84 / 0.90 / 0.86 | 0.02 / 0.01 / 0.04 | 0.81 / 0.62 / 0.86 |
| bmcs_cf | 154 [145-165] | 378 [366-398] | 676 [662-698] | 94 [84-104] | 0.71 / 0.88 / 0.90 | 0.03 / 0.01 / 0.02 | 0.81 / 0.51 / 0.86 |
| bmcs_cal_r | 176 [162-185] | 408 [397-426] | 721 [693-736] | 46 [40-62] | 0.81 / 0.94 / 0.94 | 0.02 / 0.00 / 0.04 | 0.81 / 0.62 / 0.91 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.72 | 0.013 |
| bmcs_cal vs calib | 0.40 | 0.178 |
| bmcs_cal vs transfer | 1.00 | 1.7e-10 |
| bmcs_cal vs mix50_cal | 0.82 | 8.41e-05 |
| bmcs_cal vs bmcs_cf | 0.68 | 0.0413 |
| bmcs_cal vs bmcs_cal_r | 0.36 | 0.123 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.53 | 0.717 |
| bmcs_cf vs calib | 0.20 | 0.000325 |
| bmcs_cf vs transfer | 1.00 | 1.71e-10 |
| bmcs_cf vs mix50_cal | 0.70 | 0.0223 |
| bmcs_cf vs bmcs_cal | 0.32 | 0.0275 |
| bmcs_cf vs bmcs_cal_r | 0.22 | 0.000848 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.00 | 5.67e-11 |
| transfer vs fresh | 0.00 | 5.67e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 2.5 [1.9-3.2], never: 0/30
- calib: 2.0 [1.6-2.5], never: 0/30
- transfer: 120.3 [51.8-240.0], never: 13/30
- mix50_cal: 5.6 [2.9-8.9], never: 0/30
- bmcs_cal: 2.5 [1.6-3.4], never: 0/30
- bmcs_cf: 2.6 [2.3-3.3], never: 0/30
- bmcs_cal_r: 2.0 [1.7-3.4], never: 0/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.e-03 5.e-04 3.e-04 2.e-04 1.e-04 5.e-05 2.e-05 1.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 16 [12-23] | 50 [42-61] | 98 [81-114] | 53 [47-61] | 0.33 / 0.56 / 0.66 | 0.00 / 0.00 / 0.00 | 0.82 / 0.73 / 0.73 |
| calib | 17 [14-19] | 39 [34-49] | 78 [67-86] | 79 [74-84] | 0.24 / 0.35 / 0.43 | 0.00 / 0.00 / 0.00 | 0.82 / 0.61 / 0.46 |
| transfer | 30 [26-35] | 64 [58-70] | 109 [104-116] | 41 [39-43] | 0.61 / 0.58 / 0.62 | 1.00 / 1.00 / 1.00 | 0.81 / 0.84 / 0.84 |
| mix50_cal | 21 [18-27] | 49 [45-54] | 88 [80-99] | 62 [58-66] | 0.43 / 0.46 / 0.52 | 0.50 / 0.51 / 0.50 | 0.83 / 0.72 / 0.61 |
| bmcs_cal | 26 [21-30] | 61 [54-68] | 103 [95-113] | 48 [42-51] | 0.53 / 0.56 / 0.60 | 0.77 / 0.91 / 0.91 | 0.81 / 0.80 / 0.84 |
| bmcs_cf | 29 [22-31] | 60 [55-68] | 106 [98-112] | 45 [41-48] | 0.56 / 0.58 / 0.63 | 0.80 / 0.90 / 0.88 | 0.81 / 0.81 / 0.85 |
| bmcs_cal_r | 34 [28-39] | 78 [68-90] | 134 [119-145] | 20 [15-25] | 0.74 / 0.84 / 0.84 | 0.79 / 0.84 / 0.82 | 0.81 / 0.73 / 0.70 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.70 | 0.0208 |
| bmcs_cal vs calib | 0.92 | 1.24e-07 |
| bmcs_cal vs transfer | 0.40 | 0.338 |
| bmcs_cal vs mix50_cal | 0.75 | 0.00305 |
| bmcs_cal vs bmcs_cf | 0.49 | 0.894 |
| bmcs_cal vs bmcs_cal_r | 0.14 | 6.87e-06 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.72 | 0.0102 |
| bmcs_cf vs calib | 0.94 | 3.84e-08 |
| bmcs_cf vs transfer | 0.40 | 0.406 |
| bmcs_cf vs mix50_cal | 0.78 | 0.000644 |
| bmcs_cf vs bmcs_cal | 0.51 | 0.894 |
| bmcs_cf vs bmcs_cal_r | 0.14 | 1.1e-05 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.98 | 4.43e-10 |
| transfer vs fresh | 0.78 | 0.000188 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00125 0.00075 0.0005  0.00025 0.0001 ]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 57 [53-64] | 136 [122-146] | 244 [219-254] | 69 [61-75] | 0.29 / 0.39 / 0.42 | 0.00 / 0.00 / 0.00 | 0.50 / 0.22 / 0.28 |
| calib | 55 [47-61] | 128 [120-138] | 231 [216-240] | 77 [70-87] | 0.30 / 0.36 / 0.38 | 0.00 / 0.00 / 0.00 | 0.51 / 0.25 / 0.18 |
| transfer | 70 [61-72] | 153 [142-160] | 260 [248-269] | 46 [41-50] | 0.49 / 0.49 / 0.49 | 1.00 / 1.00 / 1.00 | 0.51 / 0.43 / 0.60 |
| mix50_cal | 58 [52-66] | 131 [125-147] | 228 [217-247] | 67 [61-74] | 0.37 / 0.39 / 0.41 | 0.50 / 0.50 / 0.50 | 0.51 / 0.26 / 0.22 |
| bmcs_cal | 61 [54-70] | 138 [130-148] | 235 [222-250] | 62 [51-69] | 0.38 / 0.40 / 0.42 | 0.72 / 0.84 / 0.84 | 0.51 / 0.30 / 0.39 |
| bmcs_cf | 65 [58-73] | 146 [133-158] | 246 [234-262] | 54 [47-60] | 0.45 / 0.46 / 0.47 | 0.82 / 0.89 / 0.86 | 0.50 / 0.26 / 0.44 |
| bmcs_cal_r | 68 [65-72] | 148 [139-161] | 259 [242-272] | 48 [34-55] | 0.39 / 0.45 / 0.48 | 0.74 / 0.83 / 0.82 | 0.51 / 0.31 / 0.52 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.57 | 0.68 |
| bmcs_cal vs calib | 0.69 | 0.0514 |
| bmcs_cal vs transfer | 0.27 | 0.012 |
| bmcs_cal vs mix50_cal | 0.57 | 0.68 |
| bmcs_cal vs bmcs_cf | 0.39 | 0.389 |
| bmcs_cal vs bmcs_cal_r | 0.31 | 0.0514 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.69 | 0.0572 |
| bmcs_cf vs calib | 0.80 | 0.000334 |
| bmcs_cf vs transfer | 0.38 | 0.371 |
| bmcs_cf vs mix50_cal | 0.69 | 0.0572 |
| bmcs_cf vs bmcs_cal | 0.61 | 0.371 |
| bmcs_cf vs bmcs_cal_r | 0.42 | 0.371 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.91 | 1.29e-07 |
| transfer vs fresh | 0.80 | 7.57e-05 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.00075 0.00175 0.0015  0.002   0.00125 0.0005  0.00025 0.0001 ]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 60 [49-64] | 138 [126-154] | 240 [226-254] | 66 [56-74] | 0.30 / 0.40 / 0.44 | 0.00 / 0.00 / 0.00 | 0.51 / 0.30 / 0.37 |
| calib | 52 [47-62] | 125 [116-137] | 230 [214-240] | 74 [68-80] | 0.33 / 0.38 / 0.40 | 0.00 / 0.00 / 0.00 | 0.52 / 0.31 / 0.27 |
| transfer | 68 [59-71] | 143 [134-155] | 252 [237-262] | 57 [54-68] | 0.31 / 0.34 / 0.36 | 1.00 / 1.00 / 1.00 | 0.50 / 0.42 / 0.56 |
| mix50_cal | 60 [52-67] | 137 [122-149] | 230 [220-248] | 72 [66-81] | 0.26 / 0.31 / 0.32 | 0.49 / 0.50 / 0.50 | 0.51 / 0.27 / 0.23 |
| bmcs_cal | 58 [54-64] | 136 [126-143] | 240 [220-248] | 70 [61-76] | 0.29 / 0.34 / 0.35 | 0.61 / 0.73 / 0.77 | 0.51 / 0.30 / 0.31 |
| bmcs_cf | 57 [51-68] | 136 [127-145] | 234 [219-241] | 72 [64-79] | 0.26 / 0.33 / 0.34 | 0.66 / 0.70 / 0.70 | 0.50 / 0.26 / 0.39 |
| bmcs_cal_r | 62 [55-66] | 143 [134-154] | 251 [236-262] | 51 [43-63] | 0.37 / 0.46 / 0.48 | 0.61 / 0.68 / 0.69 | 0.51 / 0.35 / 0.53 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.44 | 1 |
| bmcs_cal vs calib | 0.66 | 0.145 |
| bmcs_cal vs transfer | 0.30 | 0.0486 |
| bmcs_cal vs mix50_cal | 0.48 | 1 |
| bmcs_cal vs bmcs_cf | 0.49 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.32 | 0.0846 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.44 | 1 |
| bmcs_cf vs calib | 0.63 | 0.294 |
| bmcs_cf vs transfer | 0.32 | 0.0954 |
| bmcs_cf vs mix50_cal | 0.49 | 1 |
| bmcs_cf vs bmcs_cal | 0.51 | 1 |
| bmcs_cf vs bmcs_cal_r | 0.34 | 0.163 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.79 | 0.000172 |
| transfer vs fresh | 0.60 | 0.196 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 24.5 [7.4-91.0], never: 6/30
- calib: 17.3 [5.2-206.0], never: 8/30
- transfer: 43.6 [6.3-240.0], never: 12/30
- mix50_cal: 240.0 [7.6-240.0], never: 16/30
- bmcs_cal: 21.4 [4.7-240.0], never: 12/30
- bmcs_cf: 209.0 [12.6-240.0], never: 15/30
- bmcs_cal_r: 9.6 [4.2-102.8], never: 7/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00075 0.00075 0.0005  0.00025 0.0001 ]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 56 [49-62] | 140 [130-151] | 298 [279-314] | 158 [133-167] | 0.26 / 0.20 / 0.38 | 0.00 / 0.00 / 0.00 | 0.52 / 0.23 / 0.28 |
| calib | 56 [48-62] | 138 [128-144] | 284 [274-311] | 164 [150-179] | 0.28 / 0.20 / 0.37 | 0.00 / 0.00 / 0.00 | 0.50 / 0.22 / 0.19 |
| transfer | 71 [66-74] | 159 [148-168] | 302 [291-326] | 147 [134-157] | 0.46 / 0.22 / 0.29 | 1.00 / 1.00 / 1.00 | 0.52 / 0.42 / 0.55 |
| mix50_cal | 62 [58-68] | 146 [138-156] | 294 [282-315] | 151 [145-164] | 0.42 / 0.23 / 0.33 | 0.50 / 0.50 / 0.50 | 0.51 / 0.23 / 0.20 |
| bmcs_cal | 65 [61-72] | 152 [140-160] | 300 [284-318] | 152 [145-165] | 0.41 / 0.21 / 0.29 | 0.77 / 0.87 / 0.90 | 0.51 / 0.31 / 0.38 |
| bmcs_cf | 62 [58-69] | 150 [141-161] | 301 [284-314] | 147 [137-163] | 0.39 / 0.23 / 0.33 | 0.80 / 0.89 / 0.88 | 0.51 / 0.28 / 0.42 |
| bmcs_cal_r | 64 [59-70] | 152 [139-166] | 320 [283-334] | 144 [119-167] | 0.43 / 0.21 / 0.31 | 0.78 / 0.84 / 0.85 | 0.51 / 0.35 / 0.54 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.73 | 0.013 |
| bmcs_cal vs calib | 0.77 | 0.00195 |
| bmcs_cal vs transfer | 0.39 | 0.51 |
| bmcs_cal vs mix50_cal | 0.59 | 0.71 |
| bmcs_cal vs bmcs_cf | 0.53 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.47 | 1 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.70 | 0.0363 |
| bmcs_cf vs calib | 0.74 | 0.00906 |
| bmcs_cf vs transfer | 0.35 | 0.187 |
| bmcs_cf vs mix50_cal | 0.55 | 1 |
| bmcs_cf vs bmcs_cal | 0.47 | 1 |
| bmcs_cf vs bmcs_cal_r | 0.46 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.85 | 7.88e-06 |
| transfer vs fresh | 0.81 | 3.14e-05 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00125 0.00075 0.0005  0.00025 0.0001 ]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 48 [40-53] | 110 [104-116] | 182 [177-190] | 37 [29-41] | 0.18 / 0.26 / 0.25 | 0.00 / 0.00 / 0.00 | 0.49 / 0.25 / 0.36 |
| calib | 49 [47-54] | 106 [98-116] | 174 [162-184] | 42 [37-49] | 0.17 / 0.26 / 0.23 | 0.00 / 0.00 / 0.00 | 0.49 / 0.26 / 0.22 |
| transfer | 58 [53-66] | 122 [107-134] | 191 [180-212] | 22 [19-29] | 0.31 / 0.35 / 0.32 | 1.00 / 1.00 / 1.00 | 0.49 / 0.46 / 0.59 |
| mix50_cal | 52 [47-57] | 112 [103-120] | 180 [171-201] | 37 [28-40] | 0.23 / 0.29 / 0.27 | 0.51 / 0.50 / 0.50 | 0.49 / 0.29 / 0.27 |
| bmcs_cal | 56 [51-63] | 116 [108-122] | 187 [178-196] | 32 [26-35] | 0.25 / 0.31 / 0.27 | 0.78 / 0.88 / 0.86 | 0.50 / 0.34 / 0.44 |
| bmcs_cf | 55 [49-57] | 113 [108-124] | 186 [177-198] | 31 [25-35] | 0.27 / 0.33 / 0.29 | 0.76 / 0.85 / 0.81 | 0.50 / 0.32 / 0.48 |
| bmcs_cal_r | 55 [50-59] | 118 [111-125] | 193 [182-200] | 27 [21-36] | 0.23 / 0.32 / 0.25 | 0.71 / 0.77 / 0.75 | 0.50 / 0.37 / 0.53 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.66 | 0.182 |
| bmcs_cal vs calib | 0.69 | 0.0794 |
| bmcs_cal vs transfer | 0.41 | 0.782 |
| bmcs_cal vs mix50_cal | 0.60 | 0.782 |
| bmcs_cal vs bmcs_cf | 0.53 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.46 | 1 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.64 | 0.332 |
| bmcs_cf vs calib | 0.67 | 0.139 |
| bmcs_cf vs transfer | 0.38 | 0.421 |
| bmcs_cf vs mix50_cal | 0.58 | 0.86 |
| bmcs_cf vs bmcs_cal | 0.47 | 0.86 |
| bmcs_cf vs bmcs_cal_r | 0.42 | 0.86 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00334 |
| transfer vs fresh | 0.71 | 0.0053 |
