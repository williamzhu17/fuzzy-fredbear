# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256, v+1 level multiplier = 1.0.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 382 [363-401] | 844 [828-870] | 1460 [1434-1489] | 60 [52-75] | 0.93 / 0.95 / 0.95 | 0.00 / 0.00 / 0.00 | 0.47 / 0.02 / 0.02 |
| transfer | 396 [386-408] | 870 [855-896] | 1488 [1456-1510] | 41 [37-48] | 0.97 / 0.96 / 0.96 | 1.00 / 1.00 / 1.00 | 0.44 / 0.03 / 0.06 |
| bmcs_cal | 382 [376-405] | 860 [845-871] | 1464 [1439-1481] | 48 [45-56] | 0.96 / 0.95 / 0.95 | 0.83 / 0.91 / 0.90 | 0.44 / 0.03 / 0.05 |
| bmcs_cal_r | 392 [372-404] | 870 [833-894] | 1478 [1445-1519] | 44 [36-52] | 0.94 / 0.97 / 0.97 | 0.91 / 0.90 / 0.87 | 0.44 / 0.02 / 0.08 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.64 | 0.204 |
| bmcs_cal_r vs transfer | 0.46 | 0.636 |
| bmcs_cal_r vs bmcs_cal | 0.59 | 0.516 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.72 | 0.00274 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 380 [373-396] | 868 [838-890] | 1469 [1443-1491] | 45 [38-53] | 0.96 / 0.97 / 0.95 | 0.00 / 0.00 / 0.00 | 0.65 / 0.01 / 0.04 |
| transfer | 414 [388-426] | 890 [868-914] | 1498 [1470-1522] | 25 [23-28] | 0.99 / 0.98 / 0.96 | 1.00 / 1.00 / 1.00 | 0.54 / 0.01 / 0.09 |
| bmcs_cal | 400 [387-409] | 877 [862-904] | 1498 [1472-1525] | 29 [25-34] | 0.99 / 0.97 / 0.96 | 0.77 / 0.84 / 0.95 | 0.55 / 0.01 / 0.06 |
| bmcs_cal_r | 390 [380-399] | 870 [846-880] | 1486 [1460-1510] | 30 [23-35] | 0.96 / 0.98 / 0.98 | 0.95 / 0.95 / 0.93 | 0.55 / 0.00 / 0.05 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.52 | 0.751 |
| bmcs_cal_r vs transfer | 0.31 | 0.0315 |
| bmcs_cal_r vs bmcs_cal | 0.38 | 0.198 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.68 | 0.0195 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 377 [364-393] | 864 [840-888] | 1464 [1435-1488] | 43 [39-58] | 0.92 / 0.99 / 0.94 | 0.00 / 0.00 / 0.00 | 0.79 / 0.00 / 0.05 |
| transfer | 408 [396-424] | 898 [880-918] | 1524 [1490-1546] | 12 [11-13] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.63 / 0.00 / 0.01 |
| bmcs_cal | 400 [389-411] | 886 [865-919] | 1506 [1466-1530] | 16 [15-19] | 0.99 / 1.00 / 0.97 | 0.73 / 0.63 / 0.93 | 0.74 / 0.00 / 0.01 |
| bmcs_cal_r | 403 [383-415] | 888 [859-910] | 1510 [1482-1526] | 18 [16-21] | 0.97 / 0.99 / 0.99 | 0.97 / 0.97 / 0.95 | 0.74 / 0.00 / 0.01 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.70 | 0.0228 |
| bmcs_cal_r vs transfer | 0.37 | 0.157 |
| bmcs_cal_r vs bmcs_cal | 0.45 | 0.539 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 3.35e-05 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 380 [358-389] | 872 [853-890] | 1482 [1454-1516] | 39 [29-46] | 0.93 / 1.00 / 0.97 | 0.00 / 0.00 / 0.00 | 0.86 / 0.00 / 0.00 |
| transfer | 397 [389-410] | 887 [870-906] | 1502 [1490-1529] | 7 [7-8] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.77 / 0.00 / 0.00 |
| bmcs_cal | 403 [387-414] | 896 [886-907] | 1522 [1503-1540] | 10 [10-12] | 0.99 / 1.00 / 0.97 | 0.80 / 0.66 / 0.81 | 0.82 / 0.00 / 0.00 |
| bmcs_cal_r | 396 [388-410] | 877 [860-899] | 1500 [1486-1514] | 16 [13-19] | 0.98 / 0.99 / 0.99 | 0.97 / 0.99 / 0.99 | 0.82 / 0.00 / 0.00 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.61 | 0.29 |
| bmcs_cal_r vs transfer | 0.43 | 0.379 |
| bmcs_cal_r vs bmcs_cal | 0.32 | 0.055 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.67 | 0.0236 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.00000e-02 1.84552e-03 7.26612e-03 1.08729e-03 8.34084e-04 4.74313e-04
 1.19068e-04 3.83869e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 374 [358-393] | 852 [810-862] | 1450 [1420-1481] | 61 [51-82] | 0.80 / 0.84 / 0.85 | 0.00 / 0.00 / 0.00 | 0.48 / 0.04 / 0.03 |
