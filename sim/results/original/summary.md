# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults N=500, gamma=0.98, B=256.

Cells: median [IQR] of cumulative successes. Regret = oracle expected successes - policy expected successes at 4h.


## no_shift

old rates: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
new rates: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]

| policy | 15m | 1h | 4h | regret@4h | share T (0-15m / 15m-1h / 1h-4h) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|
| fresh | 353 [342-364] | 812 [792-842] | 1408 [1390-1438] | 100 [93-111] | 0.00 / 0.00 / 0.00 | 0.31 / 0.05 / 0.03 |
| calib | 364 [343-378] | 822 [794-859] | 1424 [1396-1454] | 82 [68-104] | 0.00 / 0.00 / 0.00 | 0.32 / 0.20 / 0.04 |
| shuffled | 364 [350-377] | 836 [814-855] | 1441 [1402-1478] | 74 [69-86] | 0.00 / 0.00 / 0.00 | 0.48 / 0.28 / 0.06 |
| transfer | 388 [364-400] | 854 [838-875] | 1459 [1443-1479] | 67 [59-76] | 1.00 / 1.00 / 1.00 | 0.68 / 0.37 / 0.08 |
| adaptive | 368 [353-376] | 834 [810-858] | 1444 [1415-1456] | 87 [74-96] | 0.78 / 0.58 / 0.51 | 0.47 / 0.14 / 0.04 |
| mix50 | 358 [346-376] | 822 [804-846] | 1436 [1418-1459] | 94 [81-105] | 0.50 / 0.50 / 0.50 | 0.48 / 0.08 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm-corrected within scenario; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.66 | 0.154 |
| adaptive vs calib | 0.55 | 1 |
| adaptive vs shuffled | 0.47 | 1 |
| adaptive vs transfer | 0.28 | 0.0192 |
| adaptive vs mix50 | 0.57 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.00925 |
| transfer vs shuffled | 0.67 | 0.0215 |
| transfer vs fresh | 0.81 | 0.000126 |

## mild_shift

old rates: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
new rates: [1.00000e-02 1.84552e-03 7.26612e-03 1.08729e-03 8.34084e-04 4.74313e-04
 1.19068e-04 3.83869e-05]

| policy | 15m | 1h | 4h | regret@4h | share T (0-15m / 15m-1h / 1h-4h) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|
| fresh | 351 [332-359] | 804 [778-823] | 1392 [1356-1417] | 105 [91-163] | 0.00 / 0.00 / 0.00 | 0.34 / 0.07 / 0.03 |
| calib | 376 [358-389] | 850 [824-874] | 1455 [1404-1486] | 72 [64-86] | 0.00 / 0.00 / 0.00 | 0.34 / 0.22 / 0.05 |
| shuffled | 370 [356-381] | 843 [823-868] | 1448 [1398-1485] | 74 [61-114] | 0.00 / 0.00 / 0.00 | 0.49 / 0.29 / 0.06 |
| transfer | 384 [364-396] | 851 [828-867] | 1450 [1420-1488] | 64 [57-73] | 1.00 / 1.00 / 1.00 | 0.68 / 0.36 / 0.09 |
| adaptive | 366 [335-380] | 830 [796-848] | 1442 [1406-1476] | 87 [71-124] | 0.75 / 0.58 / 0.51 | 0.54 / 0.13 / 0.04 |
| mix50 | 353 [338-369] | 816 [797-836] | 1426 [1397-1447] | 89 [77-106] | 0.50 / 0.50 / 0.50 | 0.48 / 0.09 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm-corrected within scenario; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.70 | 0.0291 |
| adaptive vs calib | 0.34 | 0.0979 |
| adaptive vs shuffled | 0.40 | 0.338 |
| adaptive vs transfer | 0.29 | 0.0291 |
| adaptive vs mix50 | 0.56 | 0.403 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.53 | 0.701 |
| transfer vs shuffled | 0.59 | 0.497 |
| transfer vs fresh | 0.87 | 1.94e-06 |

## reversal

old rates: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
new rates: [0.0002 0.005  0.003  0.002  0.001  0.0005 0.01   0.0001]

| policy | 15m | 1h | 4h | regret@4h | share T (0-15m / 15m-1h / 1h-4h) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|
| fresh | 348 [334-363] | 822 [797-846] | 1429 [1398-1454] | 105 [96-125] | 0.00 / 0.00 / 0.00 | 0.35 / 0.05 / 0.03 |
| calib | 365 [350-378] | 830 [801-852] | 1441 [1406-1455] | 82 [69-98] | 0.00 / 0.00 / 0.00 | 0.34 / 0.18 / 0.04 |
| shuffled | 372 [355-382] | 836 [815-854] | 1434 [1402-1478] | 82 [65-90] | 0.00 / 0.00 / 0.00 | 0.46 / 0.23 / 0.06 |
| transfer | 356 [339-374] | 821 [797-838] | 1432 [1410-1466] | 84 [74-108] | 1.00 / 1.00 / 1.00 | 0.60 / 0.24 / 0.06 |
| adaptive | 350 [334-366] | 819 [791-833] | 1416 [1382-1448] | 95 [88-119] | 0.61 / 0.54 / 0.51 | 0.46 / 0.09 / 0.03 |
| mix50 | 356 [327-372] | 810 [798-829] | 1418 [1390-1441] | 96 [84-102] | 0.50 / 0.50 / 0.50 | 0.43 / 0.07 / 0.03 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm-corrected within scenario; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.45 | 1 |
| adaptive vs calib | 0.38 | 0.454 |
| adaptive vs shuffled | 0.30 | 0.0424 |
| adaptive vs transfer | 0.47 | 1 |
| adaptive vs mix50 | 0.54 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.41 | 0.485 |
| transfer vs shuffled | 0.33 | 0.0607 |
| transfer vs fresh | 0.48 | 0.751 |

