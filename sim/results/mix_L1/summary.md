# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 1.0.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 353 [331-374] | 828 [798-852] | 1425 [1398-1460] | 109 [92-115] | 0.84 / 0.93 / 0.95 | 0.00 / 0.00 / 0.00 | 0.79 / 0.00 / 0.00 |
| calib | 377 [364-393] | 864 [840-888] | 1464 [1435-1488] | 43 [39-58] | 0.92 / 0.99 / 0.94 | 0.00 / 0.00 / 0.00 | 0.79 / 0.00 / 0.05 |
| transfer | 408 [396-424] | 898 [880-918] | 1524 [1490-1546] | 12 [11-13] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.63 / 0.00 / 0.01 |
| mix50_cal | 400 [389-416] | 889 [867-910] | 1506 [1467-1522] | 24 [22-26] | 0.99 / 1.00 / 0.95 | 0.49 / 0.50 / 0.50 | 0.70 / 0.00 / 0.02 |
| mix50_cal_r | 385 [374-398] | 863 [851-878] | 1481 [1461-1500] | 38 [35-49] | 0.94 / 0.98 / 0.98 | 0.50 / 0.50 / 0.50 | 0.74 / 0.00 / 0.01 |
| bmcs_cal_r | 403 [383-415] | 888 [859-910] | 1510 [1482-1526] | 18 [16-21] | 0.97 / 0.99 / 0.99 | 0.97 / 0.97 / 0.95 | 0.74 / 0.00 / 0.01 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.88 | 1.68e-06 |
| bmcs_cal_r vs calib | 0.70 | 0.0228 |
| bmcs_cal_r vs transfer | 0.37 | 0.157 |
| bmcs_cal_r vs mix50_cal | 0.47 | 0.652 |
| bmcs_cal_r vs mix50_cal_r | 0.71 | 0.0217 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 3.35e-05 |
| transfer vs fresh | 0.96 | 1.39e-09 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.00000e-02 1.84552e-03 7.26612e-03 1.08729e-03 8.34084e-04 4.74313e-04
 1.19068e-04 3.83869e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 344 [326-356] | 805 [775-830] | 1403 [1374-1431] | 107 [100-125] | 0.77 / 0.88 / 0.89 | 0.00 / 0.00 / 0.00 | 0.81 / 0.01 / 0.01 |
