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
| shuffled | 364 [350-377] | 836 [814-855] | 1441 [1402-1478] | 74 [69-86] | 0.90 / 0.94 / 0.95 | 0.00 / 0.00 / 0.00 | 0.48 / 0.28 / 0.06 |
| transfer | 388 [364-400] | 854 [838-875] | 1459 [1443-1479] | 67 [59-76] | 0.91 / 0.94 / 0.95 | 1.00 / 1.00 / 1.00 | 0.68 / 0.37 / 0.08 |
| adaptive | 368 [353-376] | 834 [810-858] | 1444 [1415-1456] | 87 [74-96] | 0.88 / 0.94 / 0.95 | 0.78 / 0.58 / 0.51 | 0.47 / 0.14 / 0.04 |
| mix50 | 358 [346-376] | 822 [804-846] | 1436 [1418-1459] | 94 [81-105] | 0.86 / 0.94 / 0.95 | 0.50 / 0.50 / 0.50 | 0.48 / 0.08 / 0.04 |
| bmc | 380 [374-393] | 856 [839-871] | 1462 [1440-1500] | 66 [57-73] | 0.92 / 0.94 / 0.95 | 1.00 / 1.00 / 1.00 | 0.56 / 0.38 / 0.08 |
| bmc_cal | 376 [362-392] | 849 [818-875] | 1452 [1430-1485] | 68 [60-74] | 0.91 / 0.94 / 0.95 | 0.85 / 0.86 / 0.87 | 0.55 / 0.33 / 0.07 |
| bma_cal | 372 [360-383] | 834 [820-855] | 1452 [1424-1473] | 73 [63-83] | 0.91 / 0.94 / 0.95 | 0.84 / 0.86 / 0.87 | 0.51 / 0.31 / 0.07 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.76 | 0.00552 |
| bmc_cal vs calib | 0.68 | 0.104 |
| bmc_cal vs shuffled | 0.60 | 0.676 |
| bmc_cal vs transfer | 0.45 | 0.676 |
| bmc_cal vs adaptive | 0.65 | 0.225 |
| bmc_cal vs mix50 | 0.69 | 0.0908 |
| bmc_cal vs bmc | 0.42 | 0.676 |
| bmc_cal vs bma_cal | 0.60 | 0.676 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.69 | 0.0694 |
| bma_cal vs calib | 0.60 | 0.757 |
| bma_cal vs shuffled | 0.50 | 1 |
| bma_cal vs transfer | 0.31 | 0.0812 |
| bma_cal vs adaptive | 0.53 | 1 |
| bma_cal vs mix50 | 0.61 | 0.757 |
| bma_cal vs bmc | 0.30 | 0.0694 |
| bma_cal vs bmc_cal | 0.40 | 0.757 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.66 | 0.231 |
| adaptive vs calib | 0.55 | 1 |
| adaptive vs shuffled | 0.47 | 1 |
| adaptive vs transfer | 0.28 | 0.0268 |
| adaptive vs mix50 | 0.57 | 1 |
| adaptive vs bmc | 0.27 | 0.02 |
| adaptive vs bmc_cal | 0.35 | 0.231 |
| adaptive vs bma_cal | 0.47 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.00925 |
| transfer vs shuffled | 0.67 | 0.0215 |
| transfer vs fresh | 0.81 | 0.000126 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 343 [335-360] | 817 [795-834] | 1414 [1386-1446] | 103 [97-120] | 0.83 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.76 / 0.08 / 0.06 |
| calib | 394 [370-404] | 892 [860-912] | 1497 [1469-1523] | 34 [30-46] | 0.93 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 | 0.73 / 0.80 / 0.93 |
| shuffled | 202 [108-369] | 635 [414-855] | 1184 [816-1454] | 305 [51-706] | 0.43 / 0.66 / 0.76 | 0.00 / 0.00 / 0.00 | 0.85 / 0.90 / 0.85 |
| transfer | 409 [395-420] | 892 [874-919] | 1492 [1479-1542] | 10 [10-12] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 |
| adaptive | 376 [369-392] | 846 [831-871] | 1459 [1434-1482] | 59 [57-65] | 0.93 / 0.95 / 0.96 | 0.90 / 0.65 / 0.52 | 0.86 / 0.39 / 0.09 |
| mix50 | 362 [354-376] | 840 [825-863] | 1444 [1427-1467] | 82 [75-89] | 0.88 / 0.95 / 0.95 | 0.50 / 0.50 / 0.50 | 0.88 / 0.12 / 0.09 |
| bmc | 406 [384-415] | 888 [869-922] | 1508 [1479-1544] | 13 [12-14] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.91 / 1.00 / 1.00 |
| bmc_cal | 404 [391-419] | 896 [879-915] | 1509 [1482-1534] | 21 [19-23] | 1.00 / 1.00 / 0.96 | 1.00 / 1.00 / 0.62 | 0.92 / 1.00 / 1.00 |
| bma_cal | 400 [392-406] | 892 [866-911] | 1503 [1486-1528] | 21 [20-24] | 0.99 / 1.00 / 0.96 | 0.99 / 1.00 / 0.59 | 0.97 / 1.00 / 1.00 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.94 | 3.19e-08 |
| bmc_cal vs calib | 0.58 | 1 |
| bmc_cal vs shuffled | 0.87 | 4.88e-06 |
| bmc_cal vs transfer | 0.51 | 1 |
| bmc_cal vs adaptive | 0.87 | 4.88e-06 |
| bmc_cal vs mix50 | 0.89 | 1.65e-06 |
| bmc_cal vs bmc | 0.53 | 1 |
| bmc_cal vs bma_cal | 0.57 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.90 | 7.52e-07 |
| bma_cal vs calib | 0.52 | 1 |
| bma_cal vs shuffled | 0.85 | 2.98e-05 |
| bma_cal vs transfer | 0.45 | 1 |
| bma_cal vs adaptive | 0.80 | 0.000337 |
| bma_cal vs mix50 | 0.83 | 9.15e-05 |
| bma_cal vs bmc | 0.47 | 1 |
| bma_cal vs bmc_cal | 0.43 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.77 | 0.000899 |
| adaptive vs calib | 0.21 | 0.000356 |
| adaptive vs shuffled | 0.72 | 0.00716 |
| adaptive vs transfer | 0.13 | 7.42e-06 |
| adaptive vs mix50 | 0.55 | 0.51 |
| adaptive vs bmc | 0.15 | 2.13e-05 |
| adaptive vs bmc_cal | 0.13 | 6.5e-06 |
| adaptive vs bma_cal | 0.20 | 0.000337 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.57 | 0.318 |
| transfer vs shuffled | 0.87 | 1.57e-06 |
| transfer vs fresh | 0.94 | 1.37e-08 |

