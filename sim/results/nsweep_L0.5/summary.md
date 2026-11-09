# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 0.5.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [5.0e-03 2.5e-03 1.5e-03 1.0e-03 5.0e-04 2.5e-04 1.0e-04 5.0e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 166 [153-177] | 396 [378-405] | 684 [666-697] | 77 [71-89] | 0.80 / 0.89 / 0.90 | 0.00 / 0.00 / 0.00 | 0.50 / 0.04 / 0.04 |
| transfer | 176 [166-188] | 412 [388-417] | 706 [684-715] | 61 [57-76] | 0.82 / 0.89 / 0.91 | 1.00 / 1.00 / 1.00 | 0.48 / 0.12 / 0.10 |
| bmcs_cal | 178 [164-190] | 407 [381-423] | 700 [674-718] | 64 [57-73] | 0.83 / 0.90 / 0.91 | 0.86 / 0.88 / 0.84 | 0.47 / 0.10 / 0.08 |
| bmcs_cal_r | 182 [168-187] | 422 [400-435] | 720 [704-737] | 43 [29-54] | 0.87 / 0.93 / 0.94 | 0.83 / 0.83 / 0.81 | 0.47 / 0.17 / 0.23 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.78 | 0.000693 |
| bmcs_cal_r vs transfer | 0.65 | 0.0824 |
| bmcs_cal_r vs bmcs_cal | 0.65 | 0.0824 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.70 | 0.00759 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 173 [161-183] | 396 [375-409] | 688 [664-695] | 74 [68-89] | 0.81 / 0.88 / 0.88 | 0.00 / 0.00 / 0.00 | 0.67 / 0.06 / 0.06 |
| transfer | 188 [180-205] | 426 [411-434] | 719 [706-737] | 46 [40-49] | 0.91 / 0.91 / 0.91 | 1.00 / 1.00 / 1.00 | 0.62 / 0.17 / 0.28 |
| bmcs_cal | 187 [175-191] | 414 [394-429] | 710 [684-734] | 51 [47-63] | 0.89 / 0.90 / 0.90 | 0.86 / 0.92 / 0.91 | 0.62 / 0.12 / 0.20 |
| bmcs_cal_r | 191 [182-201] | 431 [421-447] | 730 [713-751] | 28 [20-37] | 0.91 / 0.95 / 0.95 | 0.89 / 0.90 / 0.88 | 0.62 / 0.11 / 0.37 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.87 | 2.64e-06 |
| bmcs_cal_r vs transfer | 0.60 | 0.201 |
| bmcs_cal_r vs bmcs_cal | 0.72 | 0.00823 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 9.47e-06 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 182 [168-196] | 416 [400-430] | 700 [676-719] | 64 [57-80] | 0.87 / 0.91 / 0.87 | 0.00 / 0.00 / 0.00 | 0.80 / 0.04 / 0.17 |
| transfer | 201 [187-213] | 438 [430-459] | 739 [726-761] | 27 [25-32] | 0.98 / 0.94 / 0.91 | 1.00 / 1.00 / 1.00 | 0.73 / 0.03 / 0.41 |
| bmcs_cal | 198 [186-205] | 428 [415-444] | 724 [700-740] | 39 [35-40] | 0.96 / 0.92 / 0.90 | 0.82 / 0.91 / 0.97 | 0.79 / 0.04 / 0.31 |
| bmcs_cal_r | 193 [183-208] | 434 [417-452] | 734 [719-754] | 22 [17-26] | 0.94 / 0.97 / 0.97 | 0.93 / 0.94 / 0.91 | 0.79 / 0.03 / 0.33 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.69 | 0.0389 |
| bmcs_cal_r vs transfer | 0.39 | 0.259 |
| bmcs_cal_r vs bmcs_cal | 0.55 | 0.51 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 3.81e-05 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 170 [159-184] | 414 [394-442] | 674 [651-694] | 79 [72-92] | 0.86 / 0.98 / 0.79 | 0.00 / 0.00 / 0.00 | 0.87 / 0.01 / 0.50 |
| transfer | 204 [195-210] | 440 [425-456] | 740 [723-763] | 25 [23-27] | 1.00 / 0.96 / 0.89 | 1.00 / 1.00 / 1.00 | 0.83 / 0.00 / 0.08 |
| bmcs_cal | 198 [191-205] | 438 [418-446] | 725 [696-744] | 31 [28-36] | 0.98 / 0.95 / 0.88 | 0.86 / 0.85 / 0.99 | 0.86 / 0.00 / 0.10 |
| bmcs_cal_r | 190 [174-200] | 430 [412-446] | 738 [722-768] | 15 [12-18] | 0.95 / 0.98 / 0.98 | 0.94 / 0.96 / 0.93 | 0.86 / 0.01 / 0.49 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.64 | 0.127 |
| bmcs_cal_r vs transfer | 0.35 | 0.122 |
| bmcs_cal_r vs bmcs_cal | 0.46 | 0.61 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.79 | 0.000114 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [5.00000e-03 9.22759e-04 3.63306e-03 5.43643e-04 4.17042e-04 2.37157e-04
 5.95342e-05 1.91934e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 159 [148-178] | 380 [360-410] | 672 [626-692] | 85 [70-121] | 0.66 / 0.77 / 0.80 | 0.00 / 0.00 / 0.00 | 0.49 / 0.07 / 0.05 |
| transfer | 182 [169-192] | 410 [371-422] | 701 [664-719] | 68 [52-75] | 0.79 / 0.84 / 0.85 | 1.00 / 1.00 / 1.00 | 0.46 / 0.12 / 0.10 |
| bmcs_cal | 176 [166-192] | 404 [390-418] | 686 [674-710] | 68 [55-79] | 0.79 / 0.85 / 0.86 | 0.84 / 0.85 / 0.82 | 0.47 / 0.10 / 0.07 |
| bmcs_cal_r | 181 [173-196] | 414 [402-427] | 716 [698-731] | 49 [29-61] | 0.82 / 0.89 / 0.90 | 0.83 / 0.82 / 0.80 | 0.47 / 0.16 / 0.22 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.77 | 0.00126 |
| bmcs_cal_r vs transfer | 0.60 | 0.181 |
| bmcs_cal_r vs bmcs_cal | 0.65 | 0.0984 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.0405 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 172 [157-192] | 407 [376-424] | 695 [646-710] | 71 [63-90] | 0.77 / 0.82 / 0.83 | 0.00 / 0.00 / 0.00 | 0.69 / 0.08 / 0.07 |
| transfer | 198 [189-206] | 428 [414-442] | 727 [704-737] | 40 [37-46] | 0.92 / 0.90 / 0.90 | 1.00 / 1.00 / 1.00 | 0.61 / 0.15 / 0.26 |
| bmcs_cal | 190 [182-197] | 422 [410-435] | 717 [689-734] | 45 [40-54] | 0.90 / 0.88 / 0.88 | 0.86 / 0.92 / 0.91 | 0.66 / 0.11 / 0.19 |
| bmcs_cal_r | 188 [178-196] | 421 [407-438] | 722 [698-754] | 33 [24-46] | 0.88 / 0.92 / 0.92 | 0.88 / 0.89 / 0.86 | 0.66 / 0.10 / 0.36 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.71 | 0.0152 |
| bmcs_cal_r vs transfer | 0.43 | 0.758 |
| bmcs_cal_r vs bmcs_cal | 0.51 | 0.871 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.77 | 0.000355 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 179 [168-192] | 404 [392-422] | 682 [656-708] | 64 [53-79] | 0.81 / 0.84 / 0.82 | 0.00 / 0.00 / 0.00 | 0.82 / 0.10 / 0.20 |
| transfer | 198 [191-214] | 440 [428-458] | 736 [720-760] | 23 [21-28] | 0.99 / 0.95 / 0.92 | 1.00 / 1.00 / 1.00 | 0.74 / 0.02 / 0.38 |
| bmcs_cal | 202 [188-211] | 443 [427-456] | 730 [717-749] | 31 [25-38] | 0.98 / 0.94 / 0.91 | 0.82 / 0.89 / 0.96 | 0.78 / 0.02 / 0.27 |
| bmcs_cal_r | 196 [184-200] | 425 [414-444] | 740 [718-760] | 18 [17-24] | 0.95 / 0.97 / 0.96 | 0.93 / 0.94 / 0.90 | 0.78 / 0.03 / 0.30 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.74 | 0.00342 |
| bmcs_cal_r vs transfer | 0.36 | 0.129 |
| bmcs_cal_r vs bmcs_cal | 0.37 | 0.129 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.82 | 1.92e-05 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 178 [151-184] | 417 [378-439] | 688 [651-716] | 79 [62-101] | 0.74 / 0.86 / 0.72 | 0.00 / 0.00 / 0.00 | 0.87 / 0.14 / 0.42 |
| transfer | 201 [196-208] | 444 [428-460] | 730 [723-758] | 21 [15-31] | 1.00 / 0.97 / 0.90 | 1.00 / 1.00 / 1.00 | 0.84 / 0.00 / 0.06 |
| bmcs_cal | 200 [190-204] | 431 [417-443] | 726 [706-746] | 26 [21-37] | 0.98 / 0.97 / 0.89 | 0.81 / 0.75 / 0.98 | 0.86 / 0.00 / 0.07 |
| bmcs_cal_r | 196 [185-204] | 438 [426-453] | 748 [728-770] | 13 [11-18] | 0.96 / 0.99 / 0.99 | 0.95 / 0.98 / 0.97 | 0.86 / 0.00 / 0.36 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.71 | 0.0136 |
| bmcs_cal_r vs transfer | 0.42 | 0.386 |
| bmcs_cal_r vs bmcs_cal | 0.60 | 0.386 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.78 | 0.000245 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.0e-04 2.5e-03 1.5e-03 1.0e-03 5.0e-04 2.5e-04 5.0e-03 5.0e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 161 [150-176] | 390 [370-407] | 679 [654-693] | 76 [70-86] | 0.79 / 0.88 / 0.90 | 0.00 / 0.00 / 0.00 | 0.53 / 0.17 / 0.16 |
| transfer | 150 [132-162] | 378 [358-385] | 662 [636-682] | 90 [80-117] | 0.70 / 0.86 / 0.88 | 1.00 / 1.00 / 1.00 | 0.51 / 0.08 / 0.07 |
| bmcs_cal | 158 [143-167] | 382 [359-395] | 668 [647-699] | 95 [79-104] | 0.72 / 0.85 / 0.87 | 0.25 / 0.28 / 0.31 | 0.52 / 0.08 / 0.07 |
| bmcs_cal_r | 172 [141-182] | 396 [370-421] | 703 [658-727] | 47 [37-82] | 0.74 / 0.89 / 0.90 | 0.30 / 0.33 / 0.37 | 0.52 / 0.25 / 0.33 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.55 | 0.544 |
| bmcs_cal_r vs transfer | 0.68 | 0.0551 |
| bmcs_cal_r vs bmcs_cal | 0.63 | 0.184 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.32 | 0.018 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 1.9 [1.4-2.7], never: 0/30
- transfer: 3.2 [2.3-5.5], never: 0/30
- bmcs_cal: 2.3 [1.4-3.3], never: 0/30
- bmcs_cal_r: 1.8 [1.2-3.2], never: 0/30

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 167 [150-176] | 388 [375-408] | 681 [664-704] | 70 [63-82] | 0.83 / 0.90 / 0.90 | 0.00 / 0.00 / 0.00 | 0.70 / 0.39 / 0.44 |
| transfer | 104 [87-130] | 308 [268-350] | 588 [530-630] | 174 [142-213] | 0.34 / 0.69 / 0.74 | 1.00 / 1.00 / 1.00 | 0.69 / 0.19 / 0.20 |
| bmcs_cal | 172 [158-188] | 396 [367-411] | 681 [652-705] | 79 [69-90] | 0.78 / 0.87 / 0.88 | 0.07 / 0.09 / 0.15 | 0.69 / 0.24 / 0.20 |
| bmcs_cal_r | 173 [155-189] | 404 [383-425] | 708 [670-729] | 54 [36-65] | 0.80 / 0.91 / 0.92 | 0.10 / 0.12 / 0.19 | 0.69 / 0.38 / 0.63 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.63 | 0.189 |
| bmcs_cal_r vs transfer | 0.90 | 2.83e-07 |
| bmcs_cal_r vs bmcs_cal | 0.61 | 0.189 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.10 | 1.36e-07 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 1.8 [1.4-2.9], never: 0/30
- transfer: 10.7 [6.0-17.6], never: 1/30
- bmcs_cal: 2.1 [1.4-2.7], never: 0/30
- bmcs_cal_r: 1.8 [1.5-3.0], never: 0/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 182 [170-197] | 402 [390-428] | 698 [673-714] | 69 [56-74] | 0.89 / 0.91 / 0.88 | 0.00 / 0.00 / 0.00 | 0.81 / 0.70 / 0.92 |
| transfer | 66 [60-76] | 189 [170-198] | 376 [348-402] | 398 [344-423] | 0.00 / 0.13 / 0.31 | 1.00 / 1.00 / 1.00 | 0.81 / 0.63 / 0.73 |
| bmcs_cal | 167 [158-181] | 402 [382-410] | 674 [658-702] | 78 [68-90] | 0.84 / 0.90 / 0.86 | 0.02 / 0.01 / 0.04 | 0.81 / 0.62 / 0.86 |
| bmcs_cal_r | 176 [162-185] | 408 [397-426] | 721 [693-736] | 46 [40-62] | 0.81 / 0.94 / 0.94 | 0.02 / 0.00 / 0.04 | 0.81 / 0.62 / 0.91 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.53 | 0.728 |
| bmcs_cal_r vs transfer | 1.00 | 8.56e-11 |
| bmcs_cal_r vs bmcs_cal | 0.64 | 0.123 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.00 | 2.83e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 2.0 [1.6-2.5], never: 0/30
- transfer: 120.3 [51.8-240.0], never: 13/30
- bmcs_cal: 2.5 [1.6-3.4], never: 0/30
- bmcs_cal_r: 2.0 [1.7-3.4], never: 0/30

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 170 [152-185] | 410 [391-421] | 683 [647-699] | 78 [67-101] | 0.82 / 0.97 / 0.79 | 0.00 / 0.00 / 0.00 | 0.87 / 0.99 / 0.99 |
| transfer | 52 [46-55] | 143 [132-157] | 261 [252-280] | 499 [494-506] | 0.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 | 0.89 / 0.51 / 0.93 |
| bmcs_cal | 167 [151-180] | 404 [392-426] | 672 [657-697] | 83 [75-92] | 0.83 / 0.98 / 0.80 | 0.02 / 0.00 / 0.00 | 0.88 / 0.99 / 0.99 |
| bmcs_cal_r | 151 [131-161] | 390 [370-403] | 690 [676-715] | 69 [58-89] | 0.68 / 0.90 / 0.90 | 0.02 / 0.00 / 0.00 | 0.88 / 0.99 / 0.99 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.27 | 0.00487 |
| bmcs_cal_r vs transfer | 1.00 | 1.04e-10 |
| bmcs_cal_r vs bmcs_cal | 0.30 | 0.0076 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.00 | 2.85e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 2.7 [2.1-4.4], never: 0/30
- transfer: 240.0 [240.0-240.0], never: 30/30
- bmcs_cal: 3.0 [2.4-3.4], never: 0/30
- bmcs_cal_r: 3.8 [2.9-4.7], never: 1/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.e-03 5.e-04 3.e-04 2.e-04 1.e-04 5.e-05 2.e-05 1.e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 17 [12-20] | 46 [39-58] | 84 [77-107] | 61 [53-68] | 0.29 / 0.52 / 0.61 | 0.00 / 0.00 / 0.00 | 0.54 / 0.26 / 0.16 |
| transfer | 26 [22-28] | 61 [53-67] | 106 [97-115] | 47 [42-50] | 0.45 / 0.60 / 0.67 | 1.00 / 1.00 / 1.00 | 0.52 / 0.34 / 0.28 |
| bmcs_cal | 22 [18-24] | 54 [48-58] | 99 [90-103] | 53 [50-57] | 0.39 / 0.54 / 0.62 | 0.71 / 0.77 / 0.75 | 0.53 / 0.33 / 0.25 |
| bmcs_cal_r | 27 [23-36] | 70 [64-77] | 127 [117-135] | 22 [19-30] | 0.62 / 0.79 / 0.83 | 0.70 / 0.76 / 0.76 | 0.53 / 0.34 / 0.33 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.91 | 1.39e-07 |
| bmcs_cal_r vs transfer | 0.75 | 0.000916 |
| bmcs_cal_r vs bmcs_cal | 0.91 | 1.4e-07 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.78 | 0.000187 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 17 [13-19] | 44 [37-54] | 81 [71-96] | 69 [63-73] | 0.28 / 0.44 / 0.54 | 0.00 / 0.00 / 0.00 | 0.70 / 0.41 / 0.27 |
| transfer | 29 [23-32] | 62 [57-70] | 109 [99-120] | 44 [41-46] | 0.50 / 0.59 / 0.66 | 1.00 / 1.00 / 1.00 | 0.69 / 0.60 / 0.54 |
| bmcs_cal | 22 [17-26] | 52 [48-57] | 98 [91-108] | 53 [48-56] | 0.44 / 0.53 / 0.62 | 0.76 / 0.85 / 0.82 | 0.70 / 0.56 / 0.48 |
| bmcs_cal_r | 28 [22-33] | 71 [65-77] | 126 [120-131] | 25 [18-35] | 0.60 / 0.78 / 0.80 | 0.71 / 0.79 / 0.78 | 0.70 / 0.53 / 0.49 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.93 | 2.98e-08 |
| bmcs_cal_r vs transfer | 0.67 | 0.021 |
| bmcs_cal_r vs bmcs_cal | 0.86 | 2.81e-06 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.87 | 1.01e-06 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 17 [14-19] | 39 [34-49] | 78 [67-86] | 79 [74-84] | 0.24 / 0.35 / 0.43 | 0.00 / 0.00 / 0.00 | 0.82 / 0.61 / 0.46 |
| transfer | 30 [26-35] | 64 [58-70] | 109 [104-116] | 41 [39-43] | 0.61 / 0.58 / 0.62 | 1.00 / 1.00 / 1.00 | 0.81 / 0.84 / 0.84 |
| bmcs_cal | 26 [21-30] | 61 [54-68] | 103 [95-113] | 48 [42-51] | 0.53 / 0.56 / 0.60 | 0.77 / 0.91 / 0.91 | 0.81 / 0.80 / 0.84 |
| bmcs_cal_r | 34 [28-39] | 78 [68-90] | 134 [119-145] | 20 [15-25] | 0.74 / 0.84 / 0.84 | 0.79 / 0.84 / 0.82 | 0.81 / 0.73 / 0.70 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 1.00 | 8.94e-11 |
| bmcs_cal_r vs transfer | 0.81 | 3.66e-05 |
| bmcs_cal_r vs bmcs_cal | 0.86 | 2.75e-06 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.98 | 2.21e-10 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 12 [10-16] | 31 [25-38] | 58 [48-60] | 98 [93-99] | 0.19 / 0.22 / 0.25 | 0.00 / 0.00 / 0.00 | 0.87 / 0.78 / 0.75 |
| transfer | 38 [32-40] | 75 [68-84] | 124 [113-127] | 31 [29-33] | 0.82 / 0.63 / 0.58 | 1.00 / 1.00 / 1.00 | 0.87 / 0.95 / 0.97 |
| bmcs_cal | 32 [29-38] | 70 [65-78] | 118 [108-122] | 39 [35-40] | 0.72 / 0.61 / 0.56 | 0.83 / 0.94 / 0.95 | 0.87 / 0.95 / 0.95 |
| bmcs_cal_r | 32 [29-37] | 80 [72-85] | 139 [130-151] | 11 [9-14] | 0.83 / 0.92 / 0.91 | 0.81 / 0.89 / 0.86 | 0.87 / 0.89 / 0.89 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 1.00 | 8.44e-11 |
| bmcs_cal_r vs transfer | 0.62 | 0.1 |
| bmcs_cal_r vs bmcs_cal | 0.72 | 0.00547 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 1.00 | 3.11e-11 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00125 0.00075 0.0005  0.00025 0.0001 ]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 62 [52-66] | 134 [122-146] | 234 [224-255] | 64 [57-74] | 0.32 / 0.41 / 0.43 | 0.00 / 0.00 / 0.00 | 0.25 / 0.09 / 0.06 |
| transfer | 60 [56-68] | 136 [131-154] | 245 [232-256] | 59 [54-69] | 0.34 / 0.43 / 0.46 | 1.00 / 1.00 / 1.00 | 0.25 / 0.12 / 0.09 |
| bmcs_cal | 62 [52-67] | 140 [128-145] | 235 [226-252] | 65 [59-73] | 0.32 / 0.38 / 0.42 | 0.66 / 0.72 / 0.69 | 0.26 / 0.10 / 0.07 |
| bmcs_cal_r | 64 [57-68] | 146 [139-152] | 254 [243-266] | 52 [42-59] | 0.38 / 0.45 / 0.48 | 0.67 / 0.70 / 0.68 | 0.26 / 0.16 / 0.17 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.71 | 0.0174 |
| bmcs_cal_r vs transfer | 0.61 | 0.149 |
| bmcs_cal_r vs bmcs_cal | 0.69 | 0.027 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.59 | 0.211 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 57 [52-64] | 133 [120-143] | 227 [209-242] | 73 [70-85] | 0.23 / 0.29 / 0.33 | 0.00 / 0.00 / 0.00 | 0.37 / 0.14 / 0.10 |
| transfer | 66 [60-70] | 146 [135-159] | 250 [240-264] | 52 [47-59] | 0.42 / 0.47 / 0.48 | 1.00 / 1.00 / 1.00 | 0.37 / 0.25 / 0.21 |
| bmcs_cal | 62 [56-66] | 139 [129-156] | 238 [222-254] | 62 [56-69] | 0.32 / 0.39 / 0.42 | 0.74 / 0.79 / 0.75 | 0.37 / 0.19 / 0.14 |
| bmcs_cal_r | 62 [58-75] | 146 [133-164] | 258 [237-280] | 53 [44-60] | 0.38 / 0.44 / 0.47 | 0.72 / 0.77 / 0.74 | 0.37 / 0.25 / 0.29 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.74 | 0.0036 |
| bmcs_cal_r vs transfer | 0.51 | 0.842 |
| bmcs_cal_r vs bmcs_cal | 0.62 | 0.22 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.77 | 0.000274 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 55 [47-61] | 128 [120-138] | 231 [216-240] | 77 [70-87] | 0.30 / 0.36 / 0.38 | 0.00 / 0.00 / 0.00 | 0.51 / 0.25 / 0.18 |
| transfer | 70 [61-72] | 153 [142-160] | 260 [248-269] | 46 [41-50] | 0.49 / 0.49 / 0.49 | 1.00 / 1.00 / 1.00 | 0.51 / 0.43 / 0.60 |
| bmcs_cal | 61 [54-70] | 138 [130-148] | 235 [222-250] | 62 [51-69] | 0.38 / 0.40 / 0.42 | 0.72 / 0.84 / 0.84 | 0.51 / 0.30 / 0.39 |
| bmcs_cal_r | 68 [65-72] | 148 [139-161] | 259 [242-272] | 48 [34-55] | 0.39 / 0.45 / 0.48 | 0.74 / 0.83 / 0.82 | 0.51 / 0.31 / 0.52 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.86 | 5.74e-06 |
| bmcs_cal_r vs transfer | 0.47 | 0.652 |
| bmcs_cal_r vs bmcs_cal | 0.69 | 0.0205 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.91 | 6.47e-08 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 56 [48-62] | 126 [114-136] | 214 [198-226] | 92 [87-100] | 0.25 / 0.29 / 0.28 | 0.00 / 0.00 / 0.00 | 0.68 / 0.42 / 0.43 |
| transfer | 72 [61-81] | 154 [143-169] | 258 [246-276] | 38 [32-47] | 0.61 / 0.47 / 0.44 | 1.00 / 1.00 / 1.00 | 0.67 / 0.36 / 0.84 |
| bmcs_cal | 72 [64-77] | 158 [146-168] | 262 [242-274] | 46 [39-52] | 0.59 / 0.48 / 0.44 | 0.78 / 0.91 / 0.97 | 0.68 / 0.30 / 0.73 |
| bmcs_cal_r | 66 [59-70] | 152 [144-162] | 271 [262-280] | 30 [27-45] | 0.55 / 0.61 / 0.62 | 0.74 / 0.87 / 0.86 | 0.68 / 0.36 / 0.71 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.90 | 2.92e-07 |
| bmcs_cal_r vs transfer | 0.45 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.45 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.92 | 2.58e-08 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.00075 0.00175 0.0015  0.002   0.00125 0.0005  0.00025 0.0001 ]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 57 [50-66] | 136 [126-148] | 232 [220-250] | 67 [60-74] | 0.31 / 0.39 / 0.43 | 0.00 / 0.00 / 0.00 | 0.26 / 0.09 / 0.08 |
| transfer | 60 [51-67] | 130 [126-148] | 241 [220-251] | 65 [57-73] | 0.31 / 0.39 / 0.41 | 1.00 / 1.00 / 1.00 | 0.26 / 0.12 / 0.09 |
| bmcs_cal | 58 [52-64] | 140 [127-146] | 239 [227-254] | 68 [58-74] | 0.28 / 0.35 / 0.38 | 0.62 / 0.64 / 0.61 | 0.25 / 0.10 / 0.08 |
| bmcs_cal_r | 59 [50-66] | 141 [123-149] | 242 [221-253] | 59 [52-73] | 0.28 / 0.36 / 0.39 | 0.61 / 0.63 / 0.62 | 0.25 / 0.15 / 0.15 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.52 | 1 |
| bmcs_cal_r vs transfer | 0.55 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.52 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.47 | 0.717 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 22.4 [7.4-208.4], never: 8/30
- transfer: 13.3 [4.4-202.2], never: 8/30
- bmcs_cal: 31.1 [7.7-240.0], never: 12/30
- bmcs_cal_r: 18.2 [11.3-240.0], never: 11/30

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 62 [54-66] | 138 [125-148] | 236 [217-251] | 74 [64-79] | 0.25 / 0.34 / 0.37 | 0.00 / 0.00 / 0.00 | 0.39 / 0.15 / 0.13 |
| transfer | 60 [52-63] | 140 [131-147] | 243 [230-256] | 63 [57-71] | 0.28 / 0.37 / 0.38 | 1.00 / 1.00 / 1.00 | 0.38 / 0.25 / 0.20 |
| bmcs_cal | 59 [56-62] | 136 [126-147] | 234 [225-249] | 70 [59-79] | 0.28 / 0.33 / 0.36 | 0.65 / 0.74 / 0.71 | 0.38 / 0.18 / 0.14 |
| bmcs_cal_r | 59 [53-63] | 144 [134-150] | 246 [234-258] | 54 [49-61] | 0.29 / 0.39 / 0.42 | 0.62 / 0.67 / 0.66 | 0.38 / 0.26 / 0.28 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.63 | 0.243 |
| bmcs_cal_r vs transfer | 0.57 | 0.383 |
| bmcs_cal_r vs bmcs_cal | 0.63 | 0.243 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.56 | 0.395 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 41.5 [9.2-240.0], never: 10/30
- transfer: 33.9 [8.6-240.0], never: 12/30
- bmcs_cal: 213.4 [11.2-240.0], never: 15/30
- bmcs_cal_r: 12.4 [4.1-209.1], never: 8/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 52 [47-62] | 125 [116-137] | 230 [214-240] | 74 [68-80] | 0.33 / 0.38 / 0.40 | 0.00 / 0.00 / 0.00 | 0.52 / 0.31 / 0.27 |
| transfer | 68 [59-71] | 143 [134-155] | 252 [237-262] | 57 [54-68] | 0.31 / 0.34 / 0.36 | 1.00 / 1.00 / 1.00 | 0.50 / 0.42 / 0.56 |
| bmcs_cal | 58 [54-64] | 136 [126-143] | 240 [220-248] | 70 [61-76] | 0.29 / 0.34 / 0.35 | 0.61 / 0.73 / 0.77 | 0.51 / 0.30 / 0.31 |
| bmcs_cal_r | 62 [55-66] | 143 [134-154] | 251 [236-262] | 51 [43-63] | 0.37 / 0.46 / 0.48 | 0.61 / 0.68 / 0.69 | 0.51 / 0.35 / 0.53 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.77 | 0.00109 |
| bmcs_cal_r vs transfer | 0.49 | 0.882 |
| bmcs_cal_r vs bmcs_cal | 0.68 | 0.0338 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.79 | 8.6e-05 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 17.3 [5.2-206.0], never: 8/30
- transfer: 43.6 [6.3-240.0], never: 12/30
- bmcs_cal: 21.4 [4.7-240.0], never: 12/30
- bmcs_cal_r: 9.6 [4.2-102.8], never: 7/30

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 54 [49-61] | 125 [114-144] | 214 [204-232] | 90 [82-95] | 0.29 / 0.34 / 0.31 | 0.00 / 0.00 / 0.00 | 0.65 / 0.60 / 0.68 |
| transfer | 57 [54-64] | 134 [126-143] | 232 [219-245] | 69 [63-79] | 0.14 / 0.25 / 0.24 | 1.00 / 1.00 / 1.00 | 0.64 / 0.43 / 0.89 |
| bmcs_cal | 53 [48-57] | 122 [113-138] | 212 [202-228] | 88 [77-93] | 0.19 / 0.25 / 0.25 | 0.51 / 0.65 / 0.80 | 0.65 / 0.43 / 0.65 |
| bmcs_cal_r | 54 [47-59] | 132 [124-146] | 237 [222-252] | 61 [52-74] | 0.20 / 0.34 / 0.35 | 0.63 / 0.66 / 0.70 | 0.65 / 0.49 / 0.78 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.60 | 0.386 |
| bmcs_cal_r vs transfer | 0.44 | 0.464 |
| bmcs_cal_r vs bmcs_cal | 0.65 | 0.119 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.05 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 144.1 [11.7-240.0], never: 15/30
- transfer: 240.0 [240.0-240.0], never: 27/30
- bmcs_cal: 240.0 [21.3-240.0], never: 21/30
- bmcs_cal_r: 240.0 [11.6-240.0], never: 16/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00075 0.00075 0.0005  0.00025 0.0001 ]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 54 [49-64] | 144 [130-151] | 307 [293-319] | 152 [141-162] | 0.27 / 0.22 / 0.39 | 0.00 / 0.00 / 0.00 | 0.26 / 0.09 / 0.06 |
| transfer | 60 [57-67] | 146 [139-152] | 292 [280-310] | 157 [139-169] | 0.29 / 0.19 / 0.33 | 1.00 / 1.00 / 1.00 | 0.26 / 0.11 / 0.09 |
| bmcs_cal | 60 [57-68] | 146 [137-152] | 300 [289-320] | 150 [142-164] | 0.33 / 0.22 / 0.36 | 0.69 / 0.75 / 0.72 | 0.25 / 0.10 / 0.08 |
| bmcs_cal_r | 65 [58-71] | 154 [146-160] | 308 [291-328] | 144 [130-163] | 0.40 / 0.21 / 0.32 | 0.65 / 0.70 / 0.69 | 0.25 / 0.18 / 0.16 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.65 | 0.135 |
| bmcs_cal_r vs transfer | 0.62 | 0.241 |
| bmcs_cal_r vs bmcs_cal | 0.58 | 0.267 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.56 | 0.442 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 56 [49-60] | 140 [124-153] | 295 [280-317] | 149 [135-162] | 0.28 / 0.22 / 0.40 | 0.00 / 0.00 / 0.00 | 0.39 / 0.13 / 0.09 |
| transfer | 64 [56-71] | 148 [141-162] | 303 [292-328] | 150 [137-163] | 0.34 / 0.21 / 0.34 | 1.00 / 1.00 / 1.00 | 0.38 / 0.23 / 0.18 |
| bmcs_cal | 67 [56-69] | 150 [142-160] | 308 [284-322] | 155 [141-162] | 0.35 / 0.20 / 0.32 | 0.75 / 0.82 / 0.81 | 0.39 / 0.19 / 0.14 |
| bmcs_cal_r | 64 [56-70] | 146 [138-158] | 309 [296-332] | 146 [117-161] | 0.33 / 0.21 / 0.38 | 0.69 / 0.77 / 0.75 | 0.39 / 0.25 / 0.28 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.63 | 0.243 |
| bmcs_cal_r vs transfer | 0.45 | 0.782 |
| bmcs_cal_r vs bmcs_cal | 0.44 | 0.782 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.68 | 0.0198 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 56 [48-62] | 138 [128-144] | 284 [274-311] | 164 [150-179] | 0.28 / 0.20 / 0.37 | 0.00 / 0.00 / 0.00 | 0.50 / 0.22 / 0.19 |
| transfer | 71 [66-74] | 159 [148-168] | 302 [291-326] | 147 [134-157] | 0.46 / 0.22 / 0.29 | 1.00 / 1.00 / 1.00 | 0.52 / 0.42 / 0.55 |
| bmcs_cal | 65 [61-72] | 152 [140-160] | 300 [284-318] | 152 [145-165] | 0.41 / 0.21 / 0.29 | 0.77 / 0.87 / 0.90 | 0.51 / 0.31 / 0.38 |
| bmcs_cal_r | 64 [59-70] | 152 [139-166] | 320 [283-334] | 144 [119-167] | 0.43 / 0.21 / 0.31 | 0.78 / 0.84 / 0.85 | 0.51 / 0.35 / 0.54 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.77 | 0.00119 |
| bmcs_cal_r vs transfer | 0.40 | 0.391 |
| bmcs_cal_r vs bmcs_cal | 0.53 | 0.679 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.85 | 3.94e-06 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 56 [44-63] | 127 [118-144] | 271 [263-282] | 180 [174-187] | 0.31 / 0.21 / 0.33 | 0.00 / 0.00 / 0.00 | 0.63 / 0.38 / 0.42 |
| transfer | 75 [67-80] | 166 [159-175] | 320 [306-332] | 139 [132-148] | 0.61 / 0.24 / 0.26 | 1.00 / 1.00 / 1.00 | 0.63 / 0.33 / 0.86 |
| bmcs_cal | 72 [66-77] | 165 [154-169] | 310 [304-323] | 146 [139-158] | 0.57 / 0.24 / 0.25 | 0.80 / 0.91 / 0.97 | 0.62 / 0.28 / 0.74 |
| bmcs_cal_r | 68 [63-78] | 158 [146-164] | 292 [281-310] | 158 [144-164] | 0.51 / 0.18 / 0.18 | 0.83 / 0.89 / 0.91 | 0.62 / 0.31 / 0.74 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.87 | 2.94e-06 |
| bmcs_cal_r vs transfer | 0.26 | 0.00276 |
| bmcs_cal_r vs bmcs_cal | 0.33 | 0.0255 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.94 | 6.71e-09 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.002   0.00175 0.0015  0.00125 0.00075 0.0005  0.00025 0.0001 ]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 50 [44-56] | 112 [104-120] | 179 [172-195] | 38 [34-46] | 0.14 / 0.21 / 0.24 | 0.00 / 0.00 / 0.00 | 0.24 / 0.09 / 0.08 |
| transfer | 51 [46-58] | 108 [102-119] | 182 [169-192] | 36 [31-43] | 0.21 / 0.30 / 0.31 | 1.00 / 1.00 / 1.00 | 0.25 / 0.13 / 0.10 |
| bmcs_cal | 51 [46-58] | 114 [106-123] | 192 [176-203] | 32 [27-38] | 0.19 / 0.27 / 0.27 | 0.66 / 0.70 / 0.66 | 0.25 / 0.11 / 0.09 |
| bmcs_cal_r | 56 [50-60] | 117 [110-129] | 192 [179-203] | 26 [19-36] | 0.19 / 0.26 / 0.26 | 0.66 / 0.68 / 0.65 | 0.25 / 0.16 / 0.16 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.65 | 0.081 |
| bmcs_cal_r vs transfer | 0.67 | 0.0779 |
| bmcs_cal_r vs bmcs_cal | 0.58 | 0.304 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.49 | 0.882 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 50 [46-58] | 110 [104-122] | 180 [175-198] | 36 [32-44] | 0.16 / 0.26 / 0.26 | 0.00 / 0.00 / 0.00 | 0.36 / 0.14 / 0.11 |
| transfer | 57 [52-63] | 117 [110-124] | 189 [182-194] | 30 [27-40] | 0.22 / 0.25 / 0.25 | 1.00 / 1.00 / 1.00 | 0.37 / 0.25 / 0.21 |
| bmcs_cal | 50 [48-56] | 108 [106-116] | 183 [175-194] | 33 [28-38] | 0.22 / 0.32 / 0.29 | 0.71 / 0.77 / 0.71 | 0.36 / 0.21 / 0.17 |
| bmcs_cal_r | 54 [49-62] | 118 [108-125] | 190 [177-201] | 29 [23-38] | 0.20 / 0.28 / 0.23 | 0.70 / 0.74 / 0.71 | 0.36 / 0.26 / 0.29 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.61 | 0.251 |
| bmcs_cal_r vs transfer | 0.50 | 0.988 |
| bmcs_cal_r vs bmcs_cal | 0.64 | 0.163 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.63 | 0.0834 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 49 [47-54] | 106 [98-116] | 174 [162-184] | 42 [37-49] | 0.17 / 0.26 / 0.23 | 0.00 / 0.00 / 0.00 | 0.49 / 0.26 / 0.22 |
| transfer | 58 [53-66] | 122 [107-134] | 191 [180-212] | 22 [19-29] | 0.31 / 0.35 / 0.32 | 1.00 / 1.00 / 1.00 | 0.49 / 0.46 / 0.59 |
| bmcs_cal | 56 [51-63] | 116 [108-122] | 187 [178-196] | 32 [26-35] | 0.25 / 0.31 / 0.27 | 0.78 / 0.88 / 0.86 | 0.50 / 0.34 / 0.44 |
| bmcs_cal_r | 55 [50-59] | 118 [111-125] | 193 [182-200] | 27 [21-36] | 0.23 / 0.32 / 0.25 | 0.71 / 0.77 / 0.75 | 0.50 / 0.37 / 0.53 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.71 | 0.0132 |
| bmcs_cal_r vs transfer | 0.43 | 0.774 |
| bmcs_cal_r vs bmcs_cal | 0.54 | 0.774 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00167 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 48 [44-56] | 104 [98-112] | 171 [163-175] | 53 [48-57] | 0.18 / 0.25 / 0.24 | 0.00 / 0.00 / 0.00 | 0.66 / 0.47 / 0.45 |
| transfer | 60 [54-63] | 121 [117-126] | 192 [182-201] | 20 [16-37] | 0.32 / 0.35 / 0.28 | 1.00 / 1.00 / 1.00 | 0.65 / 0.46 / 0.87 |
| bmcs_cal | 56 [51-65] | 120 [105-133] | 190 [180-203] | 25 [23-37] | 0.27 / 0.32 / 0.27 | 0.74 / 0.87 / 0.95 | 0.66 / 0.40 / 0.78 |
| bmcs_cal_r | 56 [48-60] | 116 [109-125] | 194 [181-198] | 22 [17-33] | 0.28 / 0.36 / 0.26 | 0.73 / 0.84 / 0.85 | 0.66 / 0.43 / 0.75 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.74 | 0.00349 |
| bmcs_cal_r vs transfer | 0.38 | 0.23 |
| bmcs_cal_r vs bmcs_cal | 0.46 | 0.599 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.87 | 8.33e-07 |
