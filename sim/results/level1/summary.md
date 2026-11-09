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
| bmcs_cal | 400 [389-411] | 886 [865-919] | 1506 [1466-1530] | 16 [15-19] | 0.99 / 1.00 / 0.97 | 0.73 / 0.63 / 0.93 | 0.74 / 0.00 / 0.01 |
| bmcs_cf | 394 [380-410] | 874 [860-913] | 1492 [1474-1510] | 30 [26-32] | 0.97 / 0.98 / 0.96 | 0.97 / 0.99 / 0.98 | 0.70 / 0.00 / 0.01 |
| bmcs_cal_r | 403 [383-415] | 888 [859-910] | 1510 [1482-1526] | 18 [16-21] | 0.97 / 0.99 / 0.99 | 0.97 / 0.97 / 0.95 | 0.74 / 0.00 / 0.01 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.91 | 4.23e-07 |
| bmcs_cal vs calib | 0.71 | 0.0278 |
| bmcs_cal vs transfer | 0.39 | 0.64 |
| bmcs_cal vs mix50_cal | 0.49 | 1 |
| bmcs_cal vs bmcs_cf | 0.56 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.55 | 1 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.88 | 3.1e-06 |
| bmcs_cf vs calib | 0.65 | 0.171 |
| bmcs_cf vs transfer | 0.33 | 0.0992 |
| bmcs_cf vs mix50_cal | 0.43 | 1 |
| bmcs_cf vs bmcs_cal | 0.44 | 1 |
| bmcs_cf vs bmcs_cal_r | 0.49 | 1 |

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
| bmcs_cal | 408 [394-420] | 888 [865-910] | 1510 [1475-1534] | 15 [13-19] | 0.99 / 1.00 / 0.97 | 0.77 / 0.66 / 0.91 | 0.71 / 0.00 / 0.01 |
| bmcs_cf | 390 [378-401] | 880 [860-903] | 1486 [1478-1522] | 30 [25-37] | 0.97 / 0.98 / 0.96 | 0.97 / 0.98 / 0.98 | 0.73 / 0.00 / 0.01 |
| bmcs_cal_r | 396 [381-406] | 894 [865-912] | 1509 [1492-1527] | 19 [14-22] | 0.97 / 0.99 / 0.99 | 0.96 / 0.97 / 0.95 | 0.71 / 0.00 / 0.01 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.95 | 8.44e-09 |
| bmcs_cal vs calib | 0.67 | 0.13 |
| bmcs_cal vs transfer | 0.43 | 1 |
| bmcs_cal vs mix50_cal | 0.42 | 1 |
| bmcs_cal vs bmcs_cf | 0.53 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.46 | 1 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.95 | 8.84e-09 |
| bmcs_cf vs calib | 0.65 | 0.199 |
| bmcs_cf vs transfer | 0.40 | 0.685 |
| bmcs_cf vs mix50_cal | 0.40 | 0.685 |
| bmcs_cf vs bmcs_cal | 0.47 | 0.832 |
| bmcs_cf vs bmcs_cal_r | 0.44 | 0.832 |

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
| bmcs_cal | 376 [357-395] | 867 [836-896] | 1485 [1446-1512] | 44 [39-58] | 0.90 / 0.96 / 0.92 | 0.01 / 0.00 / 0.01 | 0.81 / 0.02 / 0.47 |
| bmcs_cf | 348 [338-357] | 818 [792-832] | 1416 [1366-1442] | 111 [100-129] | 0.83 / 0.93 / 0.94 | 0.01 / 0.00 / 0.01 | 0.81 / 0.00 / 0.22 |
| bmcs_cal_r | 356 [334-378] | 846 [810-858] | 1457 [1434-1493] | 67 [56-83] | 0.86 / 0.96 / 0.96 | 0.01 / 0.00 / 0.01 | 0.81 / 0.01 / 0.36 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.81 | 0.00013 |
| bmcs_cal vs calib | 0.47 | 0.739 |
| bmcs_cal vs transfer | 1.00 | 1.71e-10 |
| bmcs_cal vs mix50_cal | 0.77 | 0.00107 |
| bmcs_cal vs bmcs_cf | 0.84 | 4.13e-05 |
| bmcs_cal vs bmcs_cal_r | 0.69 | 0.0197 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.43 | 0.711 |
| bmcs_cf vs calib | 0.19 | 0.000126 |
| bmcs_cf vs transfer | 1.00 | 1.71e-10 |
| bmcs_cf vs mix50_cal | 0.51 | 0.848 |
| bmcs_cf vs bmcs_cal | 0.17 | 4.13e-05 |
| bmcs_cf vs bmcs_cal_r | 0.29 | 0.0183 |

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
- bmcs_cal: 1.4 [1.2-1.9], never: 1/30
- bmcs_cf: 1.6 [1.3-2.0], never: 0/30
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
| bmcs_cal | 68 [61-74] | 148 [130-156] | 244 [232-262] | 55 [51-61] | 0.73 / 0.72 / 0.74 | 0.87 / 0.94 / 0.94 | 0.81 / 0.63 / 0.79 |
| bmcs_cf | 63 [59-67] | 146 [136-154] | 250 [234-268] | 54 [49-58] | 0.71 / 0.75 / 0.77 | 0.87 / 0.94 / 0.91 | 0.80 / 0.64 / 0.82 |
| bmcs_cal_r | 68 [58-74] | 163 [147-171] | 282 [275-289] | 22 [16-30] | 0.84 / 0.92 / 0.91 | 0.85 / 0.89 / 0.88 | 0.81 / 0.68 / 0.71 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.74 | 0.0048 |
| bmcs_cal vs calib | 0.88 | 2.26e-06 |
| bmcs_cal vs transfer | 0.43 | 0.643 |
| bmcs_cal vs mix50_cal | 0.76 | 0.00216 |
| bmcs_cal vs bmcs_cf | 0.50 | 0.971 |
| bmcs_cal vs bmcs_cal_r | 0.27 | 0.00676 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.79 | 0.000557 |
| bmcs_cf vs calib | 0.90 | 7.18e-07 |
| bmcs_cf vs transfer | 0.42 | 0.629 |
| bmcs_cf vs mix50_cal | 0.81 | 0.000209 |
| bmcs_cf vs bmcs_cal | 0.50 | 0.971 |
| bmcs_cf vs bmcs_cal_r | 0.24 | 0.00149 |

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
| bmcs_cal | 148 [142-162] | 336 [315-348] | 567 [546-576] | 43 [38-63] | 0.69 / 0.67 / 0.64 | 0.75 / 0.84 / 0.94 | 0.50 / 0.08 / 0.19 |
| bmcs_cf | 146 [139-156] | 327 [309-340] | 553 [532-568] | 55 [48-71] | 0.61 / 0.62 / 0.61 | 0.87 / 0.93 / 0.92 | 0.49 / 0.07 / 0.14 |
| bmcs_cal_r | 142 [132-147] | 320 [302-338] | 548 [523-574] | 59 [51-86] | 0.55 / 0.61 / 0.63 | 0.83 / 0.89 / 0.87 | 0.50 / 0.05 / 0.17 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.92 | 1.76e-07 |
| bmcs_cal vs calib | 0.74 | 0.00738 |
| bmcs_cal vs transfer | 0.35 | 0.168 |
| bmcs_cal vs mix50_cal | 0.61 | 0.29 |
| bmcs_cal vs bmcs_cf | 0.61 | 0.29 |
| bmcs_cal vs bmcs_cal_r | 0.64 | 0.217 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.85 | 2.29e-05 |
| bmcs_cf vs calib | 0.66 | 0.135 |
| bmcs_cf vs transfer | 0.26 | 0.00795 |
| bmcs_cf vs mix50_cal | 0.49 | 1 |
| bmcs_cf vs bmcs_cal | 0.39 | 0.435 |
| bmcs_cf vs bmcs_cal_r | 0.52 | 1 |

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
| bmcs_cal | 140 [130-152] | 318 [300-334] | 542 [506-560] | 88 [64-104] | 0.39 / 0.41 / 0.41 | 0.58 / 0.68 / 0.83 | 0.49 / 0.10 / 0.17 |
| bmcs_cf | 126 [114-135] | 296 [268-316] | 514 [474-525] | 103 [79-129] | 0.30 / 0.39 / 0.40 | 0.73 / 0.80 / 0.79 | 0.50 / 0.11 / 0.15 |
| bmcs_cal_r | 126 [119-135] | 301 [288-310] | 518 [503-531] | 90 [73-103] | 0.39 / 0.51 / 0.52 | 0.71 / 0.79 / 0.79 | 0.49 / 0.08 / 0.19 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.77 | 0.00245 |
| bmcs_cal vs calib | 0.58 | 0.277 |
| bmcs_cal vs transfer | 0.63 | 0.187 |
| bmcs_cal vs mix50_cal | 0.70 | 0.0243 |
| bmcs_cal vs bmcs_cf | 0.72 | 0.0201 |
| bmcs_cal vs bmcs_cal_r | 0.71 | 0.0212 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.52 | 1 |
| bmcs_cf vs calib | 0.37 | 0.431 |
| bmcs_cf vs transfer | 0.40 | 0.695 |
| bmcs_cf vs mix50_cal | 0.46 | 1 |
| bmcs_cf vs bmcs_cal | 0.28 | 0.0241 |
| bmcs_cf vs bmcs_cal_r | 0.45 | 1 |

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
- bmcs_cal: 128.8 [3.3-240.0], never: 15/30
- bmcs_cf: 16.1 [4.7-240.0], never: 11/30
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
| bmcs_cal | 142 [133-152] | 322 [313-334] | 619 [602-661] | 271 [248-301] | 0.61 / 0.23 / 0.27 | 0.69 / 0.83 / 0.94 | 0.49 / 0.10 / 0.19 |
| bmcs_cf | 144 [134-150] | 326 [314-344] | 640 [616-673] | 272 [254-290] | 0.58 / 0.24 / 0.28 | 0.88 / 0.93 / 0.92 | 0.50 / 0.07 / 0.14 |
| bmcs_cal_r | 140 [128-149] | 319 [310-333] | 628 [581-662] | 275 [251-322] | 0.50 / 0.21 / 0.27 | 0.85 / 0.91 / 0.92 | 0.49 / 0.06 / 0.19 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.78 | 0.00131 |
| bmcs_cal vs calib | 0.51 | 1 |
| bmcs_cal vs transfer | 0.32 | 0.0863 |
| bmcs_cal vs mix50_cal | 0.45 | 1 |
| bmcs_cal vs bmcs_cf | 0.42 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.53 | 1 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.84 | 4.62e-05 |
| bmcs_cf vs calib | 0.58 | 0.792 |
| bmcs_cf vs transfer | 0.40 | 0.778 |
| bmcs_cf vs mix50_cal | 0.53 | 0.792 |
| bmcs_cf vs bmcs_cal | 0.58 | 0.792 |
| bmcs_cf vs bmcs_cal_r | 0.61 | 0.778 |

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
| bmcs_cal | 110 [104-120] | 232 [221-240] | 358 [351-372] | 36 [25-50] | 0.29 / 0.20 / 0.19 | 0.67 / 0.82 / 0.89 | 0.49 / 0.14 / 0.28 |
| bmcs_cf | 106 [98-118] | 226 [219-238] | 359 [345-377] | 40 [33-45] | 0.26 / 0.25 / 0.23 | 0.81 / 0.84 / 0.81 | 0.48 / 0.13 / 0.23 |
| bmcs_cal_r | 104 [99-113] | 225 [215-234] | 359 [346-370] | 37 [27-42] | 0.30 / 0.30 / 0.24 | 0.78 / 0.83 / 0.79 | 0.49 / 0.11 / 0.30 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.76 | 0.00264 |
| bmcs_cal vs calib | 0.64 | 0.312 |
| bmcs_cal vs transfer | 0.38 | 0.331 |
| bmcs_cal vs mix50_cal | 0.64 | 0.312 |
| bmcs_cal vs bmcs_cf | 0.56 | 0.437 |
| bmcs_cal vs bmcs_cal_r | 0.60 | 0.407 |

bmcs_cf vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cf > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cf vs fresh | 0.74 | 0.0095 |
| bmcs_cf vs calib | 0.59 | 0.947 |
| bmcs_cf vs transfer | 0.32 | 0.0764 |
| bmcs_cf vs mix50_cal | 0.58 | 0.947 |
| bmcs_cf vs bmcs_cal | 0.44 | 0.947 |
| bmcs_cf vs bmcs_cal_r | 0.54 | 0.947 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00167 |
| transfer vs fresh | 0.84 | 1.43e-05 |
