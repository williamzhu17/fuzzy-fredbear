# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## no_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 353 [342-364] | 812 [792-842] | 1408 [1390-1438] | 100 [93-111] | 0.84 / 0.93 / 0.95 | 0.00 / 0.00 / 0.00 | 0.31 / 0.05 / 0.03 |
| calib | 364 [343-378] | 822 [794-859] | 1424 [1396-1454] | 82 [68-104] | 0.88 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.32 / 0.20 / 0.04 |
| transfer | 388 [364-400] | 854 [838-875] | 1459 [1443-1479] | 67 [59-76] | 0.91 / 0.94 / 0.95 | 1.00 / 1.00 / 1.00 | 0.68 / 0.37 / 0.08 |
| adaptive | 368 [353-376] | 834 [810-858] | 1444 [1415-1456] | 87 [74-96] | 0.88 / 0.94 / 0.95 | 0.78 / 0.58 / 0.51 | 0.47 / 0.14 / 0.04 |
| bmc_cal | 376 [362-392] | 849 [818-875] | 1452 [1430-1485] | 68 [60-74] | 0.91 / 0.94 / 0.95 | 0.85 / 0.86 / 0.87 | 0.55 / 0.33 / 0.07 |
| bmcs_cal | 370 [348-381] | 849 [818-868] | 1450 [1421-1481] | 70 [63-84] | 0.90 / 0.94 / 0.95 | 0.83 / 0.83 / 0.79 | 0.55 / 0.30 / 0.06 |
| bmcs_cal_r | 379 [372-401] | 871 [853-886] | 1480 [1452-1502] | 50 [38-59] | 0.93 / 0.96 / 0.97 | 0.82 / 0.81 / 0.77 | 0.55 / 0.49 / 0.23 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.73 | 0.0111 |
| bmcs_cal vs calib | 0.64 | 0.285 |
| bmcs_cal vs transfer | 0.41 | 0.434 |
| bmcs_cal vs adaptive | 0.62 | 0.372 |
| bmcs_cal vs bmc_cal | 0.47 | 0.69 |
| bmcs_cal vs bmcs_cal_r | 0.29 | 0.0237 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.87 | 4.05e-06 |
| bmcs_cal_r vs calib | 0.79 | 0.000441 |
| bmcs_cal_r vs transfer | 0.62 | 0.102 |
| bmcs_cal_r vs adaptive | 0.82 | 0.000129 |
| bmcs_cal_r vs bmc_cal | 0.66 | 0.0689 |
| bmcs_cal_r vs bmcs_cal | 0.71 | 0.0142 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.00463 |
| transfer vs fresh | 0.81 | 8.4e-05 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 343 [335-360] | 817 [795-834] | 1414 [1386-1446] | 103 [97-120] | 0.83 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.76 / 0.08 / 0.06 |
| calib | 394 [370-404] | 892 [860-912] | 1497 [1469-1523] | 34 [30-46] | 0.93 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 | 0.73 / 0.80 / 0.93 |
| transfer | 409 [395-420] | 892 [874-919] | 1492 [1479-1542] | 10 [10-12] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 |
| adaptive | 376 [369-392] | 846 [831-871] | 1459 [1434-1482] | 59 [57-65] | 0.93 / 0.95 / 0.96 | 0.90 / 0.65 / 0.52 | 0.86 / 0.39 / 0.09 |
| bmc_cal | 404 [391-419] | 896 [879-915] | 1509 [1482-1534] | 21 [19-23] | 1.00 / 1.00 / 0.96 | 1.00 / 1.00 / 0.62 | 0.92 / 1.00 / 1.00 |
| bmcs_cal | 406 [391-416] | 886 [876-916] | 1503 [1482-1532] | 16 [13-18] | 0.99 / 1.00 / 0.97 | 0.71 / 0.58 / 0.91 | 0.92 / 1.00 / 0.99 |
| bmcs_cal_r | 400 [377-409] | 876 [857-888] | 1486 [1463-1508] | 20 [16-28] | 0.97 / 0.99 / 0.98 | 0.96 / 0.97 / 0.95 | 0.92 / 0.95 / 0.90 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.94 | 2.73e-08 |
| bmcs_cal vs calib | 0.57 | 1 |
| bmcs_cal vs transfer | 0.51 | 1 |
| bmcs_cal vs adaptive | 0.86 | 6.88e-06 |
| bmcs_cal vs bmc_cal | 0.49 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.68 | 0.0779 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.89 | 9.17e-07 |
| bmcs_cal_r vs calib | 0.39 | 0.158 |
| bmcs_cal_r vs transfer | 0.32 | 0.0498 |
| bmcs_cal_r vs adaptive | 0.75 | 0.00427 |
| bmcs_cal_r vs bmc_cal | 0.29 | 0.0222 |
| bmcs_cal_r vs bmcs_cal | 0.32 | 0.0498 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.57 | 0.318 |
| transfer vs fresh | 0.94 | 9.1e-09 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.00000e-02 1.84552e-03 7.26612e-03 1.08729e-03 8.34084e-04 4.74313e-04
 1.19068e-04 3.83869e-05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 351 [332-359] | 804 [778-823] | 1392 [1356-1417] | 105 [91-163] | 0.74 / 0.84 / 0.86 | 0.00 / 0.00 / 0.00 | 0.34 / 0.07 / 0.03 |