Recovery after reversal: minutes until the 20-batch rolling share of the new best operator reaches 50% (median [IQR]; inf = never):

- fresh: 1.7 [1.5-2.0], never: 0/30
- calib: 1.3 [1.2-1.6], never: 0/30
- shuffled: 1.3 [1.2-1.6], never: 0/30
- transfer: 1.4 [1.2-2.2], never: 0/30
- adaptive: 1.5 [1.2-1.8], never: 0/30
- mix50: 1.4 [1.2-1.8], never: 0/30

## saturation

old rates: [0.01   0.005  0.003  0.002  0.001  0.0005 0.0002 0.0001]  
new rates: [2.e-03 1.e-03 6.e-04 4.e-04 2.e-04 1.e-04 4.e-05 2.e-05]

| policy | 15m | 1h | 4h | regret@4h | share T (0-15m / 15m-1h / 1h-4h) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|
| fresh | 52 [44-61] | 133 [125-146] | 243 [228-259] | 65 [59-74] | 0.00 / 0.00 / 0.00 | 0.35 / 0.05 / 0.05 |
| calib | 43 [39-50] | 125 [112-129] | 230 [220-241] | 78 [70-83] | 0.00 / 0.00 / 0.00 | 0.36 / 0.06 / 0.04 |
| shuffled | 46 [34-55] | 118 [110-131] | 226 [210-246] | 75 [65-85] | 0.00 / 0.00 / 0.00 | 0.46 / 0.06 / 0.05 |
| transfer | 54 [48-63] | 135 [120-146] | 240 [223-258] | 66 [58-78] | 1.00 / 1.00 / 1.00 | 0.61 / 0.08 / 0.04 |
| adaptive | 52 [40-57] | 128 [120-137] | 236 [224-244] | 72 [60-78] | 0.61 / 0.50 / 0.50 | 0.52 / 0.07 / 0.04 |
| mix50 | 50 [44-54] | 132 [122-134] | 238 [227-250] | 68 [60-75] | 0.50 / 0.50 / 0.50 | 0.49 / 0.07 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm-corrected within scenario; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.38 | 0.473 |
| adaptive vs calib | 0.61 | 0.473 |
| adaptive vs shuffled | 0.62 | 0.473 |
| adaptive vs transfer | 0.37 | 0.473 |
| adaptive vs mix50 | 0.44 | 0.473 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.71 | 0.0152 |
| transfer vs shuffled | 0.68 | 0.0374 |
| transfer vs fresh | 0.52 | 0.836 |

# Sensitivity (median successes at 1h / 4h)


## N

| scenario | policy | N=0 | N=50 | N=500 | N=5000 |
|---|---|---|---|---|---|
| no_shift | adaptive | 816 / 1415 | 806 / 1412 | 834 / 1444 | 846 / 1459 |
| no_shift | transfer | 806 / 1420 | 820 / 1414 | 854 / 1459 | 892 / 1492 |
| mild_shift | adaptive | 823 / 1422 | 809 / 1396 | 830 / 1442 | 866 / 1470 |
| mild_shift | transfer | 802 / 1406 | 824 / 1408 | 851 / 1450 | 898 / 1511 |
| reversal | adaptive | 820 / 1420 | 812 / 1420 | 819 / 1416 | 821 / 1405 |
| reversal | transfer | 809 / 1394 | 814 / 1428 | 821 / 1432 | 419 / 712 |
| saturation | adaptive | 124 / 230 | 127 / 233 | 128 / 236 | 146 / 246 |
| saturation | transfer | 132 / 235 | 130 / 234 | 135 / 240 | 154 / 257 |

## gamma

| scenario | policy | gamma=1.0 | gamma=0.98 | gamma=0.95 |
|---|---|---|---|---|
| no_shift | adaptive | 842 / 1448 | 834 / 1444 | 836 / 1434 |
| mild_shift | adaptive | 839 / 1461 | 830 / 1442 | 830 / 1414 |
| reversal | adaptive | 832 / 1430 | 819 / 1416 | 817 / 1418 |
| saturation | adaptive | 132 / 242 | 128 / 236 | 128 / 240 |

## B

| scenario | policy | B=64 | B=256 | B=1024 |
|---|---|---|---|---|
| no_shift | adaptive | 825 / 1421 | 834 / 1444 | 825 / 1430 |
| mild_shift | adaptive | 835 / 1433 | 830 / 1442 | 814 / 1410 |
| reversal | adaptive | 813 / 1410 | 819 / 1416 | 825 / 1436 |
| saturation | adaptive | 123 / 227 | 128 / 236 | 134 / 242 |