## mild_shift

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [1.00000e-02 1.84552e-03 7.26612e-03 1.08729e-03 8.34084e-04 4.74313e-04
 1.19068e-04 3.83869e-05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 351 [332-359] | 804 [778-823] | 1392 [1356-1417] | 105 [91-163] | 0.74 / 0.84 / 0.86 | 0.00 / 0.00 / 0.00 | 0.34 / 0.07 / 0.03 |
| calib | 376 [358-389] | 850 [824-874] | 1455 [1404-1486] | 72 [64-86] | 0.85 / 0.90 / 0.92 | 0.00 / 0.00 / 0.00 | 0.34 / 0.22 / 0.05 |
| shuffled | 370 [356-381] | 843 [823-868] | 1448 [1398-1485] | 74 [61-114] | 0.83 / 0.88 / 0.89 | 0.00 / 0.00 / 0.00 | 0.49 / 0.29 / 0.06 |
| transfer | 384 [364-396] | 851 [828-867] | 1450 [1420-1488] | 64 [57-73] | 0.90 / 0.92 / 0.93 | 1.00 / 1.00 / 1.00 | 0.68 / 0.36 / 0.09 |
| adaptive | 366 [335-380] | 830 [796-848] | 1442 [1406-1476] | 87 [71-124] | 0.82 / 0.89 / 0.91 | 0.75 / 0.58 / 0.51 | 0.54 / 0.13 / 0.04 |
| mix50 | 353 [338-369] | 816 [797-836] | 1426 [1397-1447] | 89 [77-106] | 0.83 / 0.90 / 0.91 | 0.50 / 0.50 / 0.50 | 0.48 / 0.09 / 0.04 |
| bmc | 383 [348-392] | 850 [821-873] | 1446 [1414-1491] | 73 [57-90] | 0.86 / 0.90 / 0.91 | 1.00 / 1.00 / 1.00 | 0.57 / 0.35 / 0.08 |
| bmc_cal | 384 [371-396] | 850 [834-874] | 1453 [1431-1486] | 68 [57-82] | 0.87 / 0.91 / 0.92 | 0.82 / 0.84 / 0.84 | 0.55 / 0.32 / 0.07 |
| bma_cal | 374 [367-388] | 844 [822-864] | 1443 [1409-1474] | 82 [68-92] | 0.83 / 0.88 / 0.89 | 0.84 / 0.85 / 0.86 | 0.54 / 0.31 / 0.07 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.85 | 2.21e-05 |
| bmc_cal vs calib | 0.52 | 1 |
| bmc_cal vs shuffled | 0.59 | 1 |
| bmc_cal vs transfer | 0.48 | 1 |
| bmc_cal vs adaptive | 0.68 | 0.102 |
| bmc_cal vs mix50 | 0.75 | 0.00509 |
| bmc_cal vs bmc | 0.52 | 1 |
| bmc_cal vs bma_cal | 0.58 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.79 | 0.00109 |
| bma_cal vs calib | 0.45 | 1 |
| bma_cal vs shuffled | 0.50 | 1 |
| bma_cal vs transfer | 0.42 | 1 |
| bma_cal vs adaptive | 0.61 | 0.859 |
| bma_cal vs mix50 | 0.66 | 0.264 |
| bma_cal vs bmc | 0.45 | 1 |
| bma_cal vs bmc_cal | 0.42 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.70 | 0.0487 |
| adaptive vs calib | 0.34 | 0.13 |
| adaptive vs shuffled | 0.40 | 0.43 |
| adaptive vs transfer | 0.29 | 0.0465 |
| adaptive vs mix50 | 0.56 | 0.43 |
| adaptive vs bmc | 0.33 | 0.121 |
| adaptive vs bmc_cal | 0.32 | 0.102 |
| adaptive vs bma_cal | 0.39 | 0.43 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.53 | 0.701 |
| transfer vs shuffled | 0.59 | 0.497 |
| transfer vs fresh | 0.87 | 1.94e-06 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 356 [339-371] | 812 [805-838] | 1426 [1409-1440] | 111 [98-133] | 0.78 / 0.87 / 0.89 | 0.00 / 0.00 / 0.00 | 0.80 / 0.12 / 0.10 |
| calib | 382 [356-400] | 866 [840-889] | 1488 [1403-1500] | 42 [34-57] | 0.74 / 0.77 / 0.75 | 0.00 / 0.00 / 0.00 | 0.80 / 0.82 / 0.90 |
| shuffled | 276 [213-387] | 748 [591-864] | 1364 [1022-1482] | 169 [41-481] | 0.50 / 0.60 / 0.59 | 0.00 / 0.00 / 0.00 | 0.87 / 0.89 / 0.89 |
| transfer | 396 [382-413] | 898 [871-921] | 1511 [1483-1540] | 10 [8-11] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 |
| adaptive | 383 [369-403] | 866 [843-886] | 1470 [1450-1486] | 59 [53-67] | 0.93 / 0.94 / 0.95 | 0.90 / 0.66 / 0.52 | 0.91 / 0.46 / 0.12 |
| mix50 | 358 [343-368] | 820 [799-860] | 1425 [1392-1466] | 86 [79-99] | 0.84 / 0.92 / 0.92 | 0.50 / 0.50 / 0.50 | 0.85 / 0.19 / 0.13 |
| bmc | 400 [386-415] | 896 [878-915] | 1521 [1482-1549] | 12 [10-14] | 1.00 / 1.00 / 0.97 | 1.00 / 1.00 / 1.00 | 0.93 / 1.00 / 1.00 |
| bmc_cal | 406 [392-418] | 901 [876-910] | 1498 [1471-1518] | 21 [19-23] | 1.00 / 1.00 / 0.96 | 1.00 / 1.00 / 0.58 | 0.93 / 1.00 / 1.00 |
| bma_cal | 410 [392-419] | 896 [877-921] | 1518 [1472-1556] | 20 [19-22] | 1.00 / 1.00 / 0.96 | 1.00 / 1.00 / 0.58 | 0.98 / 1.00 / 1.00 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.95 | 1.23e-08 |
| bmc_cal vs calib | 0.71 | 0.0227 |
| bmc_cal vs shuffled | 0.87 | 6.15e-06 |
| bmc_cal vs transfer | 0.47 | 1 |
| bmc_cal vs adaptive | 0.78 | 0.00079 |
| bmc_cal vs mix50 | 0.91 | 2.54e-07 |
| bmc_cal vs bmc | 0.48 | 1 |
| bmc_cal vs bma_cal | 0.46 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.95 | 1.94e-08 |
| bma_cal vs calib | 0.74 | 0.0048 |
| bma_cal vs shuffled | 0.88 | 2.87e-06 |
| bma_cal vs transfer | 0.52 | 1 |
| bma_cal vs adaptive | 0.77 | 0.00163 |
| bma_cal vs mix50 | 0.92 | 2.14e-07 |
| bma_cal vs bmc | 0.53 | 1 |
| bma_cal vs bmc_cal | 0.54 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.82 | 0.000182 |
| adaptive vs calib | 0.50 | 0.988 |
| adaptive vs shuffled | 0.76 | 0.00171 |
| adaptive vs transfer | 0.23 | 0.00154 |
| adaptive vs mix50 | 0.75 | 0.002 |
| adaptive vs bmc | 0.22 | 0.00147 |
| adaptive vs bmc_cal | 0.22 | 0.00111 |
| adaptive vs bma_cal | 0.23 | 0.00154 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00159 |
| transfer vs shuffled | 0.87 | 1.46e-06 |
| transfer vs fresh | 0.97 | 1.38e-09 |

## reversal

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [0.0002 0.005  0.003  0.002  0.001  0.0005 0.01   0.0001]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 348 [334-363] | 822 [797-846] | 1429 [1398-1454] | 105 [96-125] | 0.83 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.35 / 0.05 / 0.03 |
| calib | 365 [350-378] | 830 [801-852] | 1441 [1406-1455] | 82 [69-98] | 0.89 / 0.94 / 0.95 | 0.00 / 0.00 / 0.00 | 0.34 / 0.18 / 0.04 |
| shuffled | 372 [355-382] | 836 [815-854] | 1434 [1402-1478] | 82 [65-90] | 0.89 / 0.94 / 0.95 | 0.00 / 0.00 / 0.00 | 0.46 / 0.23 / 0.06 |
| transfer | 356 [339-374] | 821 [797-838] | 1432 [1410-1466] | 84 [74-108] | 0.86 / 0.93 / 0.94 | 1.00 / 1.00 / 1.00 | 0.60 / 0.24 / 0.06 |
| adaptive | 350 [334-366] | 819 [791-833] | 1416 [1382-1448] | 95 [88-119] | 0.85 / 0.93 / 0.94 | 0.61 / 0.54 / 0.51 | 0.46 / 0.09 / 0.03 |
| mix50 | 356 [327-372] | 810 [798-829] | 1418 [1390-1441] | 96 [84-102] | 0.85 / 0.94 / 0.95 | 0.50 / 0.50 / 0.50 | 0.43 / 0.07 / 0.03 |
| bmc | 374 [348-390] | 833 [816-855] | 1438 [1411-1460] | 79 [71-101] | 0.88 / 0.94 / 0.94 | 1.00 / 1.00 / 1.00 | 0.46 / 0.24 / 0.06 |
| bmc_cal | 367 [342-380] | 834 [804-849] | 1432 [1415-1470] | 81 [77-98] | 0.88 / 0.94 / 0.94 | 0.29 / 0.27 / 0.27 | 0.46 / 0.19 / 0.04 |
| bma_cal | 362 [349-373] | 831 [811-857] | 1424 [1396-1440] | 89 [73-110] | 0.87 / 0.93 / 0.94 | 0.28 / 0.28 / 0.28 | 0.47 / 0.18 / 0.04 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.57 | 1 |
| bmc_cal vs calib | 0.52 | 1 |
| bmc_cal vs shuffled | 0.43 | 1 |
| bmc_cal vs transfer | 0.59 | 1 |
| bmc_cal vs adaptive | 0.63 | 0.633 |
| bmc_cal vs mix50 | 0.65 | 0.38 |
| bmc_cal vs bmc | 0.45 | 1 |
| bmc_cal vs bma_cal | 0.46 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.59 | 1 |
| bma_cal vs calib | 0.51 | 1 |
| bma_cal vs shuffled | 0.44 | 1 |
| bma_cal vs transfer | 0.61 | 0.884 |
| bma_cal vs adaptive | 0.64 | 0.467 |
| bma_cal vs mix50 | 0.67 | 0.189 |
| bma_cal vs bmc | 0.48 | 1 |
| bma_cal vs bmc_cal | 0.54 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.45 | 1 |
| adaptive vs calib | 0.38 | 0.454 |
| adaptive vs shuffled | 0.30 | 0.0679 |
| adaptive vs transfer | 0.47 | 1 |
| adaptive vs mix50 | 0.54 | 1 |
| adaptive vs bmc | 0.33 | 0.175 |
| adaptive vs bmc_cal | 0.37 | 0.452 |
| adaptive vs bma_cal | 0.36 | 0.4 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.41 | 0.485 |
| transfer vs shuffled | 0.33 | 0.0607 |
| transfer vs fresh | 0.48 | 0.751 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 1.7 [1.5-2.0], never: 0/30
- calib: 1.3 [1.2-1.6], never: 0/30
- shuffled: 1.3 [1.2-1.6], never: 0/30
- transfer: 1.4 [1.2-2.2], never: 0/30
- adaptive: 1.5 [1.2-1.8], never: 0/30
- mix50: 1.4 [1.2-1.8], never: 0/30
- bmc: 1.5 [1.2-2.2], never: 0/30
- bmc_cal: 1.4 [1.2-1.8], never: 0/30
- bma_cal: 1.6 [1.2-1.9], never: 0/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 342 [328-358] | 810 [786-831] | 1418 [1401-1440] | 112 [96-119] | 0.83 / 0.93 / 0.94 | 0.00 / 0.00 / 0.00 | 0.83 / 0.08 / 0.29 |
| calib | 384 [373-398] | 882 [846-894] | 1466 [1446-1502] | 41 [31-48] | 0.91 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 | 0.83 / 0.74 / 0.82 |
| shuffled | 168 [116-300] | 467 [384-781] | 987 [745-1372] | 523 [131-804] | 0.31 / 0.53 / 0.65 | 0.00 / 0.00 / 0.00 | 0.83 / 0.86 / 0.75 |
| transfer | 178 [168-189] | 419 [392-432] | 712 [697-735] | 813 [807-817] | 0.00 / 0.00 / 0.02 | 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 0.99 |
| adaptive | 360 [344-366] | 821 [803-827] | 1405 [1384-1422] | 111 [98-124] | 0.83 / 0.93 / 0.93 | 0.42 / 0.57 / 0.50 | 0.90 / 0.14 / 0.10 |
| mix50 | 320 [304-335] | 798 [773-810] | 1379 [1339-1403] | 134 [122-156] | 0.79 / 0.93 / 0.92 | 0.49 / 0.49 / 0.50 | 0.91 / 0.12 / 0.09 |
| bmc | 174 [163-187] | 406 [393-424] | 716 [703-730] | 808 [799-818] | 0.00 / 0.00 / 0.06 | 1.00 / 1.00 / 1.00 | 0.92 / 1.00 / 0.99 |
| bmc_cal | 382 [367-394] | 876 [859-890] | 1482 [1465-1498] | 43 [36-50] | 0.89 / 0.95 / 0.92 | 0.03 / 0.00 / 0.00 | 0.92 / 0.82 / 0.88 |
| bma_cal | 381 [359-393] | 884 [850-906] | 1474 [1450-1510] | 46 [36-56] | 0.81 / 0.91 / 0.88 | 0.06 / 0.00 / 0.00 | 0.95 / 0.84 / 0.87 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.89 | 1.33e-06 |
| bmc_cal vs calib | 0.51 | 1 |
| bmc_cal vs shuffled | 0.88 | 1.84e-06 |
| bmc_cal vs transfer | 1.00 | 2.29e-10 |
| bmc_cal vs adaptive | 0.88 | 1.84e-06 |
| bmc_cal vs mix50 | 0.91 | 3.31e-07 |
| bmc_cal vs bmc | 1.00 | 2.29e-10 |
| bmc_cal vs bma_cal | 0.46 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.80 | 0.000254 |
| bma_cal vs calib | 0.53 | 1 |
| bma_cal vs shuffled | 0.86 | 1.34e-05 |
| bma_cal vs transfer | 0.98 | 9.72e-10 |
| bma_cal vs adaptive | 0.79 | 0.000341 |
| bma_cal vs mix50 | 0.82 | 0.000134 |
| bma_cal vs bmc | 0.98 | 8.7e-10 |
| bma_cal vs bmc_cal | 0.54 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.54 | 0.594 |
| adaptive vs calib | 0.17 | 4.13e-05 |
| adaptive vs shuffled | 0.78 | 0.000637 |
| adaptive vs transfer | 1.00 | 2.28e-10 |
| adaptive vs mix50 | 0.71 | 0.00991 |
| adaptive vs bmc | 1.00 | 2.28e-10 |
| adaptive vs bmc_cal | 0.12 | 2.76e-06 |
| adaptive vs bma_cal | 0.21 | 0.000455 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.01 | 1.27e-10 |
| transfer vs shuffled | 0.35 | 0.0501 |
| transfer vs fresh | 0.00 | 8.57e-11 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 1.6 [1.4-2.1], never: 0/30
- calib: 1.3 [1.2-1.5], never: 0/30
- shuffled: 30.4 [5.3-119.1], never: 5/30
- transfer: 240.0 [240.0-240.0], never: 29/30
- adaptive: 1.7 [1.5-2.2], never: 0/30
- mix50: 3.2 [2.1-4.0], never: 0/30
- bmc: 240.0 [240.0-240.0], never: 28/30
- bmc_cal: 1.3 [1.2-1.6], never: 0/30
- bma_cal: 1.4 [1.2-1.8], never: 1/30

## saturation

**old** theta: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
**new** theta: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 52 [44-61] | 133 [125-146] | 243 [228-259] | 65 [59-74] | 0.53 / 0.76 / 0.81 | 0.00 / 0.00 / 0.00 | 0.35 / 0.05 / 0.05 |
| calib | 43 [39-50] | 125 [112-129] | 230 [220-241] | 78 [70-83] | 0.45 / 0.71 / 0.77 | 0.00 / 0.00 / 0.00 | 0.36 / 0.06 / 0.04 |
| shuffled | 46 [34-55] | 118 [110-131] | 226 [210-246] | 75 [65-85] | 0.47 / 0.72 / 0.78 | 0.00 / 0.00 / 0.00 | 0.46 / 0.06 / 0.05 |
| transfer | 54 [48-63] | 135 [120-146] | 240 [223-258] | 66 [58-78] | 0.54 / 0.73 / 0.78 | 1.00 / 1.00 / 1.00 | 0.61 / 0.08 / 0.04 |
| adaptive | 52 [40-57] | 128 [120-137] | 236 [224-244] | 72 [60-78] | 0.51 / 0.74 / 0.79 | 0.61 / 0.50 / 0.50 | 0.52 / 0.07 / 0.04 |
| mix50 | 50 [44-54] | 132 [122-134] | 238 [227-250] | 68 [60-75] | 0.51 / 0.75 / 0.79 | 0.50 / 0.50 / 0.50 | 0.49 / 0.07 / 0.04 |
| bmc | 52 [46-58] | 136 [120-143] | 236 [225-253] | 66 [58-69] | 0.56 / 0.76 / 0.79 | 1.00 / 1.00 / 1.00 | 0.53 / 0.08 / 0.04 |
| bmc_cal | 47 [42-55] | 131 [117-140] | 235 [224-252] | 65 [61-70] | 0.53 / 0.76 / 0.81 | 0.71 / 0.81 / 0.82 | 0.51 / 0.06 / 0.04 |
| bma_cal | 50 [42-56] | 128 [116-139] | 236 [222-242] | 69 [62-73] | 0.52 / 0.72 / 0.78 | 0.70 / 0.80 / 0.81 | 0.52 / 0.07 / 0.04 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.41 | 1 |
| bmc_cal vs calib | 0.63 | 0.679 |
| bmc_cal vs shuffled | 0.62 | 0.881 |
| bmc_cal vs transfer | 0.40 | 1 |
| bmc_cal vs adaptive | 0.53 | 1 |
| bmc_cal vs mix50 | 0.49 | 1 |
| bmc_cal vs bmc | 0.42 | 1 |
| bmc_cal vs bma_cal | 0.51 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.39 | 1 |
| bma_cal vs calib | 0.60 | 1 |
| bma_cal vs shuffled | 0.60 | 1 |
| bma_cal vs transfer | 0.38 | 0.949 |
| bma_cal vs adaptive | 0.50 | 1 |
| bma_cal vs mix50 | 0.47 | 1 |
| bma_cal vs bmc | 0.41 | 1 |
| bma_cal vs bmc_cal | 0.49 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.38 | 0.757 |
| adaptive vs calib | 0.61 | 0.757 |
| adaptive vs shuffled | 0.62 | 0.757 |
| adaptive vs transfer | 0.37 | 0.757 |
| adaptive vs mix50 | 0.44 | 1 |
| adaptive vs bmc | 0.39 | 0.757 |
| adaptive vs bmc_cal | 0.47 | 1 |
| adaptive vs bma_cal | 0.50 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.0152 |
| transfer vs shuffled | 0.68 | 0.0374 |
| transfer vs fresh | 0.52 | 0.836 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 46 [42-52] | 128 [115-136] | 235 [220-248] | 68 [63-76] | 0.50 / 0.77 / 0.82 | 0.00 / 0.00 / 0.00 | 0.83 / 0.21 / 0.39 |
| calib | 38 [35-44] | 103 [94-114] | 195 [178-208] | 111 [103-123] | 0.37 / 0.55 / 0.62 | 0.00 / 0.00 / 0.00 | 0.85 / 0.22 / 0.14 |
| shuffled | 20 [17-38] | 80 [52-105] | 159 [132-197] | 143 [105-172] | 0.21 / 0.43 / 0.54 | 0.00 / 0.00 / 0.00 | 0.86 / 0.68 / 0.39 |
| transfer | 72 [67-77] | 154 [144-162] | 257 [238-270] | 47 [42-49] | 0.79 / 0.74 / 0.77 | 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.61 |
| adaptive | 64 [54-73] | 146 [130-155] | 246 [235-264] | 57 [54-60] | 0.69 / 0.74 / 0.78 | 0.77 / 0.55 / 0.49 | 0.93 / 0.43 / 0.19 |
| mix50 | 50 [46-58] | 128 [119-139] | 234 [219-242] | 65 [61-70] | 0.59 / 0.73 / 0.77 | 0.50 / 0.50 / 0.50 | 0.91 / 0.28 / 0.20 |
| bmc | 77 [67-81] | 154 [141-159] | 255 [248-266] | 45 [42-49] | 0.80 / 0.75 / 0.79 | 1.00 / 1.00 / 0.77 | 0.93 / 0.99 / 0.61 |
| bmc_cal | 52 [41-58] | 119 [105-130] | 216 [198-221] | 91 [83-101] | 0.53 / 0.61 / 0.67 | 0.32 / 0.20 / 0.18 | 0.93 / 0.19 / 0.15 |
| bma_cal | 52 [41-58] | 125 [102-132] | 216 [196-229] | 89 [83-106] | 0.53 / 0.61 / 0.67 | 0.32 / 0.20 / 0.17 | 0.98 / 0.21 / 0.14 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.33 | 0.0501 |
| bmc_cal vs calib | 0.73 | 0.0105 |
| bmc_cal vs shuffled | 0.82 | 0.000129 |
| bmc_cal vs transfer | 0.06 | 4.95e-08 |
| bmc_cal vs adaptive | 0.16 | 3.37e-05 |
| bmc_cal vs mix50 | 0.30 | 0.0265 |
| bmc_cal vs bmc | 0.09 | 3.66e-07 |
| bmc_cal vs bma_cal | 0.45 | 0.491 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.40 | 0.381 |
| bma_cal vs calib | 0.72 | 0.0118 |
| bma_cal vs shuffled | 0.81 | 0.000221 |
| bma_cal vs transfer | 0.09 | 3.38e-07 |
| bma_cal vs adaptive | 0.20 | 0.000379 |
| bma_cal vs mix50 | 0.39 | 0.377 |
| bma_cal vs bmc | 0.12 | 2.94e-06 |
| bma_cal vs bmc_cal | 0.55 | 0.491 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.73 | 0.011 |
| adaptive vs calib | 0.95 | 1.34e-08 |
| adaptive vs shuffled | 0.94 | 3.96e-08 |
| adaptive vs transfer | 0.34 | 0.0741 |
| adaptive vs mix50 | 0.70 | 0.019 |
| adaptive vs bmc | 0.37 | 0.0876 |
| adaptive vs bmc_cal | 0.84 | 3.37e-05 |
| adaptive vs bma_cal | 0.80 | 0.000379 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.99 | 2.42e-10 |
| transfer vs shuffled | 0.97 | 6.28e-10 |
| transfer vs fresh | 0.86 | 1.37e-06 |

## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 126 [117-134] | 296 [275-308] | 516 [485-528] | 103 [90-117] | 0.34 / 0.45 / 0.49 | 0.00 / 0.00 / 0.00 | 0.18 / 0.06 / 0.04 |
| calib | 128 [122-138] | 300 [281-307] | 511 [490-528] | 94 [79-115] | 0.42 / 0.51 / 0.53 | 0.00 / 0.00 / 0.00 | 0.19 / 0.09 / 0.03 |
| shuffled | 122 [106-131] | 287 [270-301] | 503 [482-518] | 109 [92-128] | 0.29 / 0.41 / 0.43 | 0.00 / 0.00 / 0.00 | 0.29 / 0.09 / 0.04 |
| transfer | 132 [122-139] | 300 [286-309] | 516 [488-537] | 91 [80-107] | 0.42 / 0.52 / 0.55 | 1.00 / 1.00 / 1.00 | 0.44 / 0.10 / 0.04 |
| adaptive | 127 [116-136] | 290 [276-320] | 521 [498-542] | 95 [80-116] | 0.40 / 0.49 / 0.52 | 0.57 / 0.53 / 0.50 | 0.30 / 0.08 / 0.04 |
| mix50 | 120 [114-129] | 290 [280-297] | 511 [497-521] | 93 [82-106] | 0.39 / 0.49 / 0.52 | 0.51 / 0.51 / 0.50 | 0.31 / 0.08 / 0.03 |
| bmc | 129 [119-138] | 300 [282-312] | 514 [494-534] | 89 [79-114] | 0.38 / 0.46 / 0.49 | 1.00 / 1.00 / 1.00 | 0.28 / 0.10 / 0.04 |
| bmc_cal | 127 [120-137] | 291 [275-304] | 508 [486-525] | 97 [79-117] | 0.39 / 0.47 / 0.49 | 0.68 / 0.71 / 0.71 | 0.28 / 0.09 / 0.04 |
| bma_cal | 130 [117-138] | 297 [279-309] | 512 [481-533] | 102 [88-120] | 0.37 / 0.45 / 0.46 | 0.67 / 0.71 / 0.71 | 0.28 / 0.10 / 0.04 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.48 | 1 |
| bmc_cal vs calib | 0.42 | 1 |
| bmc_cal vs shuffled | 0.58 | 1 |
| bmc_cal vs transfer | 0.41 | 1 |
| bmc_cal vs adaptive | 0.46 | 1 |
| bmc_cal vs mix50 | 0.53 | 1 |
| bmc_cal vs bmc | 0.41 | 1 |
| bmc_cal vs bma_cal | 0.44 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.53 | 1 |
| bma_cal vs calib | 0.47 | 1 |
| bma_cal vs shuffled | 0.63 | 0.638 |
| bma_cal vs transfer | 0.45 | 1 |
| bma_cal vs adaptive | 0.50 | 1 |
| bma_cal vs mix50 | 0.60 | 1 |
| bma_cal vs bmc | 0.46 | 1 |
| bma_cal vs bmc_cal | 0.56 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.53 | 1 |
| adaptive vs calib | 0.46 | 1 |
| adaptive vs shuffled | 0.62 | 0.83 |
| adaptive vs transfer | 0.46 | 1 |
| adaptive vs mix50 | 0.56 | 1 |
| adaptive vs bmc | 0.48 | 1 |
| adaptive vs bmc_cal | 0.54 | 1 |
| adaptive vs bma_cal | 0.50 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.51 | 0.848 |
| transfer vs shuffled | 0.68 | 0.0449 |
| transfer vs fresh | 0.56 | 0.815 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 120 [111-133] | 285 [265-309] | 506 [486-521] | 103 [91-116] | 0.35 / 0.46 / 0.49 | 0.00 / 0.00 / 0.00 | 0.52 / 0.21 / 0.10 |
| calib | 134 [123-144] | 306 [278-334] | 524 [488-560] | 82 [53-109] | 0.49 / 0.53 / 0.52 | 0.00 / 0.00 / 0.00 | 0.53 / 0.64 / 0.17 |
| shuffled | 126 [113-144] | 292 [259-318] | 498 [436-530] | 110 [54-164] | 0.34 / 0.38 / 0.38 | 0.00 / 0.00 / 0.00 | 0.71 / 0.83 / 0.57 |
| transfer | 148 [139-156] | 325 [312-354] | 552 [532-574] | 44 [32-62] | 0.63 / 0.62 / 0.60 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.91 |
| adaptive | 138 [128-150] | 317 [297-323] | 540 [526-562] | 68 [54-87] | 0.57 / 0.61 / 0.62 | 0.74 / 0.57 / 0.50 | 0.73 / 0.46 / 0.13 |
| mix50 | 132 [118-138] | 306 [292-315] | 517 [501-540] | 85 [72-98] | 0.49 / 0.56 / 0.57 | 0.49 / 0.50 / 0.50 | 0.74 / 0.33 / 0.13 |
| bmc | 156 [147-162] | 334 [325-352] | 564 [546-575] | 36 [30-69] | 0.64 / 0.62 / 0.61 | 1.00 / 1.00 / 1.00 | 0.70 / 1.00 / 0.91 |
| bmc_cal | 145 [138-160] | 328 [314-348] | 553 [533-570] | 48 [36-67] | 0.64 / 0.63 / 0.61 | 0.96 / 0.91 / 0.83 | 0.67 / 0.97 / 0.55 |
| bma_cal | 146 [134-154] | 320 [311-338] | 545 [523-572] | 48 [37-75] | 0.61 / 0.61 / 0.60 | 0.94 / 0.87 / 0.81 | 0.82 / 0.95 / 0.48 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.90 | 8.46e-07 |
| bmc_cal vs calib | 0.71 | 0.0208 |
| bmc_cal vs shuffled | 0.81 | 0.000222 |
| bmc_cal vs transfer | 0.47 | 0.841 |
| bmc_cal vs adaptive | 0.73 | 0.011 |
| bmc_cal vs mix50 | 0.82 | 0.000114 |
| bmc_cal vs bmc | 0.43 | 0.841 |
| bmc_cal vs bma_cal | 0.58 | 0.841 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.88 | 3.03e-06 |
| bma_cal vs calib | 0.67 | 0.103 |
| bma_cal vs shuffled | 0.80 | 0.000567 |
| bma_cal vs transfer | 0.41 | 0.412 |
| bma_cal vs adaptive | 0.67 | 0.103 |
| bma_cal vs mix50 | 0.79 | 0.00068 |
| bma_cal vs bmc | 0.37 | 0.284 |
| bma_cal vs bmc_cal | 0.42 | 0.412 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.77 | 0.00262 |
| adaptive vs calib | 0.54 | 0.605 |
| adaptive vs shuffled | 0.68 | 0.0778 |
| adaptive vs transfer | 0.27 | 0.0108 |
| adaptive vs mix50 | 0.64 | 0.135 |
| adaptive vs bmc | 0.20 | 0.000609 |
| adaptive vs bmc_cal | 0.27 | 0.011 |
| adaptive vs bma_cal | 0.33 | 0.0778 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.74 | 0.00163 |
| transfer vs shuffled | 0.84 | 1.2e-05 |
| transfer vs fresh | 0.91 | 1.18e-07 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.0015 0.0035 0.003  0.004  0.0025 0.001  0.0005 0.0002]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 124 [115-138] | 296 [279-312] | 514 [488-529] | 103 [87-119] | 0.36 / 0.48 / 0.50 | 0.00 / 0.00 / 0.00 | 0.21 / 0.06 / 0.04 |
| calib | 121 [112-130] | 286 [268-295] | 498 [476-516] | 107 [85-133] | 0.32 / 0.41 / 0.44 | 0.00 / 0.00 / 0.00 | 0.18 / 0.08 / 0.04 |
| shuffled | 124 [112-133] | 294 [270-314] | 504 [484-530] | 103 [83-122] | 0.34 / 0.45 / 0.47 | 0.00 / 0.00 / 0.00 | 0.31 / 0.08 / 0.04 |
| transfer | 130 [118-138] | 290 [276-316] | 520 [492-538] | 92 [76-111] | 0.45 / 0.52 / 0.55 | 1.00 / 1.00 / 1.00 | 0.44 / 0.09 / 0.04 |
| adaptive | 122 [111-131] | 286 [276-303] | 508 [490-519] | 110 [99-120] | 0.28 / 0.39 / 0.41 | 0.56 / 0.52 / 0.51 | 0.34 / 0.07 / 0.04 |
| mix50 | 130 [116-137] | 296 [272-312] | 509 [486-537] | 96 [85-113] | 0.36 / 0.46 / 0.48 | 0.49 / 0.51 / 0.50 | 0.33 / 0.07 / 0.04 |
| bmc | 133 [118-138] | 302 [288-315] | 524 [503-547] | 95 [80-104] | 0.38 / 0.48 / 0.49 | 1.00 / 1.00 / 1.00 | 0.32 / 0.09 / 0.05 |
| bmc_cal | 121 [117-132] | 299 [281-308] | 505 [487-538] | 98 [82-115] | 0.37 / 0.47 / 0.48 | 0.60 / 0.64 / 0.64 | 0.32 / 0.08 / 0.04 |
| bma_cal | 133 [122-141] | 297 [282-310] | 512 [498-538] | 98 [80-119] | 0.35 / 0.44 / 0.46 | 0.61 / 0.65 / 0.66 | 0.32 / 0.08 / 0.04 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.51 | 1 |
| bmc_cal vs calib | 0.65 | 0.38 |
| bmc_cal vs shuffled | 0.54 | 1 |
| bmc_cal vs transfer | 0.51 | 1 |
| bmc_cal vs adaptive | 0.61 | 1 |
| bmc_cal vs mix50 | 0.53 | 1 |
| bmc_cal vs bmc | 0.43 | 1 |
| bmc_cal vs bma_cal | 0.50 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.51 | 1 |
| bma_cal vs calib | 0.65 | 0.414 |
| bma_cal vs shuffled | 0.54 | 1 |
| bma_cal vs transfer | 0.51 | 1 |
| bma_cal vs adaptive | 0.60 | 1 |
| bma_cal vs mix50 | 0.53 | 1 |
| bma_cal vs bmc | 0.42 | 1 |
| bma_cal vs bmc_cal | 0.50 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.41 | 1 |
| adaptive vs calib | 0.56 | 1 |
| adaptive vs shuffled | 0.46 | 1 |
| adaptive vs transfer | 0.43 | 1 |
| adaptive vs mix50 | 0.45 | 1 |
| adaptive vs bmc | 0.34 | 0.229 |
| adaptive vs bmc_cal | 0.39 | 1 |
| adaptive vs bma_cal | 0.40 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.61 | 0.383 |
| transfer vs shuffled | 0.54 | 1 |
| transfer vs fresh | 0.49 | 1 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 11.0 [4.0-27.1], never: 5/30
- calib: 28.5 [3.1-240.0], never: 12/30
- shuffled: 8.2 [3.4-207.7], never: 8/30
- transfer: 4.9 [2.5-9.9], never: 4/30
- adaptive: 19.0 [7.1-240.0], never: 9/30
- mix50: 8.2 [4.1-31.8], never: 7/30
- bmc: 7.4 [3.4-16.3], never: 5/30
- bmc_cal: 8.5 [3.7-240.0], never: 9/30
- bma_cal: 6.5 [3.5-240.0], never: 10/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 127 [116-133] | 288 [272-303] | 507 [490-521] | 98 [87-112] | 0.38 / 0.48 / 0.50 | 0.00 / 0.00 / 0.00 | 0.53 / 0.21 / 0.18 |
| calib | 141 [132-150] | 318 [287-328] | 526 [494-559] | 71 [53-102] | 0.53 / 0.58 / 0.56 | 0.00 / 0.00 / 0.00 | 0.52 / 0.55 / 0.26 |
| shuffled | 126 [111-148] | 296 [253-326] | 508 [439-550] | 113 [56-163] | 0.33 / 0.39 / 0.39 | 0.00 / 0.00 / 0.00 | 0.62 / 0.81 / 0.45 |
| transfer | 132 [120-144] | 302 [290-314] | 514 [482-528] | 102 [85-122] | 0.26 / 0.32 / 0.33 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.87 |
| adaptive | 129 [120-137] | 294 [278-310] | 501 [481-531] | 99 [79-119] | 0.37 / 0.45 / 0.47 | 0.62 / 0.55 / 0.49 | 0.76 / 0.33 / 0.13 |
| mix50 | 122 [115-132] | 288 [277-301] | 500 [487-518] | 105 [92-117] | 0.35 / 0.46 / 0.46 | 0.49 / 0.50 / 0.50 | 0.79 / 0.26 / 0.14 |
| bmc | 134 [124-141] | 298 [286-314] | 508 [489-530] | 101 [81-115] | 0.26 / 0.34 / 0.34 | 1.00 / 1.00 / 1.00 | 0.77 / 0.99 / 0.87 |
| bmc_cal | 132 [120-144] | 306 [285-313] | 510 [487-548] | 103 [77-117] | 0.30 / 0.42 / 0.40 | 0.86 / 0.73 / 0.66 | 0.76 / 0.86 / 0.27 |
| bma_cal | 137 [128-144] | 300 [294-314] | 511 [494-524] | 101 [77-124] | 0.32 / 0.38 / 0.37 | 0.83 / 0.70 / 0.63 | 0.80 / 0.86 / 0.27 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.65 | 0.289 |
| bmc_cal vs calib | 0.40 | 1 |
| bmc_cal vs shuffled | 0.58 | 1 |
| bmc_cal vs transfer | 0.50 | 1 |
| bmc_cal vs adaptive | 0.60 | 1 |
| bmc_cal vs mix50 | 0.66 | 0.26 |
| bmc_cal vs bmc | 0.52 | 1 |
| bmc_cal vs bma_cal | 0.48 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.71 | 0.0371 |
| bma_cal vs calib | 0.39 | 0.8 |
| bma_cal vs shuffled | 0.60 | 0.814 |
| bma_cal vs transfer | 0.52 | 1 |
| bma_cal vs adaptive | 0.64 | 0.362 |
| bma_cal vs mix50 | 0.72 | 0.0285 |
| bma_cal vs bmc | 0.55 | 1 |
| bma_cal vs bmc_cal | 0.52 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.55 | 1 |
| adaptive vs calib | 0.30 | 0.0532 |
| adaptive vs shuffled | 0.50 | 1 |
| adaptive vs transfer | 0.39 | 0.823 |
| adaptive vs mix50 | 0.54 | 1 |
| adaptive vs bmc | 0.41 | 1 |
| adaptive vs bmc_cal | 0.40 | 1 |
| adaptive vs bma_cal | 0.36 | 0.422 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.40 | 0.366 |
| transfer vs shuffled | 0.59 | 0.366 |
| transfer vs fresh | 0.66 | 0.113 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 6.7 [4.4-23.9], never: 5/30
- calib: 4.5 [2.2-13.2], never: 7/30
- shuffled: 145.1 [1.8-240.0], never: 15/30
- transfer: 240.0 [7.6-240.0], never: 17/30
- adaptive: 14.0 [3.9-240.0], never: 10/30
- mix50: 8.2 [5.2-26.6], never: 6/30
- bmc: 129.6 [6.2-240.0], never: 15/30
- bmc_cal: 22.5 [5.2-240.0], never: 9/30
- bma_cal: 19.4 [3.5-240.0], never: 14/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0015 0.0015 0.001  0.0005 0.0002]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 125 [116-134] | 294 [284-311] | 642 [590-666] | 274 [252-312] | 0.39 / 0.20 / 0.36 | 0.00 / 0.00 / 0.00 | 0.19 / 0.07 / 0.04 |
| calib | 128 [115-136] | 302 [294-318] | 630 [604-656] | 274 [256-302] | 0.41 / 0.22 / 0.36 | 0.00 / 0.00 / 0.00 | 0.18 / 0.08 / 0.04 |
| shuffled | 120 [114-128] | 301 [291-308] | 633 [595-678] | 291 [236-307] | 0.35 / 0.23 / 0.39 | 0.00 / 0.00 / 0.00 | 0.32 / 0.09 / 0.05 |
| transfer | 128 [115-136] | 303 [290-316] | 626 [592-658] | 273 [248-306] | 0.41 / 0.23 / 0.35 | 1.00 / 1.00 / 1.00 | 0.43 / 0.10 / 0.04 |
| adaptive | 123 [105-130] | 288 [270-311] | 634 [607-667] | 267 [233-287] | 0.35 / 0.22 / 0.43 | 0.60 / 0.51 / 0.50 | 0.32 / 0.09 / 0.04 |
| mix50 | 124 [113-131] | 296 [284-306] | 622 [588-654] | 277 [258-302] | 0.36 / 0.21 / 0.37 | 0.51 / 0.50 / 0.50 | 0.33 / 0.08 / 0.04 |
| bmc | 134 [119-140] | 315 [298-326] | 633 [601-649] | 285 [256-308] | 0.46 / 0.21 / 0.32 | 1.00 / 1.00 / 1.00 | 0.28 / 0.11 / 0.04 |
| bmc_cal | 120 [110-131] | 296 [283-309] | 628 [602-674] | 264 [230-298] | 0.40 / 0.24 / 0.40 | 0.66 / 0.70 / 0.71 | 0.27 / 0.09 / 0.04 |
| bma_cal | 128 [116-138] | 302 [287-313] | 610 [571-654] | 294 [253-325] | 0.41 / 0.20 / 0.32 | 0.67 / 0.71 / 0.72 | 0.30 / 0.09 / 0.05 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.49 | 1 |
| bmc_cal vs calib | 0.43 | 1 |
| bmc_cal vs shuffled | 0.45 | 1 |
| bmc_cal vs transfer | 0.39 | 1 |
| bmc_cal vs adaptive | 0.55 | 1 |
| bmc_cal vs mix50 | 0.52 | 1 |
| bmc_cal vs bmc | 0.30 | 0.0649 |
| bmc_cal vs bma_cal | 0.44 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.55 | 1 |
| bma_cal vs calib | 0.48 | 1 |
| bma_cal vs shuffled | 0.52 | 1 |
| bma_cal vs transfer | 0.44 | 1 |
| bma_cal vs adaptive | 0.61 | 1 |
| bma_cal vs mix50 | 0.58 | 1 |
| bma_cal vs bmc | 0.33 | 0.216 |
| bma_cal vs bmc_cal | 0.56 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.42 | 0.935 |
| adaptive vs calib | 0.40 | 0.934 |
| adaptive vs shuffled | 0.41 | 0.935 |
| adaptive vs transfer | 0.35 | 0.305 |
| adaptive vs mix50 | 0.46 | 1 |
| adaptive vs bmc | 0.28 | 0.0242 |
| adaptive vs bmc_cal | 0.45 | 1 |
| adaptive vs bma_cal | 0.39 | 0.934 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.52 | 0.83 |
| transfer vs shuffled | 0.56 | 0.815 |
| transfer vs fresh | 0.60 | 0.521 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 124 [114-134] | 300 [281-318] | 648 [624-683] | 262 [243-287] | 0.35 / 0.23 / 0.42 | 0.00 / 0.00 / 0.00 | 0.54 / 0.22 / 0.13 |
| calib | 136 [129-142] | 308 [296-322] | 611 [588-648] | 291 [264-306] | 0.44 / 0.21 / 0.30 | 0.00 / 0.00 / 0.00 | 0.54 / 0.66 / 0.20 |
| shuffled | 128 [118-140] | 297 [284-314] | 624 [584-669] | 301 [254-323] | 0.28 / 0.19 / 0.38 | 0.00 / 0.00 / 0.00 | 0.67 / 0.84 / 0.53 |
| transfer | 152 [142-167] | 332 [318-352] | 644 [606-671] | 260 [246-288] | 0.56 / 0.21 / 0.27 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.92 |
| adaptive | 138 [129-149] | 314 [300-330] | 639 [616-675] | 281 [232-300] | 0.52 / 0.23 / 0.32 | 0.74 / 0.58 / 0.50 | 0.80 / 0.44 / 0.15 |
| mix50 | 128 [122-140] | 310 [291-324] | 623 [608-646] | 283 [255-300] | 0.42 / 0.21 / 0.34 | 0.51 / 0.50 / 0.50 | 0.74 / 0.32 / 0.14 |
| bmc | 141 [134-154] | 327 [310-350] | 645 [613-674] | 265 [243-287] | 0.52 / 0.22 / 0.28 | 1.00 / 1.00 / 1.00 | 0.72 / 0.99 / 0.90 |
| bmc_cal | 147 [139-158] | 329 [317-352] | 642 [624-671] | 269 [252-287] | 0.57 / 0.22 / 0.28 | 0.95 / 0.89 / 0.84 | 0.70 / 0.96 / 0.57 |
| bma_cal | 148 [140-155] | 332 [322-344] | 621 [602-658] | 274 [254-309] | 0.56 / 0.22 / 0.24 | 0.95 / 0.90 / 0.84 | 0.84 / 0.97 / 0.56 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.82 | 0.000153 |
| bmc_cal vs calib | 0.78 | 0.00143 |
| bmc_cal vs shuffled | 0.84 | 5.56e-05 |
| bmc_cal vs transfer | 0.48 | 1 |
| bmc_cal vs adaptive | 0.71 | 0.0181 |
| bmc_cal vs mix50 | 0.77 | 0.00145 |
| bmc_cal vs bmc | 0.53 | 1 |
| bmc_cal vs bma_cal | 0.50 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.83 | 0.000103 |
| bma_cal vs calib | 0.79 | 0.000603 |
| bma_cal vs shuffled | 0.84 | 3.64e-05 |
| bma_cal vs transfer | 0.49 | 1 |
| bma_cal vs adaptive | 0.73 | 0.0105 |
| bma_cal vs mix50 | 0.79 | 0.000603 |
| bma_cal vs bmc | 0.53 | 1 |
| bma_cal vs bmc_cal | 0.50 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.66 | 0.103 |
| adaptive vs calib | 0.57 | 0.594 |
| adaptive vs shuffled | 0.68 | 0.0864 |
| adaptive vs transfer | 0.28 | 0.0288 |
| adaptive vs mix50 | 0.58 | 0.594 |
| adaptive vs bmc | 0.33 | 0.0864 |
| adaptive vs bmc_cal | 0.29 | 0.0288 |
| adaptive vs bma_cal | 0.27 | 0.021 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.79 | 0.000132 |
| transfer vs shuffled | 0.84 | 1.94e-05 |
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
| shuffled | 100 [93-108] | 213 [205-229] | 350 [335-360] | 40 [32-48] | 0.21 / 0.27 / 0.22 | 0.00 / 0.00 / 0.00 | 0.30 / 0.08 / 0.04 |
| transfer | 104 [98-109] | 224 [217-233] | 360 [343-372] | 43 [34-49] | 0.26 / 0.29 / 0.23 | 1.00 / 1.00 / 1.00 | 0.40 / 0.10 / 0.04 |
| adaptive | 104 [100-112] | 221 [207-229] | 351 [335-364] | 47 [40-57] | 0.26 / 0.24 / 0.21 | 0.56 / 0.52 / 0.50 | 0.26 / 0.07 / 0.04 |
| mix50 | 102 [94-106] | 220 [212-228] | 361 [347-370] | 42 [31-51] | 0.26 / 0.30 / 0.26 | 0.50 / 0.49 / 0.50 | 0.33 / 0.07 / 0.04 |
| bmc | 101 [94-111] | 220 [208-235] | 352 [337-369] | 44 [39-58] | 0.27 / 0.26 / 0.21 | 1.00 / 1.00 / 1.00 | 0.25 / 0.09 / 0.04 |
| bmc_cal | 104 [96-111] | 218 [208-226] | 348 [339-365] | 41 [34-54] | 0.24 / 0.24 / 0.22 | 0.65 / 0.69 / 0.68 | 0.24 / 0.08 / 0.04 |
| bma_cal | 100 [93-110] | 218 [208-232] | 352 [337-370] | 43 [35-50] | 0.26 / 0.26 / 0.22 | 0.65 / 0.68 / 0.67 | 0.30 / 0.08 / 0.04 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.51 | 1 |
| bmc_cal vs calib | 0.51 | 1 |
| bmc_cal vs shuffled | 0.56 | 1 |
| bmc_cal vs transfer | 0.37 | 0.756 |
| bmc_cal vs adaptive | 0.47 | 1 |
| bmc_cal vs mix50 | 0.45 | 1 |
| bmc_cal vs bmc | 0.44 | 1 |
| bmc_cal vs bma_cal | 0.45 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.54 | 1 |
| bma_cal vs calib | 0.54 | 1 |
| bma_cal vs shuffled | 0.60 | 1 |
| bma_cal vs transfer | 0.43 | 1 |
| bma_cal vs adaptive | 0.53 | 1 |
| bma_cal vs mix50 | 0.50 | 1 |
| bma_cal vs bmc | 0.48 | 1 |
| bma_cal vs bmc_cal | 0.55 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.52 | 1 |
| adaptive vs calib | 0.51 | 1 |
| adaptive vs shuffled | 0.57 | 1 |
| adaptive vs transfer | 0.40 | 1 |
| adaptive vs mix50 | 0.48 | 1 |
| adaptive vs bmc | 0.44 | 1 |
| adaptive vs bmc_cal | 0.53 | 1 |
| adaptive vs bma_cal | 0.47 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.61 | 0.244 |
| transfer vs shuffled | 0.67 | 0.0751 |
| transfer vs fresh | 0.62 | 0.244 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 104 [96-109] | 217 [208-228] | 352 [336-360] | 43 [35-52] | 0.24 / 0.28 / 0.24 | 0.00 / 0.00 / 0.00 | 0.51 / 0.22 / 0.16 |
| calib | 100 [92-108] | 218 [204-227] | 343 [335-357] | 54 [42-68] | 0.21 / 0.22 / 0.18 | 0.00 / 0.00 / 0.00 | 0.51 / 0.43 / 0.17 |
| shuffled | 101 [89-111] | 216 [191-226] | 332 [312-351] | 66 [49-87] | 0.08 / 0.08 / 0.11 | 0.00 / 0.00 / 0.00 | 0.70 / 0.79 / 0.36 |
| transfer | 108 [101-113] | 230 [210-236] | 351 [339-369] | 40 [30-49] | 0.35 / 0.24 / 0.20 | 1.00 / 1.00 / 1.00 | 0.97 / 0.99 / 0.59 |
| adaptive | 106 [97-118] | 225 [208-238] | 361 [345-374] | 43 [38-53] | 0.31 / 0.28 / 0.23 | 0.65 / 0.54 / 0.49 | 0.69 / 0.34 / 0.15 |
| mix50 | 100 [94-112] | 220 [204-233] | 348 [337-363] | 43 [37-55] | 0.30 / 0.28 / 0.23 | 0.50 / 0.51 / 0.50 | 0.78 / 0.33 / 0.16 |
| bmc | 108 [96-121] | 223 [210-239] | 353 [343-376] | 41 [33-54] | 0.35 / 0.19 / 0.18 | 1.00 / 1.00 / 1.00 | 0.63 / 0.98 / 0.58 |
| bmc_cal | 108 [101-118] | 228 [214-236] | 353 [343-364] | 46 [37-53] | 0.32 / 0.22 / 0.20 | 0.93 / 0.79 / 0.72 | 0.61 / 0.91 / 0.21 |
| bma_cal | 110 [105-116] | 220 [210-237] | 350 [327-365] | 46 [38-55] | 0.36 / 0.19 / 0.18 | 0.92 / 0.77 / 0.71 | 0.80 / 0.91 / 0.19 |