| calib | 381 [294-400] | 858 [640-896] | 1485 [1100-1517] | 40 [34-434] | 0.67 / 0.70 / 0.68 | 0.00 / 0.00 / 0.00 | 0.82 / 0.10 / 0.29 |
| transfer | 412 [396-422] | 894 [871-918] | 1512 [1492-1541] | 10 [8-13] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.63 / 0.00 / 0.01 |
| mix50_cal | 401 [389-415] | 897 [872-916] | 1507 [1472-1537] | 23 [19-26] | 0.99 / 1.00 / 0.96 | 0.49 / 0.50 / 0.50 | 0.73 / 0.00 / 0.01 |
| mix50_cal_r | 382 [378-397] | 876 [845-888] | 1484 [1469-1520] | 43 [36-50] | 0.93 / 0.97 / 0.97 | 0.50 / 0.50 / 0.50 | 0.71 / 0.00 / 0.01 |
| bmcs_cal_r | 396 [381-406] | 894 [865-912] | 1509 [1492-1527] | 19 [14-22] | 0.97 / 0.99 / 0.99 | 0.96 / 0.97 / 0.95 | 0.71 / 0.00 / 0.01 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.98 | 7.67e-10 |
| bmcs_cal_r vs calib | 0.70 | 0.0332 |
| bmcs_cal_r vs transfer | 0.44 | 0.91 |
| bmcs_cal_r vs mix50_cal | 0.45 | 0.91 |
| bmcs_cal_r vs mix50_cal_r | 0.69 | 0.0332 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.73 | 0.00215 |
| transfer vs fresh | 0.99 | 9.42e-11 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.0002 0.005  0.003  0.002  0.001  0.0005 0.01   0.0001]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 352 [332-362] | 822 [806-845] | 1426 [1402-1446] | 105 [93-121] | 0.81 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.81 / 0.01 / 0.22 |
| calib | 386 [370-402] | 872 [856-888] | 1477 [1438-1508] | 38 [32-41] | 0.87 / 0.93 / 0.91 | 0.00 / 0.00 / 0.00 | 0.81 / 0.07 / 0.62 |
| transfer | 179 [171-187] | 410 [398-429] | 712 [698-726] | 811 [803-816] | 0.00 / 0.00 / 0.03 | 1.00 / 1.00 / 1.00 | 0.81 / 0.03 / 0.44 |
| mix50_cal | 327 [205-366] | 819 [544-858] | 1416 [1055-1468] | 91 [73-453] | 0.61 / 0.76 / 0.78 | 0.49 / 0.50 / 0.50 | 0.81 / 0.03 / 0.12 |
| mix50_cal_r | 332 [258-355] | 800 [733-825] | 1408 [1337-1454] | 128 [74-188] | 0.64 / 0.84 / 0.86 | 0.50 / 0.50 / 0.50 | 0.81 / 0.03 / 0.18 |
| bmcs_cal_r | 356 [334-378] | 846 [810-858] | 1457 [1434-1493] | 67 [56-83] | 0.86 / 0.96 / 0.96 | 0.01 / 0.00 / 0.01 | 0.81 / 0.01 / 0.36 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.66 | 0.0755 |
| bmcs_cal_r vs calib | 0.27 | 0.00883 |
| bmcs_cal_r vs transfer | 1.00 | 1.43e-10 |
| bmcs_cal_r vs mix50_cal | 0.64 | 0.0755 |
| bmcs_cal_r vs mix50_cal_r | 0.73 | 0.00883 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.01 | 9.36e-11 |
| transfer vs fresh | 0.00 | 5.71e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 1.8 [1.5-2.4], never: 0/30
- calib: 1.2 [1.2-1.3], never: 0/30
- transfer: 240.0 [240.0-240.0], never: 29/30
- mix50_cal: 2.7 [2.0-25.4], never: 2/30
- mix50_cal_r: 3.7 [2.3-7.3], never: 1/30
- bmcs_cal_r: 1.9 [1.7-2.3], never: 0/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 48 [41-56] | 133 [119-141] | 238 [224-250] | 66 [60-75] | 0.52 / 0.76 / 0.81 | 0.00 / 0.00 / 0.00 | 0.82 / 0.40 / 0.60 |
| calib | 40 [33-55] | 106 [93-128] | 198 [180-220] | 105 [92-114] | 0.43 / 0.58 / 0.65 | 0.00 / 0.00 / 0.00 | 0.82 / 0.36 / 0.25 |
| transfer | 69 [64-78] | 147 [138-164] | 252 [236-264] | 45 [43-50] | 0.79 / 0.75 / 0.76 | 1.00 / 1.00 / 1.00 | 0.80 / 0.76 / 0.87 |
| mix50_cal | 54 [47-60] | 124 [118-138] | 226 [214-242] | 78 [73-85] | 0.60 / 0.65 / 0.70 | 0.50 / 0.50 / 0.50 | 0.82 / 0.42 / 0.35 |
| mix50_cal_r | 70 [58-80] | 162 [150-175] | 274 [260-295] | 29 [20-36] | 0.79 / 0.91 / 0.91 | 0.51 / 0.50 / 0.50 | 0.81 / 0.61 / 0.71 |
| bmcs_cal_r | 68 [58-74] | 163 [147-171] | 282 [275-289] | 22 [16-30] | 0.84 / 0.92 / 0.91 | 0.85 / 0.89 / 0.88 | 0.81 / 0.68 / 0.71 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.92 | 6.24e-08 |
| bmcs_cal_r vs calib | 0.96 | 3.17e-09 |
| bmcs_cal_r vs transfer | 0.67 | 0.0551 |
| bmcs_cal_r vs mix50_cal | 0.93 | 4.95e-08 |
| bmcs_cal_r vs mix50_cal_r | 0.48 | 0.813 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.91 | 1.1e-07 |
| transfer vs fresh | 0.81 | 4.74e-05 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 122 [113-132] | 288 [278-302] | 510 [490-528] | 99 [88-108] | 0.40 / 0.53 / 0.56 | 0.00 / 0.00 / 0.00 | 0.50 / 0.06 / 0.08 |
| calib | 133 [118-148] | 300 [283-334] | 510 [489-558] | 103 [51-116] | 0.41 / 0.49 / 0.48 | 0.00 / 0.00 / 0.00 | 0.50 / 0.15 / 0.16 |
| transfer | 158 [146-170] | 345 [326-360] | 578 [552-594] | 35 [26-57] | 0.71 / 0.69 / 0.66 | 1.00 / 1.00 / 1.00 | 0.49 / 0.06 / 0.29 |
| mix50_cal | 146 [135-158] | 324 [310-337] | 554 [539-578] | 47 [42-58] | 0.73 / 0.71 / 0.69 | 0.51 / 0.50 / 0.50 | 0.51 / 0.08 / 0.12 |
| mix50_cal_r | 136 [125-150] | 309 [293-324] | 533 [509-556] | 75 [65-87] | 0.47 / 0.54 / 0.56 | 0.50 / 0.50 / 0.50 | 0.50 / 0.06 / 0.13 |
| bmcs_cal_r | 142 [132-147] | 320 [302-338] | 548 [523-574] | 59 [51-86] | 0.55 / 0.61 / 0.63 | 0.83 / 0.89 / 0.87 | 0.50 / 0.05 / 0.17 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.82 | 9e-05 |
| bmcs_cal_r vs calib | 0.63 | 0.251 |
| bmcs_cal_r vs transfer | 0.25 | 0.0036 |
| bmcs_cal_r vs mix50_cal | 0.45 | 0.506 |
| bmcs_cal_r vs mix50_cal_r | 0.63 | 0.251 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 8.84e-06 |
| transfer vs fresh | 0.98 | 4.94e-10 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.0015 0.0035 0.003  0.004  0.0025 0.001  0.0005 0.0002]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 122 [118-134] | 296 [270-308] | 506 [492-538] | 99 [83-112] | 0.36 / 0.47 / 0.50 | 0.00 / 0.00 / 0.00 | 0.50 / 0.09 / 0.17 |
| calib | 137 [125-152] | 309 [288-325] | 526 [493-566] | 84 [53-116] | 0.46 / 0.50 / 0.48 | 0.00 / 0.00 / 0.00 | 0.51 / 0.19 / 0.26 |
| transfer | 136 [125-150] | 300 [284-323] | 510 [495-546] | 97 [68-111] | 0.27 / 0.34 / 0.35 | 1.00 / 1.00 / 1.00 | 0.49 / 0.10 / 0.35 |
| mix50_cal | 128 [118-141] | 298 [279-318] | 504 [483-532] | 102 [87-118] | 0.27 / 0.34 / 0.34 | 0.50 / 0.50 / 0.50 | 0.50 / 0.13 / 0.15 |
| mix50_cal_r | 130 [120-137] | 294 [282-318] | 517 [493-543] | 84 [66-105] | 0.42 / 0.52 / 0.53 | 0.50 / 0.50 / 0.50 | 0.49 / 0.08 / 0.18 |
| bmcs_cal_r | 126 [119-135] | 301 [288-310] | 518 [503-531] | 90 [73-103] | 0.39 / 0.51 / 0.52 | 0.71 / 0.79 / 0.79 | 0.49 / 0.08 / 0.19 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.59 | 1 |
| bmcs_cal_r vs calib | 0.41 | 1 |
| bmcs_cal_r vs transfer | 0.44 | 1 |
| bmcs_cal_r vs mix50_cal | 0.51 | 1 |
| bmcs_cal_r vs mix50_cal_r | 0.52 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.48 | 0.756 |
| transfer vs fresh | 0.64 | 0.145 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 11.2 [4.6-38.2], never: 6/30
- calib: 6.6 [2.4-240.0], never: 11/30
- transfer: 240.0 [5.7-240.0], never: 17/30
- mix50_cal: 240.0 [4.1-240.0], never: 19/30
- mix50_cal_r: 5.2 [3.2-26.6], never: 5/30
- bmcs_cal_r: 12.0 [4.6-92.2], never: 7/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0015 0.0015 0.001  0.0005 0.0002]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 122 [116-130] | 300 [284-314] | 649 [605-666] | 277 [251-301] | 0.34 / 0.21 / 0.39 | 0.00 / 0.00 / 0.00 | 0.51 / 0.07 / 0.09 |
| calib | 140 [128-154] | 323 [304-336] | 630 [603-659] | 289 [253-311] | 0.54 / 0.23 / 0.29 | 0.00 / 0.00 / 0.00 | 0.49 / 0.12 / 0.16 |
| transfer | 153 [139-167] | 336 [316-353] | 632 [612-655] | 279 [251-300] | 0.63 / 0.23 / 0.24 | 1.00 / 1.00 / 1.00 | 0.50 / 0.09 / 0.31 |
| mix50_cal | 147 [137-156] | 325 [310-339] | 614 [589-642] | 296 [262-305] | 0.57 / 0.22 / 0.24 | 0.50 / 0.50 / 0.50 | 0.50 / 0.10 / 0.13 |
| mix50_cal_r | 134 [128-149] | 315 [304-330] | 620 [590-650] | 288 [264-305] | 0.52 / 0.21 / 0.28 | 0.50 / 0.50 / 0.50 | 0.49 / 0.07 / 0.12 |
| bmcs_cal_r | 140 [128-149] | 319 [310-333] | 628 [581-662] | 275 [251-322] | 0.50 / 0.21 / 0.27 | 0.85 / 0.91 / 0.92 | 0.49 / 0.06 / 0.19 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.74 | 0.00584 |
| bmcs_cal_r vs calib | 0.49 | 1 |
| bmcs_cal_r vs transfer | 0.32 | 0.0563 |
| bmcs_cal_r vs mix50_cal | 0.43 | 1 |
| bmcs_cal_r vs mix50_cal_r | 0.55 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.66 | 0.0345 |
| transfer vs fresh | 0.87 | 1.57e-06 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 99 [92-104] | 210 [202-223] | 349 [337-362] | 42 [35-52] | 0.24 / 0.29 / 0.24 | 0.00 / 0.00 / 0.00 | 0.49 / 0.13 / 0.16 |
| calib | 110 [98-118] | 224 [209-233] | 342 [330-368] | 47 [39-66] | 0.24 / 0.18 / 0.18 | 0.00 / 0.00 / 0.00 | 0.49 / 0.18 / 0.16 |
| transfer | 118 [106-124] | 238 [224-252] | 372 [353-387] | 34 [28-49] | 0.30 / 0.20 / 0.19 | 1.00 / 1.00 / 1.00 | 0.47 / 0.15 / 0.46 |
| mix50_cal | 107 [96-113] | 222 [215-231] | 347 [337-362] | 40 [24-53] | 0.22 / 0.22 / 0.21 | 0.51 / 0.50 / 0.50 | 0.48 / 0.16 / 0.17 |
| mix50_cal_r | 112 [102-119] | 229 [222-240] | 363 [351-372] | 38 [30-44] | 0.31 / 0.24 / 0.20 | 0.50 / 0.50 / 0.50 | 0.49 / 0.10 / 0.21 |
| bmcs_cal_r | 104 [99-113] | 225 [215-234] | 359 [346-370] | 37 [27-42] | 0.30 / 0.30 / 0.24 | 0.78 / 0.83 / 0.79 | 0.49 / 0.11 / 0.30 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.71 | 0.022 |
| bmcs_cal_r vs calib | 0.55 | 0.946 |
| bmcs_cal_r vs transfer | 0.30 | 0.0362 |
| bmcs_cal_r vs mix50_cal | 0.53 | 0.946 |
| bmcs_cal_r vs mix50_cal_r | 0.40 | 0.557 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00167 |
| transfer vs fresh | 0.84 | 1.43e-05 |