| calib | 376 [358-389] | 850 [824-874] | 1455 [1404-1486] | 72 [64-86] | 0.85 / 0.90 / 0.92 | 0.00 / 0.00 / 0.00 | 0.34 / 0.22 / 0.05 |
| transfer | 384 [364-396] | 851 [828-867] | 1450 [1420-1488] | 64 [57-73] | 0.90 / 0.92 / 0.93 | 1.00 / 1.00 / 1.00 | 0.68 / 0.36 / 0.09 |
| adaptive | 366 [335-380] | 830 [796-848] | 1442 [1406-1476] | 87 [71-124] | 0.82 / 0.89 / 0.91 | 0.75 / 0.58 / 0.51 | 0.54 / 0.13 / 0.04 |
| bmc_cal | 384 [371-396] | 850 [834-874] | 1453 [1431-1486] | 68 [57-82] | 0.87 / 0.91 / 0.92 | 0.82 / 0.84 / 0.84 | 0.55 / 0.32 / 0.07 |
| bmcs_cal | 373 [347-385] | 844 [812-860] | 1448 [1419-1467] | 69 [66-88] | 0.86 / 0.90 / 0.92 | 0.82 / 0.82 / 0.78 | 0.55 / 0.30 / 0.07 |
| bmcs_cal_r | 369 [354-396] | 852 [828-863] | 1462 [1428-1479] | 61 [38-89] | 0.86 / 0.92 / 0.92 | 0.81 / 0.79 / 0.75 | 0.55 / 0.44 / 0.22 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.77 | 0.00238 |
| bmcs_cal vs calib | 0.42 | 0.686 |
| bmcs_cal vs transfer | 0.39 | 0.686 |
| bmcs_cal vs adaptive | 0.59 | 0.686 |
| bmcs_cal vs bmc_cal | 0.39 | 0.686 |
| bmcs_cal vs bmcs_cal_r | 0.42 | 0.686 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.83 | 6.98e-05 |
| bmcs_cal_r vs calib | 0.49 | 1 |
| bmcs_cal_r vs transfer | 0.46 | 1 |
| bmcs_cal_r vs adaptive | 0.67 | 0.138 |
| bmcs_cal_r vs bmc_cal | 0.46 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.58 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.53 | 0.701 |
| transfer vs fresh | 0.87 | 1.3e-06 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 356 [339-371] | 812 [805-838] | 1426 [1409-1440] | 111 [98-133] | 0.78 / 0.87 / 0.89 | 0.00 / 0.00 / 0.00 | 0.80 / 0.12 / 0.10 |
| calib | 382 [356-400] | 866 [840-889] | 1488 [1403-1500] | 42 [34-57] | 0.74 / 0.77 / 0.75 | 0.00 / 0.00 / 0.00 | 0.80 / 0.82 / 0.90 |
| transfer | 396 [382-413] | 898 [871-921] | 1511 [1483-1540] | 10 [8-11] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 |
| adaptive | 383 [369-403] | 866 [843-886] | 1470 [1450-1486] | 59 [53-67] | 0.93 / 0.94 / 0.95 | 0.90 / 0.66 / 0.52 | 0.91 / 0.46 / 0.12 |
| bmc_cal | 406 [392-418] | 901 [876-910] | 1498 [1471-1518] | 21 [19-23] | 1.00 / 1.00 / 0.96 | 1.00 / 1.00 / 0.58 | 0.93 / 1.00 / 1.00 |
| bmcs_cal | 405 [392-423] | 900 [880-912] | 1522 [1484-1547] | 16 [13-17] | 0.99 / 1.00 / 0.97 | 0.71 / 0.61 / 0.92 | 0.93 / 1.00 / 1.00 |
| bmcs_cal_r | 392 [377-405] | 884 [865-898] | 1498 [1476-1533] | 19 [15-23] | 0.97 / 0.99 / 0.99 | 0.96 / 0.97 / 0.95 | 0.93 / 0.96 / 0.91 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.98 | 9.17e-10 |
| bmcs_cal vs calib | 0.76 | 0.0021 |
| bmcs_cal vs transfer | 0.51 | 1 |
| bmcs_cal vs adaptive | 0.82 | 0.000117 |
| bmcs_cal vs bmc_cal | 0.52 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.69 | 0.0343 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.93 | 8.91e-08 |
| bmcs_cal_r vs calib | 0.64 | 0.155 |
| bmcs_cal_r vs transfer | 0.36 | 0.155 |
| bmcs_cal_r vs adaptive | 0.66 | 0.138 |
| bmcs_cal_r vs bmc_cal | 0.35 | 0.155 |
| bmcs_cal_r vs bmcs_cal | 0.31 | 0.0572 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00159 |
| transfer vs fresh | 0.97 | 9.18e-10 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.0002 0.005  0.003  0.002  0.001  0.0005 0.01   0.0001]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 348 [334-363] | 822 [797-846] | 1429 [1398-1454] | 105 [96-125] | 0.83 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.35 / 0.05 / 0.03 |
| calib | 365 [350-378] | 830 [801-852] | 1441 [1406-1455] | 82 [69-98] | 0.89 / 0.94 / 0.95 | 0.00 / 0.00 / 0.00 | 0.34 / 0.18 / 0.04 |
| transfer | 356 [339-374] | 821 [797-838] | 1432 [1410-1466] | 84 [74-108] | 0.86 / 0.93 / 0.94 | 1.00 / 1.00 / 1.00 | 0.60 / 0.24 / 0.06 |
| adaptive | 350 [334-366] | 819 [791-833] | 1416 [1382-1448] | 95 [88-119] | 0.85 / 0.93 / 0.94 | 0.61 / 0.54 / 0.51 | 0.46 / 0.09 / 0.03 |
| bmc_cal | 367 [342-380] | 834 [804-849] | 1432 [1415-1470] | 81 [77-98] | 0.88 / 0.94 / 0.94 | 0.29 / 0.27 / 0.27 | 0.46 / 0.19 / 0.04 |
| bmcs_cal | 366 [356-377] | 834 [816-858] | 1427 [1405-1444] | 79 [70-91] | 0.90 / 0.94 / 0.95 | 0.30 / 0.34 / 0.37 | 0.46 / 0.19 / 0.04 |
| bmcs_cal_r | 374 [347-388] | 842 [818-881] | 1465 [1430-1500] | 59 [45-89] | 0.87 / 0.93 / 0.93 | 0.32 / 0.36 / 0.38 | 0.46 / 0.34 / 0.16 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.60 | 0.632 |
| bmcs_cal vs calib | 0.54 | 1 |
| bmcs_cal vs transfer | 0.63 | 0.405 |
| bmcs_cal vs adaptive | 0.65 | 0.316 |
| bmcs_cal vs bmc_cal | 0.55 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.39 | 0.632 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.70 | 0.0325 |
| bmcs_cal_r vs calib | 0.64 | 0.135 |
| bmcs_cal_r vs transfer | 0.72 | 0.0183 |
| bmcs_cal_r vs adaptive | 0.73 | 0.0142 |
| bmcs_cal_r vs bmc_cal | 0.65 | 0.135 |
| bmcs_cal_r vs bmcs_cal | 0.61 | 0.158 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.41 | 0.485 |
| transfer vs fresh | 0.48 | 0.751 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 1.7 [1.5-2.0], never: 0/30
- calib: 1.3 [1.2-1.6], never: 0/30
- transfer: 1.4 [1.2-2.2], never: 0/30
- adaptive: 1.5 [1.2-1.8], never: 0/30
- bmc_cal: 1.4 [1.2-1.8], never: 0/30
- bmcs_cal: 1.3 [1.2-1.6], never: 0/30
- bmcs_cal_r: 1.2 [1.2-1.9], never: 1/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 342 [328-358] | 810 [786-831] | 1418 [1401-1440] | 112 [96-119] | 0.83 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.83 / 0.08 / 0.29 |
| calib | 384 [373-398] | 882 [846-894] | 1466 [1446-1502] | 41 [31-48] | 0.91 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 | 0.83 / 0.74 / 0.82 |
| transfer | 178 [168-189] | 419 [392-432] | 712 [697-735] | 813 [807-817] | 0.00 / 0.00 / 0.02 | 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 0.99 |
| adaptive | 360 [344-366] | 821 [803-827] | 1405 [1384-1422] | 111 [98-124] | 0.83 / 0.93 / 0.93 | 0.42 / 0.57 / 0.50 | 0.90 / 0.14 / 0.10 |
| bmc_cal | 382 [367-394] | 876 [859-890] | 1482 [1465-1498] | 43 [36-50] | 0.89 / 0.95 / 0.92 | 0.03 / 0.00 / 0.00 | 0.92 / 0.82 / 0.88 |
| bmcs_cal | 380 [370-395] | 870 [844-894] | 1476 [1431-1511] | 55 [43-61] | 0.93 / 0.99 / 0.94 | 0.01 / 0.00 / 0.01 | 0.92 / 0.69 / 0.88 |
| bmcs_cal_r | 354 [336-364] | 822 [816-848] | 1434 [1404-1458] | 69 [54-95] | 0.88 / 0.97 / 0.96 | 0.01 / 0.00 / 0.00 | 0.92 / 0.39 / 0.48 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.87 | 3.13e-06 |
| bmcs_cal vs calib | 0.47 | 1 |
| bmcs_cal vs transfer | 1.00 | 1.72e-10 |
| bmcs_cal vs adaptive | 0.86 | 8.26e-06 |
| bmcs_cal vs bmc_cal | 0.45 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.77 | 0.000979 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.71 | 0.0124 |
| bmcs_cal_r vs calib | 0.24 | 0.00201 |
| bmcs_cal_r vs transfer | 1.00 | 1.71e-10 |
| bmcs_cal_r vs adaptive | 0.61 | 0.131 |
| bmcs_cal_r vs bmc_cal | 0.20 | 0.000246 |
| bmcs_cal_r vs bmcs_cal | 0.23 | 0.00131 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.01 | 6.35e-11 |
| transfer vs fresh | 0.00 | 5.72e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 1.6 [1.4-2.1], never: 0/30
- calib: 1.3 [1.2-1.5], never: 0/30
- transfer: 240.0 [240.0-240.0], never: 29/30
- adaptive: 1.7 [1.5-2.2], never: 0/30
- bmc_cal: 1.3 [1.2-1.6], never: 0/30
- bmcs_cal: 1.6 [1.3-1.8], never: 0/30
- bmcs_cal_r: 1.9 [1.6-2.4], never: 0/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 52 [44-61] | 133 [125-146] | 243 [228-259] | 65 [59-74] | 0.53 / 0.76 / 0.81 | 0.00 / 0.00 / 0.00 | 0.35 / 0.05 / 0.05 |
| calib | 43 [39-50] | 125 [112-129] | 230 [220-241] | 78 [70-83] | 0.45 / 0.71 / 0.77 | 0.00 / 0.00 / 0.00 | 0.36 / 0.06 / 0.04 |
| transfer | 54 [48-63] | 135 [120-146] | 240 [223-258] | 66 [58-78] | 0.54 / 0.73 / 0.78 | 1.00 / 1.00 / 1.00 | 0.61 / 0.08 / 0.04 |
| adaptive | 52 [40-57] | 128 [120-137] | 236 [224-244] | 72 [60-78] | 0.51 / 0.74 / 0.79 | 0.61 / 0.50 / 0.50 | 0.52 / 0.07 / 0.04 |
| bmc_cal | 47 [42-55] | 131 [117-140] | 235 [224-252] | 65 [61-70] | 0.53 / 0.76 / 0.81 | 0.71 / 0.81 / 0.82 | 0.51 / 0.06 / 0.04 |
| bmcs_cal | 48 [41-56] | 127 [116-138] | 233 [221-248] | 70 [65-77] | 0.49 / 0.73 / 0.78 | 0.72 / 0.74 / 0.72 | 0.51 / 0.07 / 0.04 |
| bmcs_cal_r | 64 [59-70] | 151 [142-160] | 266 [251-280] | 31 [26-46] | 0.73 / 0.86 / 0.88 | 0.69 / 0.71 / 0.71 | 0.51 / 0.18 / 0.11 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.39 | 0.64 |
| bmcs_cal vs calib | 0.60 | 0.64 |
| bmcs_cal vs transfer | 0.37 | 0.466 |
| bmcs_cal vs adaptive | 0.49 | 1 |
| bmcs_cal vs bmc_cal | 0.48 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.14 | 8.55e-06 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.78 | 0.000355 |
| bmcs_cal_r vs calib | 0.91 | 2.07e-07 |
| bmcs_cal_r vs transfer | 0.76 | 0.000456 |
| bmcs_cal_r vs adaptive | 0.87 | 4.73e-06 |
| bmcs_cal_r vs bmc_cal | 0.85 | 8.87e-06 |
| bmcs_cal_r vs bmcs_cal | 0.86 | 5.7e-06 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.0101 |
| transfer vs fresh | 0.52 | 0.836 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 46 [42-52] | 128 [115-136] | 235 [220-248] | 68 [63-76] | 0.50 / 0.77 / 0.82 | 0.00 / 0.00 / 0.00 | 0.83 / 0.21 / 0.39 |
| calib | 38 [35-44] | 103 [94-114] | 195 [178-208] | 111 [103-123] | 0.37 / 0.55 / 0.62 | 0.00 / 0.00 / 0.00 | 0.85 / 0.22 / 0.14 |
| transfer | 72 [67-77] | 154 [144-162] | 257 [238-270] | 47 [42-49] | 0.79 / 0.74 / 0.77 | 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.61 |
| adaptive | 64 [54-73] | 146 [130-155] | 246 [235-264] | 57 [54-60] | 0.69 / 0.74 / 0.78 | 0.77 / 0.55 / 0.49 | 0.93 / 0.43 / 0.19 |
| bmc_cal | 52 [41-58] | 119 [105-130] | 216 [198-221] | 91 [83-101] | 0.53 / 0.61 / 0.67 | 0.32 / 0.20 / 0.18 | 0.93 / 0.19 / 0.15 |
| bmcs_cal | 68 [58-72] | 147 [136-155] | 245 [238-264] | 55 [50-62] | 0.73 / 0.73 / 0.74 | 0.87 / 0.95 / 0.94 | 0.93 / 0.73 / 0.24 |
| bmcs_cal_r | 72 [64-78] | 162 [149-174] | 275 [264-292] | 21 [16-29] | 0.85 / 0.91 / 0.91 | 0.84 / 0.87 / 0.84 | 0.93 / 0.78 / 0.69 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.78 | 0.000751 |
| bmcs_cal vs calib | 0.97 | 2.15e-09 |
| bmcs_cal vs transfer | 0.35 | 0.0885 |
| bmcs_cal vs adaptive | 0.53 | 0.673 |
| bmcs_cal vs bmc_cal | 0.89 | 1.49e-06 |
| bmcs_cal vs bmcs_cal_r | 0.22 | 0.000751 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.94 | 2.7e-08 |
| bmcs_cal_r vs calib | 1.00 | 1.7e-10 |
| bmcs_cal_r vs transfer | 0.65 | 0.0536 |
| bmcs_cal_r vs adaptive | 0.77 | 0.000563 |
| bmcs_cal_r vs bmc_cal | 0.98 | 1.23e-09 |
| bmcs_cal_r vs bmcs_cal | 0.78 | 0.000563 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.99 | 1.61e-10 |
| transfer vs fresh | 0.86 | 1.37e-06 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 126 [117-134] | 296 [275-308] | 516 [485-528] | 103 [90-117] | 0.34 / 0.45 / 0.49 | 0.00 / 0.00 / 0.00 | 0.18 / 0.06 / 0.04 |
| calib | 128 [122-138] | 300 [281-307] | 511 [490-528] | 94 [79-115] | 0.42 / 0.51 / 0.53 | 0.00 / 0.00 / 0.00 | 0.19 / 0.09 / 0.03 |
| transfer | 132 [122-139] | 300 [286-309] | 516 [488-537] | 91 [80-107] | 0.42 / 0.52 / 0.55 | 1.00 / 1.00 / 1.00 | 0.44 / 0.10 / 0.04 |
| adaptive | 127 [116-136] | 290 [276-320] | 521 [498-542] | 95 [80-116] | 0.40 / 0.49 / 0.52 | 0.57 / 0.53 / 0.50 | 0.30 / 0.08 / 0.04 |
| bmc_cal | 127 [120-137] | 291 [275-304] | 508 [486-525] | 97 [79-117] | 0.39 / 0.47 / 0.49 | 0.68 / 0.71 / 0.71 | 0.28 / 0.09 / 0.04 |
| bmcs_cal | 128 [123-134] | 294 [280-304] | 517 [494-534] | 98 [84-115] | 0.39 / 0.46 / 0.50 | 0.66 / 0.68 / 0.64 | 0.28 / 0.09 / 0.04 |
| bmcs_cal_r | 134 [123-142] | 304 [290-324] | 526 [505-554] | 83 [64-100] | 0.43 / 0.53 / 0.55 | 0.64 / 0.66 / 0.64 | 0.28 / 0.15 / 0.07 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.48 | 1 |
| bmcs_cal vs calib | 0.42 | 1 |
| bmcs_cal vs transfer | 0.42 | 1 |
| bmcs_cal vs adaptive | 0.46 | 1 |
| bmcs_cal vs bmc_cal | 0.51 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.34 | 0.171 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.64 | 0.253 |
| bmcs_cal_r vs calib | 0.59 | 0.485 |
| bmcs_cal_r vs transfer | 0.59 | 0.485 |
| bmcs_cal_r vs adaptive | 0.61 | 0.473 |
| bmcs_cal_r vs bmc_cal | 0.66 | 0.192 |
| bmcs_cal_r vs bmcs_cal | 0.66 | 0.171 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.51 | 0.848 |
| transfer vs fresh | 0.56 | 0.815 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 120 [111-133] | 285 [265-309] | 506 [486-521] | 103 [91-116] | 0.35 / 0.46 / 0.49 | 0.00 / 0.00 / 0.00 | 0.52 / 0.21 / 0.10 |
| calib | 134 [123-144] | 306 [278-334] | 524 [488-560] | 82 [53-109] | 0.49 / 0.53 / 0.52 | 0.00 / 0.00 / 0.00 | 0.53 / 0.64 / 0.17 |
| transfer | 148 [139-156] | 325 [312-354] | 552 [532-574] | 44 [32-62] | 0.63 / 0.62 / 0.60 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.91 |
| adaptive | 138 [128-150] | 317 [297-323] | 540 [526-562] | 68 [54-87] | 0.57 / 0.61 / 0.62 | 0.74 / 0.57 / 0.50 | 0.73 / 0.46 / 0.13 |
| bmc_cal | 145 [138-160] | 328 [314-348] | 553 [533-570] | 48 [36-67] | 0.64 / 0.63 / 0.61 | 0.96 / 0.91 / 0.83 | 0.67 / 0.97 / 0.55 |
| bmcs_cal | 148 [139-161] | 335 [315-346] | 569 [529-589] | 44 [34-64] | 0.66 / 0.65 / 0.63 | 0.73 / 0.82 / 0.93 | 0.67 / 0.92 / 0.52 |
| bmcs_cal_r | 146 [135-152] | 320 [308-332] | 547 [530-564] | 60 [51-75] | 0.50 / 0.56 / 0.56 | 0.86 / 0.92 / 0.91 | 0.67 / 0.70 / 0.46 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.91 | 3.74e-07 |
| bmcs_cal vs calib | 0.72 | 0.013 |
| bmcs_cal vs transfer | 0.49 | 1 |
| bmcs_cal vs adaptive | 0.75 | 0.00394 |
| bmcs_cal vs bmc_cal | 0.52 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.67 | 0.0724 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.86 | 1.11e-05 |
| bmcs_cal_r vs calib | 0.62 | 0.248 |
| bmcs_cal_r vs transfer | 0.36 | 0.204 |
| bmcs_cal_r vs adaptive | 0.61 | 0.248 |
| bmcs_cal_r vs bmc_cal | 0.35 | 0.204 |
| bmcs_cal_r vs bmcs_cal | 0.33 | 0.121 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00163 |
| transfer vs fresh | 0.91 | 7.86e-08 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.0015 0.0035 0.003  0.004  0.0025 0.001  0.0005 0.0002]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 124 [115-138] | 296 [279-312] | 514 [488-529] | 103 [87-119] | 0.36 / 0.48 / 0.50 | 0.00 / 0.00 / 0.00 | 0.21 / 0.06 / 0.04 |
| calib | 121 [112-130] | 286 [268-295] | 498 [476-516] | 107 [85-133] | 0.32 / 0.41 / 0.44 | 0.00 / 0.00 / 0.00 | 0.18 / 0.08 / 0.04 |
| transfer | 130 [118-138] | 290 [276-316] | 520 [492-538] | 92 [76-111] | 0.45 / 0.52 / 0.55 | 1.00 / 1.00 / 1.00 | 0.44 / 0.09 / 0.04 |
| adaptive | 122 [111-131] | 286 [276-303] | 508 [490-519] | 110 [99-120] | 0.28 / 0.39 / 0.41 | 0.56 / 0.52 / 0.51 | 0.34 / 0.07 / 0.04 |
| bmc_cal | 121 [117-132] | 299 [281-308] | 505 [487-538] | 98 [82-115] | 0.37 / 0.47 / 0.48 | 0.60 / 0.64 / 0.64 | 0.32 / 0.08 / 0.04 |
| bmcs_cal | 130 [123-140] | 304 [283-317] | 523 [507-549] | 94 [83-108] | 0.38 / 0.46 / 0.48 | 0.59 / 0.62 / 0.60 | 0.32 / 0.08 / 0.04 |
| bmcs_cal_r | 132 [120-143] | 305 [290-320] | 520 [508-560] | 85 [55-102] | 0.44 / 0.51 / 0.53 | 0.57 / 0.61 / 0.60 | 0.32 / 0.14 / 0.07 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.58 | 1 |
| bmcs_cal vs calib | 0.71 | 0.0304 |
| bmcs_cal vs transfer | 0.58 | 1 |
| bmcs_cal vs adaptive | 0.66 | 0.146 |
| bmcs_cal vs bmc_cal | 0.58 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.48 | 1 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.61 | 0.589 |
| bmcs_cal_r vs calib | 0.73 | 0.0108 |
| bmcs_cal_r vs transfer | 0.60 | 0.589 |
| bmcs_cal_r vs adaptive | 0.69 | 0.0504 |
| bmcs_cal_r vs bmc_cal | 0.61 | 0.589 |
| bmcs_cal_r vs bmcs_cal | 0.52 | 0.802 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.61 | 0.255 |
| transfer vs fresh | 0.49 | 0.877 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 11.0 [4.0-27.1], never: 5/30
- calib: 28.5 [3.1-240.0], never: 12/30
- transfer: 4.9 [2.5-9.9], never: 4/30
- adaptive: 19.0 [7.1-240.0], never: 9/30
- bmc_cal: 8.5 [3.7-240.0], never: 9/30
- bmcs_cal: 6.7 [3.5-47.6], never: 7/30
- bmcs_cal_r: 4.2 [1.6-22.7], never: 6/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 127 [116-133] | 288 [272-303] | 507 [490-521] | 98 [87-112] | 0.38 / 0.48 / 0.50 | 0.00 / 0.00 / 0.00 | 0.53 / 0.21 / 0.18 |
| calib | 141 [132-150] | 318 [287-328] | 526 [494-559] | 71 [53-102] | 0.53 / 0.58 / 0.56 | 0.00 / 0.00 / 0.00 | 0.52 / 0.55 / 0.26 |
| transfer | 132 [120-144] | 302 [290-314] | 514 [482-528] | 102 [85-122] | 0.26 / 0.32 / 0.33 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.87 |
| adaptive | 129 [120-137] | 294 [278-310] | 501 [481-531] | 99 [79-119] | 0.37 / 0.45 / 0.47 | 0.62 / 0.55 / 0.49 | 0.76 / 0.33 / 0.13 |
| bmc_cal | 132 [120-144] | 306 [285-313] | 510 [487-548] | 103 [77-117] | 0.30 / 0.42 / 0.40 | 0.86 / 0.73 / 0.66 | 0.76 / 0.86 / 0.27 |
| bmcs_cal | 137 [125-150] | 308 [292-319] | 510 [498-537] | 92 [69-115] | 0.39 / 0.43 / 0.43 | 0.52 / 0.64 / 0.79 | 0.76 / 0.79 / 0.29 |
| bmcs_cal_r | 120 [111-130] | 290 [273-306] | 510 [484-523] | 99 [72-131] | 0.32 / 0.43 / 0.45 | 0.61 / 0.71 / 0.73 | 0.76 / 0.49 / 0.29 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.71 | 0.029 |
| bmcs_cal vs calib | 0.47 | 1 |
| bmcs_cal vs transfer | 0.57 | 1 |
| bmcs_cal vs adaptive | 0.67 | 0.0842 |
| bmcs_cal vs bmc_cal | 0.57 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.71 | 0.029 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.50 | 1 |
| bmcs_cal_r vs calib | 0.28 | 0.02 |
| bmcs_cal_r vs transfer | 0.34 | 0.146 |
| bmcs_cal_r vs adaptive | 0.46 | 1 |
| bmcs_cal_r vs bmc_cal | 0.35 | 0.146 |
| bmcs_cal_r vs bmcs_cal | 0.29 | 0.0271 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.40 | 0.183 |
| transfer vs fresh | 0.66 | 0.0755 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 6.7 [4.4-23.9], never: 5/30
- calib: 4.5 [2.2-13.2], never: 7/30
- transfer: 240.0 [7.6-240.0], never: 17/30
- adaptive: 14.0 [3.9-240.0], never: 10/30
- bmc_cal: 22.5 [5.2-240.0], never: 9/30
- bmcs_cal: 7.3 [3.3-240.0], never: 11/30
- bmcs_cal_r: 9.5 [4.8-240.0], never: 13/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0015 0.0015 0.001  0.0005 0.0002]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 125 [116-134] | 294 [284-311] | 642 [590-666] | 274 [252-312] | 0.39 / 0.20 / 0.36 | 0.00 / 0.00 / 0.00 | 0.19 / 0.07 / 0.04 |
| calib | 128 [115-136] | 302 [294-318] | 630 [604-656] | 274 [256-302] | 0.41 / 0.22 / 0.36 | 0.00 / 0.00 / 0.00 | 0.18 / 0.08 / 0.04 |
| transfer | 128 [115-136] | 303 [290-316] | 626 [592-658] | 273 [248-306] | 0.41 / 0.23 / 0.35 | 1.00 / 1.00 / 1.00 | 0.43 / 0.10 / 0.04 |
| adaptive | 123 [105-130] | 288 [270-311] | 634 [607-667] | 267 [233-287] | 0.35 / 0.22 / 0.43 | 0.60 / 0.51 / 0.50 | 0.32 / 0.09 / 0.04 |
| bmc_cal | 120 [110-131] | 296 [283-309] | 628 [602-674] | 264 [230-298] | 0.40 / 0.24 / 0.40 | 0.66 / 0.70 / 0.71 | 0.27 / 0.09 / 0.04 |
| bmcs_cal | 126 [118-134] | 306 [285-322] | 640 [596-668] | 270 [246-290] | 0.39 / 0.23 / 0.39 | 0.64 / 0.66 / 0.64 | 0.27 / 0.09 / 0.04 |
| bmcs_cal_r | 130 [121-140] | 309 [296-327] | 613 [587-676] | 285 [240-312] | 0.41 / 0.21 / 0.34 | 0.63 / 0.66 / 0.65 | 0.27 / 0.15 / 0.06 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.58 | 1 |
| bmcs_cal vs calib | 0.54 | 1 |
| bmcs_cal vs transfer | 0.50 | 1 |
| bmcs_cal vs adaptive | 0.64 | 0.381 |
| bmcs_cal vs bmc_cal | 0.60 | 0.823 |
| bmcs_cal vs bmcs_cal_r | 0.43 | 1 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.64 | 0.241 |
| bmcs_cal_r vs calib | 0.59 | 0.728 |
| bmcs_cal_r vs transfer | 0.57 | 0.728 |
| bmcs_cal_r vs adaptive | 0.69 | 0.0811 |
| bmcs_cal_r vs bmc_cal | 0.66 | 0.163 |
| bmcs_cal_r vs bmcs_cal | 0.56 | 0.728 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.52 | 0.83 |
| transfer vs fresh | 0.60 | 0.347 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 124 [114-134] | 300 [281-318] | 648 [624-683] | 262 [243-287] | 0.35 / 0.23 / 0.42 | 0.00 / 0.00 / 0.00 | 0.54 / 0.22 / 0.13 |
| calib | 136 [129-142] | 308 [296-322] | 611 [588-648] | 291 [264-306] | 0.44 / 0.21 / 0.30 | 0.00 / 0.00 / 0.00 | 0.54 / 0.66 / 0.20 |
| transfer | 152 [142-167] | 332 [318-352] | 644 [606-671] | 260 [246-288] | 0.56 / 0.21 / 0.27 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.92 |
| adaptive | 138 [129-149] | 314 [300-330] | 639 [616-675] | 281 [232-300] | 0.52 / 0.23 / 0.32 | 0.74 / 0.58 / 0.50 | 0.80 / 0.44 / 0.15 |
| bmc_cal | 147 [139-158] | 329 [317-352] | 642 [624-671] | 269 [252-287] | 0.57 / 0.22 / 0.28 | 0.95 / 0.89 / 0.84 | 0.70 / 0.96 / 0.57 |
| bmcs_cal | 142 [139-154] | 334 [312-352] | 640 [607-677] | 264 [243-301] | 0.50 / 0.22 / 0.30 | 0.68 / 0.80 / 0.93 | 0.70 / 0.89 / 0.51 |
| bmcs_cal_r | 138 [127-148] | 320 [306-331] | 630 [584-654] | 276 [243-319] | 0.50 / 0.21 / 0.26 | 0.83 / 0.89 / 0.90 | 0.70 / 0.68 / 0.44 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.79 | 0.000585 |
| bmcs_cal vs calib | 0.73 | 0.0088 |
| bmcs_cal vs transfer | 0.47 | 1 |
| bmcs_cal vs adaptive | 0.68 | 0.0748 |
| bmcs_cal vs bmc_cal | 0.49 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.64 | 0.161 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.70 | 0.0543 |
| bmcs_cal_r vs calib | 0.63 | 0.178 |
| bmcs_cal_r vs transfer | 0.31 | 0.0596 |
| bmcs_cal_r vs adaptive | 0.54 | 0.554 |
| bmcs_cal_r vs bmc_cal | 0.33 | 0.0842 |
| bmcs_cal_r vs bmcs_cal | 0.36 | 0.161 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.79 | 0.000132 |
| transfer vs fresh | 0.82 | 3.59e-05 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 101 [90-111] | 215 [208-234] | 352 [342-364] | 43 [39-52] | 0.23 / 0.27 / 0.25 | 0.00 / 0.00 / 0.00 | 0.18 / 0.06 / 0.04 |
| calib | 106 [97-112] | 216 [206-230] | 354 [344-370] | 44 [34-50] | 0.25 / 0.25 / 0.21 | 0.00 / 0.00 / 0.00 | 0.18 / 0.07 / 0.04 |
| transfer | 104 [98-109] | 224 [217-233] | 360 [343-372] | 43 [34-49] | 0.26 / 0.29 / 0.23 | 1.00 / 1.00 / 1.00 | 0.40 / 0.10 / 0.04 |
| adaptive | 104 [100-112] | 221 [207-229] | 351 [335-364] | 47 [40-57] | 0.26 / 0.24 / 0.21 | 0.56 / 0.52 / 0.50 | 0.26 / 0.07 / 0.04 |
| bmc_cal | 104 [96-111] | 218 [208-226] | 348 [339-365] | 41 [34-54] | 0.24 / 0.24 / 0.22 | 0.65 / 0.69 / 0.68 | 0.24 / 0.08 / 0.04 |
| bmcs_cal | 102 [92-112] | 224 [212-230] | 351 [336-367] | 43 [37-47] | 0.29 / 0.24 / 0.21 | 0.64 / 0.65 / 0.61 | 0.24 / 0.08 / 0.04 |
| bmcs_cal_r | 108 [98-113] | 228 [218-236] | 362 [348-370] | 34 [28-47] | 0.24 / 0.26 / 0.22 | 0.63 / 0.63 / 0.61 | 0.24 / 0.12 / 0.05 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.56 | 1 |
| bmcs_cal vs calib | 0.56 | 1 |
| bmcs_cal vs transfer | 0.45 | 1 |
| bmcs_cal vs adaptive | 0.54 | 1 |
| bmcs_cal vs bmc_cal | 0.57 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.39 | 0.81 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.65 | 0.151 |
| bmcs_cal_r vs calib | 0.66 | 0.151 |
| bmcs_cal_r vs transfer | 0.55 | 0.496 |
| bmcs_cal_r vs adaptive | 0.66 | 0.151 |
| bmcs_cal_r vs bmc_cal | 0.68 | 0.103 |
| bmcs_cal_r vs bmcs_cal | 0.61 | 0.27 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.61 | 0.244 |
| transfer vs fresh | 0.62 | 0.244 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 104 [96-109] | 217 [208-228] | 352 [336-360] | 43 [35-52] | 0.24 / 0.28 / 0.24 | 0.00 / 0.00 / 0.00 | 0.51 / 0.22 / 0.16 |
| calib | 100 [92-108] | 218 [204-227] | 343 [335-357] | 54 [42-68] | 0.21 / 0.22 / 0.18 | 0.00 / 0.00 / 0.00 | 0.51 / 0.43 / 0.17 |
| transfer | 108 [101-113] | 230 [210-236] | 351 [339-369] | 40 [30-49] | 0.35 / 0.24 / 0.20 | 1.00 / 1.00 / 1.00 | 0.97 / 0.99 / 0.59 |
| adaptive | 106 [97-118] | 225 [208-238] | 361 [345-374] | 43 [38-53] | 0.31 / 0.28 / 0.23 | 0.65 / 0.54 / 0.49 | 0.69 / 0.34 / 0.15 |
| bmc_cal | 108 [101-118] | 228 [214-236] | 353 [343-364] | 46 [37-53] | 0.32 / 0.22 / 0.20 | 0.93 / 0.79 / 0.72 | 0.61 / 0.91 / 0.21 |
| bmcs_cal | 109 [104-118] | 224 [216-230] | 352 [340-365] | 42 [34-48] | 0.34 / 0.23 / 0.21 | 0.65 / 0.83 / 0.89 | 0.61 / 0.76 / 0.25 |
| bmcs_cal_r | 110 [100-116] | 223 [211-234] | 356 [341-364] | 43 [36-50] | 0.36 / 0.26 / 0.20 | 0.78 / 0.83 / 0.82 | 0.61 / 0.59 / 0.32 |

bmcs_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal vs fresh | 0.62 | 0.585 |
| bmcs_cal vs calib | 0.62 | 0.585 |
| bmcs_cal vs transfer | 0.47 | 1 |
| bmcs_cal vs adaptive | 0.51 | 1 |
| bmcs_cal vs bmc_cal | 0.45 | 1 |
| bmcs_cal vs bmcs_cal_r | 0.51 | 1 |

bmcs_cal_r vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmcs_cal_r > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmcs_cal_r vs fresh | 0.60 | 0.856 |
| bmcs_cal_r vs calib | 0.61 | 0.8 |
| bmcs_cal_r vs transfer | 0.47 | 1 |
| bmcs_cal_r vs adaptive | 0.50 | 1 |
| bmcs_cal_r vs bmc_cal | 0.46 | 1 |
| bmcs_cal_r vs bmcs_cal | 0.49 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.0916 |
| transfer vs fresh | 0.64 | 0.0916 |