| transfer | 398 [383-411] | 877 [847-903] | 1486 [1466-1509] | 39 [34-42] | 0.96 / 0.95 / 0.95 | 1.00 / 1.00 / 1.00 | 0.42 / 0.04 / 0.06 |
| bmcs_cal | 386 [369-404] | 858 [825-875] | 1459 [1425-1497] | 44 [41-66] | 0.92 / 0.92 / 0.92 | 0.83 / 0.88 / 0.88 | 0.45 / 0.03 / 0.05 |
| bmcs_cal_r | 384 [375-395] | 870 [850-882] | 1469 [1438-1488] | 48 [35-68] | 0.90 / 0.93 / 0.93 | 0.89 / 0.89 / 0.85 | 0.45 / 0.02 / 0.09 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.68 | 0.0596 |
| bmcs_cal_r vs transfer | 0.42 | 0.329 |
| bmcs_cal_r vs bmcs_cal | 0.60 | 0.329 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.72 | 0.00393 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 380 [358-397] | 864 [824-898] | 1468 [1425-1495] | 45 [40-57] | 0.84 / 0.87 / 0.85 | 0.00 / 0.00 / 0.00 | 0.68 / 0.03 / 0.06 |
| transfer | 406 [394-418] | 897 [881-918] | 1509 [1488-1546] | 20 [19-24] | 1.00 / 0.98 / 0.96 | 1.00 / 1.00 / 1.00 | 0.50 / 0.00 / 0.08 |
| bmcs_cal | 406 [388-418] | 884 [862-907] | 1512 [1472-1529] | 27 [24-32] | 0.98 / 0.98 / 0.96 | 0.76 / 0.80 / 0.93 | 0.61 / 0.00 / 0.06 |
| bmcs_cal_r | 396 [387-407] | 881 [866-894] | 1498 [1480-1524] | 28 [23-36] | 0.96 / 0.97 / 0.97 | 0.93 / 0.93 / 0.90 | 0.61 / 0.00 / 0.04 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.61 | 0.263 |
| bmcs_cal_r vs transfer | 0.34 | 0.0892 |
| bmcs_cal_r vs bmcs_cal | 0.46 | 0.615 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.72 | 0.00296 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 381 [294-400] | 858 [640-896] | 1485 [1100-1517] | 40 [34-434] | 0.67 / 0.70 / 0.68 | 0.00 / 0.00 / 0.00 | 0.82 / 0.10 / 0.29 |
| transfer | 412 [396-422] | 894 [871-918] | 1512 [1492-1541] | 10 [8-13] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.63 / 0.00 / 0.01 |
| bmcs_cal | 408 [394-420] | 888 [865-910] | 1510 [1475-1534] | 15 [13-19] | 0.99 / 1.00 / 0.97 | 0.77 / 0.66 / 0.91 | 0.71 / 0.00 / 0.01 |
| bmcs_cal_r | 396 [381-406] | 894 [865-912] | 1509 [1492-1527] | 19 [14-22] | 0.97 / 0.99 / 0.99 | 0.96 / 0.97 / 0.95 | 0.71 / 0.00 / 0.01 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.70 | 0.0249 |
| bmcs_cal_r vs transfer | 0.44 | 0.91 |
| bmcs_cal_r vs bmcs_cal | 0.54 | 0.91 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.73 | 0.00215 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 369 [298-394] | 848 [676-888] | 1468 [1128-1518] | 36 [26-429] | 0.67 / 0.70 / 0.70 | 0.00 / 0.00 / 0.00 | 0.86 / 0.17 / 0.30 |
| transfer | 407 [395-423] | 902 [879-923] | 1520 [1506-1553] | 7 [3-11] | 1.00 / 1.00 / 0.98 | 1.00 / 1.00 / 1.00 | 0.79 / 0.00 / 0.00 |
| bmcs_cal | 402 [387-412] | 900 [873-913] | 1520 [1486-1530] | 11 [8-16] | 0.99 / 1.00 / 0.98 | 0.81 / 0.62 / 0.73 | 0.84 / 0.00 / 0.00 |
| bmcs_cal_r | 395 [387-406] | 886 [871-907] | 1508 [1489-1525] | 17 [14-20] | 0.97 / 0.99 / 0.99 | 0.97 / 0.98 / 0.97 | 0.84 / 0.00 / 0.00 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.73 | 0.00748 |
| bmcs_cal_r vs transfer | 0.36 | 0.115 |
| bmcs_cal_r vs bmcs_cal | 0.38 | 0.117 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.81 | 3.58e-05 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.0002 0.005  0.003  0.002  0.001  0.0005 0.01   0.0001]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 380 [355-394] | 846 [831-873] | 1463 [1430-1486] | 64 [55-80] | 0.92 / 0.95 / 0.95 | 0.00 / 0.00 / 0.00 | 0.52 / 0.07 / 0.11 |
| transfer | 357 [326-368] | 824 [802-855] | 1419 [1393-1452] | 88 [70-123] | 0.81 / 0.92 / 0.92 | 1.00 / 1.00 / 1.00 | 0.50 / 0.03 / 0.04 |
| bmcs_cal | 364 [341-388] | 837 [802-854] | 1430 [1396-1467] | 70 [58-102] | 0.88 / 0.93 / 0.94 | 0.13 / 0.17 / 0.24 | 0.50 / 0.04 / 0.04 |
| bmcs_cal_r | 364 [316-380] | 846 [765-867] | 1444 [1360-1482] | 69 [54-134] | 0.74 / 0.89 / 0.90 | 0.20 / 0.22 / 0.29 | 0.50 / 0.05 / 0.14 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.41 | 0.693 |
| bmcs_cal_r vs transfer | 0.56 | 0.832 |
| bmcs_cal_r vs bmcs_cal | 0.54 | 0.832 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.33 | 0.0223 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 1.2 [1.2-1.9], never: 0/30
- transfer: 2.2 [1.6-3.7], never: 0/30
- bmcs_cal: 1.5 [1.2-1.9], never: 0/30
- bmcs_cal_r: 1.6 [1.2-3.9], never: 0/30

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 386 [370-401] | 853 [839-870] | 1465 [1427-1490] | 45 [40-56] | 0.92 / 0.96 / 0.94 | 0.00 / 0.00 / 0.00 | 0.69 / 0.06 / 0.33 |
| transfer | 197 [179-220] | 540 [454-660] | 1028 [838-1223] | 473 [270-682] | 0.19 / 0.51 / 0.56 | 1.00 / 1.00 / 1.00 | 0.68 / 0.11 / 0.16 |
| bmcs_cal | 376 [342-399] | 859 [803-880] | 1448 [1393-1480] | 62 [46-116] | 0.82 / 0.94 / 0.92 | 0.06 / 0.03 / 0.13 | 0.69 / 0.03 / 0.17 |
| bmcs_cal_r | 366 [356-386] | 856 [821-864] | 1458 [1436-1485] | 58 [45-78] | 0.87 / 0.94 / 0.95 | 0.04 / 0.03 / 0.10 | 0.69 / 0.03 / 0.22 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.45 | 1 |
| bmcs_cal_r vs transfer | 0.93 | 2.43e-08 |
| bmcs_cal_r vs bmcs_cal | 0.47 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.05 | 3.19e-09 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 1.2 [1.2-1.5], never: 0/30
- transfer: 27.3 [11.4-93.3], never: 6/30
- bmcs_cal: 1.6 [1.2-2.8], never: 0/30
- bmcs_cal_r: 1.4 [1.3-1.8], never: 0/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 386 [370-402] | 872 [856-888] | 1477 [1438-1508] | 38 [32-41] | 0.87 / 0.93 / 0.91 | 0.00 / 0.00 / 0.00 | 0.81 / 0.07 / 0.62 |
| transfer | 179 [171-187] | 410 [398-429] | 712 [698-726] | 811 [803-816] | 0.00 / 0.00 / 0.03 | 1.00 / 1.00 / 1.00 | 0.81 / 0.03 / 0.44 |
| bmcs_cal | 376 [357-395] | 867 [836-896] | 1485 [1446-1512] | 44 [39-58] | 0.90 / 0.96 / 0.92 | 0.01 / 0.00 / 0.01 | 0.81 / 0.02 / 0.47 |
| bmcs_cal_r | 356 [334-378] | 846 [810-858] | 1457 [1434-1493] | 67 [56-83] | 0.86 / 0.96 / 0.96 | 0.01 / 0.00 / 0.01 | 0.81 / 0.01 / 0.36 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.27 | 0.00463 |
| bmcs_cal_r vs transfer | 1.00 | 8.55e-11 |
| bmcs_cal_r vs bmcs_cal | 0.31 | 0.00987 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.01 | 9.36e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 1.2 [1.2-1.3], never: 0/30
- transfer: 240.0 [240.0-240.0], never: 29/30
- bmcs_cal: 1.4 [1.2-1.9], never: 1/30
- bmcs_cal_r: 1.9 [1.7-2.3], never: 0/30

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 376 [362-393] | 872 [848-894] | 1502 [1462-1535] | 38 [26-44] | 0.94 / 1.00 / 0.98 | 0.00 / 0.00 / 0.00 | 0.88 / 0.02 / 0.78 |
| transfer | 136 [121-143] | 366 [343-380] | 636 [610-670] | 890 [881-892] | 0.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 | 0.88 / 0.03 / 0.16 |
| bmcs_cal | 361 [344-379] | 844 [816-874] | 1462 [1421-1504] | 43 [33-63] | 0.81 / 0.87 / 0.87 | 0.01 / 0.00 / 0.00 | 0.88 / 0.13 / 0.77 |
| bmcs_cal_r | 337 [315-350] | 819 [802-841] | 1423 [1410-1468] | 92 [75-115] | 0.81 / 0.97 / 0.96 | 0.01 / 0.00 / 0.00 | 0.88 / 0.06 / 0.72 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.13 | 2.29e-06 |
| bmcs_cal_r vs transfer | 1.00 | 8.57e-11 |
| bmcs_cal_r vs bmcs_cal | 0.35 | 0.0406 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.00 | 2.86e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 1.6 [1.3-1.8], never: 0/30
- transfer: 240.0 [240.0-240.0], never: 30/30
- bmcs_cal: 1.8 [1.4-2.5], never: 3/30
- bmcs_cal_r: 2.5 [2.0-3.7], never: 0/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 40 [36-50] | 122 [117-132] | 224 [212-240] | 80 [71-88] | 0.42 / 0.72 / 0.77 | 0.00 / 0.00 / 0.00 | 0.54 / 0.15 / 0.08 |
| transfer | 55 [50-62] | 137 [123-153] | 244 [226-261] | 60 [56-65] | 0.58 / 0.74 / 0.79 | 1.00 / 1.00 / 1.00 | 0.50 / 0.25 / 0.19 |
| bmcs_cal | 58 [48-62] | 130 [122-142] | 243 [218-256] | 65 [61-73] | 0.56 / 0.72 / 0.78 | 0.79 / 0.81 / 0.79 | 0.53 / 0.23 / 0.15 |
| bmcs_cal_r | 64 [48-74] | 150 [133-161] | 260 [239-277] | 38 [29-48] | 0.67 / 0.80 / 0.84 | 0.74 / 0.78 / 0.77 | 0.53 / 0.34 / 0.34 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.80 | 0.000152 |
| bmcs_cal_r vs transfer | 0.63 | 0.0822 |
| bmcs_cal_r vs bmcs_cal | 0.70 | 0.0162 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.00483 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 46 [41-52] | 124 [109-132] | 222 [203-236] | 83 [75-98] | 0.48 / 0.68 / 0.74 | 0.00 / 0.00 / 0.00 | 0.70 / 0.20 / 0.14 |
| transfer | 59 [51-66] | 138 [131-148] | 242 [230-260] | 56 [50-59] | 0.65 / 0.73 / 0.79 | 1.00 / 1.00 / 1.00 | 0.69 / 0.52 / 0.43 |
| bmcs_cal | 62 [53-66] | 136 [131-151] | 238 [228-255] | 62 [57-69] | 0.62 / 0.73 / 0.77 | 0.82 / 0.89 / 0.87 | 0.69 / 0.41 / 0.35 |
| bmcs_cal_r | 70 [63-77] | 160 [152-172] | 274 [266-288] | 26 [22-36] | 0.80 / 0.88 / 0.90 | 0.80 / 0.82 / 0.81 | 0.69 / 0.51 / 0.52 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.97 | 1.18e-09 |
| bmcs_cal_r vs transfer | 0.85 | 7.82e-06 |
| bmcs_cal_r vs bmcs_cal | 0.83 | 8.81e-06 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.79 | 0.000107 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 40 [33-55] | 106 [93-128] | 198 [180-220] | 105 [92-114] | 0.43 / 0.58 / 0.65 | 0.00 / 0.00 / 0.00 | 0.82 / 0.36 / 0.25 |
| transfer | 69 [64-78] | 147 [138-164] | 252 [236-264] | 45 [43-50] | 0.79 / 0.75 / 0.76 | 1.00 / 1.00 / 1.00 | 0.80 / 0.76 / 0.87 |
| bmcs_cal | 68 [61-74] | 148 [130-156] | 244 [232-262] | 55 [51-61] | 0.73 / 0.72 / 0.74 | 0.87 / 0.94 / 0.94 | 0.81 / 0.63 / 0.79 |
| bmcs_cal_r | 68 [58-74] | 163 [147-171] | 282 [275-289] | 22 [16-30] | 0.84 / 0.92 / 0.91 | 0.85 / 0.89 / 0.88 | 0.81 / 0.68 / 0.71 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.96 | 1.9e-09 |
| bmcs_cal_r vs transfer | 0.67 | 0.0275 |
| bmcs_cal_r vs bmcs_cal | 0.73 | 0.00451 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.91 | 5.5e-08 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 34 [31-43] | 90 [80-103] | 154 [136-176] | 151 [131-157] | 0.35 / 0.42 / 0.42 | 0.00 / 0.00 / 0.00 | 0.87 / 0.53 / 0.52 |
| transfer | 80 [72-88] | 158 [155-171] | 261 [250-279] | 37 [33-41] | 0.92 / 0.78 / 0.72 | 1.00 / 1.00 / 1.00 | 0.86 / 0.64 / 0.95 |
| bmcs_cal | 74 [66-79] | 153 [144-169] | 258 [241-274] | 44 [41-51] | 0.86 / 0.75 / 0.70 | 0.90 / 0.97 / 0.98 | 0.87 / 0.65 / 0.94 |
| bmcs_cal_r | 72 [66-80] | 166 [153-174] | 286 [277-294] | 15 [10-20] | 0.90 / 0.95 / 0.95 | 0.88 / 0.93 / 0.90 | 0.87 / 0.62 / 0.88 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 1.00 | 8.97e-11 |
| bmcs_cal_r vs transfer | 0.54 | 0.569 |
| bmcs_cal_r vs bmcs_cal | 0.66 | 0.0582 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 1.00 | 2.81e-11 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 125 [116-133] | 294 [277-311] | 510 [487-542] | 102 [77-119] | 0.38 / 0.45 / 0.48 | 0.00 / 0.00 / 0.00 | 0.24 / 0.05 / 0.04 |
| transfer | 138 [126-148] | 304 [297-314] | 526 [510-541] | 83 [69-96] | 0.45 / 0.51 / 0.53 | 1.00 / 1.00 / 1.00 | 0.24 / 0.08 / 0.06 |
| bmcs_cal | 130 [125-139] | 298 [286-320] | 520 [487-552] | 87 [75-105] | 0.44 / 0.52 / 0.54 | 0.75 / 0.78 / 0.74 | 0.25 / 0.07 / 0.05 |
| bmcs_cal_r | 128 [121-138] | 299 [283-309] | 518 [501-531] | 83 [65-97] | 0.43 / 0.52 / 0.54 | 0.72 / 0.76 / 0.73 | 0.25 / 0.08 / 0.09 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.54 | 1 |
| bmcs_cal_r vs transfer | 0.39 | 0.429 |
| bmcs_cal_r vs bmcs_cal | 0.47 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.0467 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 132 [116-139] | 297 [280-309] | 512 [495-527] | 100 [85-121] | 0.33 / 0.40 / 0.42 | 0.00 / 0.00 / 0.00 | 0.36 / 0.08 / 0.07 |
| transfer | 140 [134-149] | 316 [300-326] | 536 [515-550] | 75 [58-83] | 0.54 / 0.56 / 0.58 | 1.00 / 1.00 / 1.00 | 0.36 / 0.12 / 0.13 |
| bmcs_cal | 138 [127-151] | 313 [292-324] | 528 [510-560] | 66 [55-91] | 0.53 / 0.57 / 0.57 | 0.77 / 0.86 / 0.85 | 0.36 / 0.09 / 0.10 |
| bmcs_cal_r | 134 [127-144] | 309 [292-324] | 546 [515-566] | 77 [61-89] | 0.47 / 0.56 / 0.58 | 0.80 / 0.83 / 0.80 | 0.36 / 0.08 / 0.14 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.64 | 0.187 |
| bmcs_cal_r vs transfer | 0.44 | 0.884 |
| bmcs_cal_r vs bmcs_cal | 0.50 | 0.976 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.00622 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 133 [118-148] | 300 [283-334] | 510 [489-558] | 103 [51-116] | 0.41 / 0.49 / 0.48 | 0.00 / 0.00 / 0.00 | 0.50 / 0.15 / 0.16 |
| transfer | 158 [146-170] | 345 [326-360] | 578 [552-594] | 35 [26-57] | 0.71 / 0.69 / 0.66 | 1.00 / 1.00 / 1.00 | 0.49 / 0.06 / 0.29 |
| bmcs_cal | 148 [142-162] | 336 [315-348] | 567 [546-576] | 43 [38-63] | 0.69 / 0.67 / 0.64 | 0.75 / 0.84 / 0.94 | 0.50 / 0.08 / 0.19 |
| bmcs_cal_r | 142 [132-147] | 320 [302-338] | 548 [523-574] | 59 [51-86] | 0.55 / 0.61 / 0.63 | 0.83 / 0.89 / 0.87 | 0.50 / 0.05 / 0.17 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.63 | 0.145 |
| bmcs_cal_r vs transfer | 0.25 | 0.0027 |
| bmcs_cal_r vs bmcs_cal | 0.36 | 0.145 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.83 | 8.84e-06 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 134 [124-148] | 318 [279-334] | 530 [480-552] | 81 [57-134] | 0.43 / 0.53 / 0.44 | 0.00 / 0.00 / 0.00 | 0.67 / 0.17 / 0.51 |
| transfer | 158 [151-167] | 357 [346-367] | 596 [574-609] | 19 [17-24] | 0.94 / 0.89 / 0.75 | 1.00 / 1.00 / 1.00 | 0.66 / 0.02 / 0.15 |
| bmcs_cal | 150 [147-164] | 344 [331-362] | 578 [557-603] | 31 [22-38] | 0.85 / 0.84 / 0.71 | 0.71 / 0.62 / 0.94 | 0.67 / 0.04 / 0.23 |
| bmcs_cal_r | 152 [132-159] | 333 [316-353] | 569 [538-591] | 32 [25-43] | 0.76 / 0.80 / 0.80 | 0.88 / 0.94 / 0.93 | 0.67 / 0.02 / 0.23 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.65 | 0.0917 |
| bmcs_cal_r vs transfer | 0.22 | 0.000471 |
| bmcs_cal_r vs bmcs_cal | 0.35 | 0.0917 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.85 | 3.42e-06 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.0015 0.0035 0.003  0.004  0.0025 0.001  0.0005 0.0002]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 130 [121-146] | 296 [282-320] | 518 [490-558] | 95 [69-110] | 0.43 / 0.52 / 0.54 | 0.00 / 0.00 / 0.00 | 0.25 / 0.06 / 0.05 |
| transfer | 126 [118-135] | 289 [276-308] | 506 [488-530] | 96 [75-111] | 0.38 / 0.48 / 0.50 | 1.00 / 1.00 / 1.00 | 0.25 / 0.07 / 0.06 |
| bmcs_cal | 129 [117-141] | 302 [283-323] | 521 [500-542] | 87 [67-102] | 0.43 / 0.49 / 0.52 | 0.64 / 0.68 / 0.67 | 0.24 / 0.07 / 0.05 |
| bmcs_cal_r | 136 [112-146] | 311 [297-324] | 536 [512-553] | 74 [57-103] | 0.44 / 0.54 / 0.56 | 0.62 / 0.67 / 0.66 | 0.24 / 0.07 / 0.08 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.59 | 0.491 |
| bmcs_cal_r vs transfer | 0.66 | 0.105 |
| bmcs_cal_r vs bmcs_cal | 0.58 | 0.491 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.43 | 0.359 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 7.5 [2.9-36.9], never: 6/30
- transfer: 5.2 [2.9-22.2], never: 4/30
- bmcs_cal: 4.9 [2.3-32.5], never: 6/30
- bmcs_cal_r: 5.8 [1.8-17.1], never: 7/30

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 134 [121-142] | 301 [284-312] | 515 [498-544] | 95 [72-104] | 0.44 / 0.53 / 0.53 | 0.00 / 0.00 / 0.00 | 0.38 / 0.10 / 0.10 |
| transfer | 136 [128-144] | 306 [290-324] | 523 [496-548] | 87 [61-121] | 0.39 / 0.44 / 0.46 | 1.00 / 1.00 / 1.00 | 0.37 / 0.13 / 0.13 |
| bmcs_cal | 135 [123-149] | 302 [290-318] | 522 [503-546] | 81 [63-103] | 0.44 / 0.49 / 0.51 | 0.63 / 0.73 / 0.76 | 0.37 / 0.09 / 0.09 |
| bmcs_cal_r | 130 [119-141] | 295 [273-321] | 518 [487-547] | 90 [64-120] | 0.36 / 0.44 / 0.47 | 0.68 / 0.74 / 0.72 | 0.37 / 0.08 / 0.15 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.48 | 0.866 |
| bmcs_cal_r vs transfer | 0.41 | 0.642 |
| bmcs_cal_r vs bmcs_cal | 0.44 | 0.866 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.59 | 0.24 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 6.4 [2.4-14.2], never: 4/30
- transfer: 3.9 [1.9-240.0], never: 9/30
- bmcs_cal: 4.0 [1.9-21.8], never: 7/30
- bmcs_cal_r: 12.2 [2.6-240.0], never: 12/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 137 [125-152] | 309 [288-325] | 526 [493-566] | 84 [53-116] | 0.46 / 0.50 / 0.48 | 0.00 / 0.00 / 0.00 | 0.51 / 0.19 / 0.26 |
| transfer | 136 [125-150] | 300 [284-323] | 510 [495-546] | 97 [68-111] | 0.27 / 0.34 / 0.35 | 1.00 / 1.00 / 1.00 | 0.49 / 0.10 / 0.35 |
| bmcs_cal | 140 [130-152] | 318 [300-334] | 542 [506-560] | 88 [64-104] | 0.39 / 0.41 / 0.41 | 0.58 / 0.68 / 0.83 | 0.49 / 0.10 / 0.17 |
| bmcs_cal_r | 126 [119-135] | 301 [288-310] | 518 [503-531] | 90 [73-103] | 0.39 / 0.51 / 0.52 | 0.71 / 0.79 / 0.79 | 0.49 / 0.08 / 0.19 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.41 | 0.45 |
| bmcs_cal_r vs transfer | 0.44 | 0.45 |
| bmcs_cal_r vs bmcs_cal | 0.29 | 0.0159 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.48 | 0.756 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 6.6 [2.4-240.0], never: 11/30
- transfer: 240.0 [5.7-240.0], never: 17/30
- bmcs_cal: 128.8 [3.3-240.0], never: 15/30
- bmcs_cal_r: 12.0 [4.6-92.2], never: 7/30

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 140 [128-151] | 324 [304-349] | 536 [483-573] | 57 [48-118] | 0.54 / 0.64 / 0.52 | 0.00 / 0.00 / 0.00 | 0.65 / 0.22 / 0.76 |
| transfer | 128 [118-134] | 292 [268-302] | 490 [468-518] | 104 [98-128] | 0.04 / 0.11 / 0.16 | 1.00 / 1.00 / 1.00 | 0.63 / 0.09 / 0.24 |
| bmcs_cal | 132 [118-140] | 299 [286-319] | 506 [480-529] | 105 [74-116] | 0.30 / 0.40 / 0.35 | 0.44 / 0.36 / 0.81 | 0.65 / 0.17 / 0.42 |
| bmcs_cal_r | 116 [111-124] | 295 [265-306] | 506 [480-532] | 104 [96-123] | 0.20 / 0.36 / 0.38 | 0.61 / 0.66 / 0.70 | 0.65 / 0.11 / 0.35 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.23 | 0.00106 |
| bmcs_cal_r vs transfer | 0.53 | 0.69 |
| bmcs_cal_r vs bmcs_cal | 0.40 | 0.343 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.22 | 0.000218 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- calib: 4.8 [2.7-240.0], never: 9/30
- transfer: 240.0 [240.0-240.0], never: 26/30
- bmcs_cal: 240.0 [4.9-240.0], never: 16/30
- bmcs_cal_r: 240.0 [10.2-240.0], never: 17/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0015 0.0015 0.001  0.0005 0.0002]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 132 [115-145] | 306 [286-327] | 612 [580-648] | 300 [268-318] | 0.39 / 0.21 / 0.30 | 0.00 / 0.00 / 0.00 | 0.25 / 0.06 / 0.04 |
| transfer | 129 [117-138] | 310 [303-318] | 630 [596-671] | 281 [247-320] | 0.40 / 0.21 / 0.35 | 1.00 / 1.00 / 1.00 | 0.25 / 0.08 / 0.06 |
| bmcs_cal | 134 [127-144] | 313 [294-326] | 627 [602-658] | 278 [262-296] | 0.46 / 0.22 / 0.33 | 0.75 / 0.79 / 0.75 | 0.25 / 0.07 / 0.05 |
| bmcs_cal_r | 132 [120-143] | 310 [293-326] | 628 [594-672] | 269 [232-289] | 0.45 / 0.21 / 0.37 | 0.71 / 0.73 / 0.71 | 0.25 / 0.09 / 0.09 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.52 | 1 |
| bmcs_cal_r vs transfer | 0.47 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.47 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.54 | 0.579 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 132 [123-146] | 303 [286-332] | 646 [613-661] | 270 [253-296] | 0.42 / 0.21 / 0.35 | 0.00 / 0.00 / 0.00 | 0.37 / 0.08 / 0.07 |
| transfer | 144 [128-155] | 323 [308-338] | 628 [609-660] | 273 [254-289] | 0.53 / 0.22 / 0.31 | 1.00 / 1.00 / 1.00 | 0.36 / 0.12 / 0.12 |
| bmcs_cal | 142 [132-148] | 320 [306-334] | 632 [616-667] | 275 [247-299] | 0.49 / 0.23 / 0.34 | 0.77 / 0.85 / 0.86 | 0.38 / 0.09 / 0.10 |
| bmcs_cal_r | 133 [123-145] | 313 [305-329] | 637 [594-669] | 265 [243-314] | 0.47 / 0.22 / 0.30 | 0.80 / 0.86 / 0.84 | 0.38 / 0.09 / 0.14 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.62 | 0.307 |
| bmcs_cal_r vs transfer | 0.40 | 0.396 |
| bmcs_cal_r vs bmcs_cal | 0.45 | 0.478 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.68 | 0.018 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 140 [128-154] | 323 [304-336] | 630 [603-659] | 289 [253-311] | 0.54 / 0.23 / 0.29 | 0.00 / 0.00 / 0.00 | 0.49 / 0.12 / 0.16 |
| transfer | 153 [139-167] | 336 [316-353] | 632 [612-655] | 279 [251-300] | 0.63 / 0.23 / 0.24 | 1.00 / 1.00 / 1.00 | 0.50 / 0.09 / 0.31 |
| bmcs_cal | 142 [133-152] | 322 [313-334] | 619 [602-661] | 271 [248-301] | 0.61 / 0.23 / 0.27 | 0.69 / 0.83 / 0.94 | 0.49 / 0.10 / 0.19 |
| bmcs_cal_r | 140 [128-149] | 319 [310-333] | 628 [581-662] | 275 [251-322] | 0.50 / 0.21 / 0.27 | 0.85 / 0.91 / 0.92 | 0.49 / 0.06 / 0.19 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.49 | 1 |
| bmcs_cal_r vs transfer | 0.32 | 0.0423 |
| bmcs_cal_r vs bmcs_cal | 0.47 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.66 | 0.0345 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 138 [118-150] | 315 [293-334] | 602 [574-626] | 300 [288-319] | 0.53 / 0.19 / 0.25 | 0.00 / 0.00 / 0.00 | 0.62 / 0.15 / 0.57 |
| transfer | 162 [155-169] | 361 [339-370] | 652 [632-671] | 271 [252-282] | 0.83 / 0.25 / 0.20 | 1.00 / 1.00 / 1.00 | 0.62 / 0.05 / 0.20 |
| bmcs_cal | 155 [145-170] | 351 [326-366] | 643 [605-664] | 277 [250-289] | 0.84 / 0.26 / 0.20 | 0.76 / 0.66 / 0.94 | 0.61 / 0.05 / 0.23 |
| bmcs_cal_r | 147 [133-158] | 330 [316-351] | 604 [584-621] | 305 [291-315] | 0.67 / 0.21 / 0.13 | 0.90 / 0.94 / 0.93 | 0.61 / 0.04 / 0.22 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.67 | 0.0438 |
| bmcs_cal_r vs transfer | 0.27 | 0.00612 |
| bmcs_cal_r vs bmcs_cal | 0.37 | 0.0904 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.86 | 1.27e-06 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 1000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 102 [98-109] | 216 [206-232] | 356 [336-367] | 41 [36-52] | 0.21 / 0.25 / 0.23 | 0.00 / 0.00 / 0.00 | 0.24 / 0.06 / 0.05 |
| transfer | 108 [101-112] | 222 [211-237] | 356 [346-366] | 38 [33-51] | 0.23 / 0.26 / 0.23 | 1.00 / 1.00 / 1.00 | 0.24 / 0.09 / 0.08 |
| bmcs_cal | 106 [94-113] | 222 [207-236] | 352 [334-376] | 45 [39-52] | 0.24 / 0.28 / 0.26 | 0.70 / 0.73 / 0.68 | 0.25 / 0.08 / 0.06 |
| bmcs_cal_r | 109 [103-113] | 224 [216-239] | 364 [348-374] | 35 [27-40] | 0.27 / 0.26 / 0.21 | 0.73 / 0.74 / 0.69 | 0.25 / 0.09 / 0.11 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.64 | 0.163 |
| bmcs_cal_r vs transfer | 0.57 | 0.516 |
| bmcs_cal_r vs bmcs_cal | 0.58 | 0.516 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.58 | 0.297 |