bmc_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bmc_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bmc_cal vs fresh | 0.64 | 0.4 |
| bmc_cal vs calib | 0.65 | 0.289 |
| bmc_cal vs shuffled | 0.69 | 0.0788 |
| bmc_cal vs transfer | 0.51 | 1 |
| bmc_cal vs adaptive | 0.54 | 1 |
| bmc_cal vs mix50 | 0.61 | 0.757 |
| bmc_cal vs bmc | 0.52 | 1 |
| bmc_cal vs bma_cal | 0.55 | 1 |

bma_cal vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(bma_cal > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| bma_cal vs fresh | 0.58 | 1 |
| bma_cal vs calib | 0.58 | 1 |
| bma_cal vs shuffled | 0.65 | 0.387 |
| bma_cal vs transfer | 0.47 | 1 |
| bma_cal vs adaptive | 0.49 | 1 |
| bma_cal vs mix50 | 0.56 | 1 |
| bma_cal vs bmc | 0.47 | 1 |
| bma_cal vs bmc_cal | 0.45 | 1 |

adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.59 | 1 |
| adaptive vs calib | 0.60 | 1 |
| adaptive vs shuffled | 0.66 | 0.238 |
| adaptive vs transfer | 0.47 | 1 |
| adaptive vs mix50 | 0.58 | 1 |
| adaptive vs bmc | 0.48 | 1 |
| adaptive vs bmc_cal | 0.46 | 1 |
| adaptive vs bma_cal | 0.51 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.65 | 0.0916 |
| transfer vs shuffled | 0.69 | 0.0321 |
| transfer vs fresh | 0.64 | 0.0916 |