### N = 2000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 108 [91-113] | 221 [208-232] | 356 [347-366] | 45 [36-52] | 0.22 / 0.18 / 0.19 | 0.00 / 0.00 / 0.00 | 0.36 / 0.09 / 0.08 |
| transfer | 111 [103-118] | 233 [221-243] | 366 [347-381] | 34 [26-44] | 0.29 / 0.24 / 0.22 | 1.00 / 1.00 / 1.00 | 0.35 / 0.16 / 0.15 |
| bmcs_cal | 110 [104-118] | 230 [219-242] | 363 [350-368] | 43 [32-49] | 0.26 / 0.26 / 0.23 | 0.74 / 0.83 / 0.79 | 0.35 / 0.12 / 0.12 |
| bmcs_cal_r | 110 [101-118] | 229 [221-238] | 364 [350-374] | 34 [27-46] | 0.28 / 0.30 / 0.23 | 0.77 / 0.81 / 0.75 | 0.35 / 0.11 / 0.17 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.64 | 0.21 |
| bmcs_cal_r vs transfer | 0.46 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.50 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.0427 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 110 [98-118] | 224 [209-233] | 342 [330-368] | 47 [39-66] | 0.24 / 0.18 / 0.18 | 0.00 / 0.00 / 0.00 | 0.49 / 0.18 / 0.16 |
| transfer | 118 [106-124] | 238 [224-252] | 372 [353-387] | 34 [28-49] | 0.30 / 0.20 / 0.19 | 1.00 / 1.00 / 1.00 | 0.47 / 0.15 / 0.46 |
| bmcs_cal | 110 [104-120] | 232 [221-240] | 358 [351-372] | 36 [25-50] | 0.29 / 0.20 / 0.19 | 0.67 / 0.82 / 0.89 | 0.49 / 0.14 / 0.28 |
| bmcs_cal_r | 104 [99-113] | 225 [215-234] | 359 [346-370] | 37 [27-42] | 0.30 / 0.30 / 0.24 | 0.78 / 0.83 / 0.79 | 0.49 / 0.11 / 0.30 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.55 | 0.473 |
| bmcs_cal_r vs transfer | 0.30 | 0.0271 |
| bmcs_cal_r vs bmcs_cal | 0.40 | 0.407 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00167 |

### N = 20000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV C vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| calib | 100 [92-115] | 214 [206-234] | 341 [328-352] | 55 [46-68] | 0.15 / 0.16 / 0.16 | 0.00 / 0.00 / 0.00 | 0.65 / 0.42 / 0.50 |
| transfer | 116 [94-129] | 232 [209-244] | 353 [338-370] | 36 [26-65] | 0.15 / 0.17 / 0.20 | 1.00 / 1.00 / 1.00 | 0.65 / 0.13 / 0.53 |
| bmcs_cal | 111 [92-119] | 232 [208-246] | 351 [342-373] | 37 [29-52] | 0.16 / 0.19 / 0.20 | 0.58 / 0.68 / 0.95 | 0.66 / 0.19 / 0.39 |
| bmcs_cal_r | 110 [90-120] | 228 [210-241] | 358 [330-379] | 39 [33-57] | 0.26 / 0.22 / 0.18 | 0.77 / 0.79 / 0.80 | 0.66 / 0.14 / 0.39 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs calib | 0.62 | 0.372 |
| bmcs_cal_r vs transfer | 0.47 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.48 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.63 | 0.0889 |
