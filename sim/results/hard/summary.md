# Stage 1 simulation results

R = 30 trials, T = 1,000,000 executions (= '4h'), K = 8, defaults gamma=0.98, B=256.

Cells: median [IQR] of cumulative successes. Regret = greedy-oracle expected successes - policy expected successes at 4h. Best-op share = fraction of executions on the operator with the highest *current* true rate.


## close_no_shift

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 120 [111-133] | 290 [268-299] | 506 [483-522] | 107 [91-120] | 0.33 / 0.45 / 0.47 | 0.00 / 0.00 / 0.00 | 0.18 / 0.07 / 0.04 |
| calib | 132 [115-141] | 295 [275-314] | 506 [481-527] | 97 [77-117] | 0.37 / 0.46 / 0.49 | 0.00 / 0.00 / 0.00 | 0.18 / 0.08 / 0.04 |
| shuffled | 122 [114-134] | 288 [279-308] | 507 [492-525] | 98 [88-111] | 0.39 / 0.46 / 0.50 | 0.00 / 0.00 / 0.00 | 0.29 / 0.09 / 0.04 |
| transfer | 132 [120-141] | 296 [284-309] | 517 [502-538] | 88 [78-109] | 0.38 / 0.46 / 0.49 | 1.00 / 1.00 / 1.00 | 0.42 / 0.10 / 0.04 |
| adaptive | 132 [118-141] | 300 [283-308] | 520 [500-547] | 92 [79-107] | 0.43 / 0.54 / 0.56 | 0.57 / 0.52 / 0.51 | 0.26 / 0.08 / 0.04 |
| mix50 | 126 [118-132] | 295 [283-312] | 519 [494-535] | 91 [84-108] | 0.39 / 0.51 / 0.54 | 0.50 / 0.50 / 0.50 | 0.30 / 0.08 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.62 | 0.535 |
| adaptive vs calib | 0.53 | 1 |
| adaptive vs shuffled | 0.57 | 1 |
| adaptive vs transfer | 0.50 | 1 |
| adaptive vs mix50 | 0.52 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.52 | 0.767 |
| transfer vs shuffled | 0.58 | 0.567 |
| transfer vs fresh | 0.62 | 0.351 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 126 [117-133] | 282 [267-308] | 501 [476-523] | 112 [87-124] | 0.33 / 0.42 / 0.45 | 0.00 / 0.00 / 0.00 | 0.51 / 0.22 / 0.12 |
| calib | 138 [130-151] | 304 [294-331] | 522 [489-555] | 80 [50-107] | 0.50 / 0.52 / 0.51 | 0.00 / 0.00 / 0.00 | 0.49 / 0.66 / 0.21 |
| shuffled | 126 [101-152] | 304 [235-330] | 510 [415-563] | 96 [36-165] | 0.45 / 0.49 / 0.49 | 0.00 / 0.00 / 0.00 | 0.67 / 0.85 / 0.54 |
| transfer | 148 [134-159] | 330 [310-342] | 552 [533-576] | 50 [35-66] | 0.57 / 0.56 / 0.55 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.91 |
| adaptive | 140 [130-147] | 312 [299-324] | 538 [524-560] | 66 [54-88] | 0.58 / 0.60 / 0.62 | 0.76 / 0.59 / 0.51 | 0.71 / 0.46 / 0.14 |
| mix50 | 136 [121-142] | 303 [281-324] | 530 [501-551] | 85 [69-105] | 0.45 / 0.53 / 0.55 | 0.50 / 0.50 / 0.50 | 0.74 / 0.34 / 0.14 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.80 | 0.000336 |
| adaptive vs calib | 0.56 | 0.451 |
| adaptive vs shuffled | 0.62 | 0.351 |
| adaptive vs transfer | 0.33 | 0.108 |
| adaptive vs mix50 | 0.62 | 0.351 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.69 | 0.0105 |
| transfer vs shuffled | 0.72 | 0.00636 |
| transfer vs fresh | 0.87 | 2.19e-06 |

## close_reversal

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.0015 0.0035 0.003  0.004  0.0025 0.001  0.0005 0.0002]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 116 [109-128] | 274 [268-298] | 495 [472-519] | 111 [101-127] | 0.30 / 0.40 / 0.44 | 0.00 / 0.00 / 0.00 | 0.19 / 0.06 / 0.04 |
| calib | 122 [114-132] | 288 [269-300] | 507 [491-522] | 98 [85-111] | 0.36 / 0.46 / 0.50 | 0.00 / 0.00 / 0.00 | 0.19 / 0.08 / 0.04 |
| shuffled | 125 [114-137] | 290 [273-303] | 512 [481-526] | 102 [86-117] | 0.36 / 0.44 / 0.47 | 0.00 / 0.00 / 0.00 | 0.31 / 0.08 / 0.04 |
| transfer | 126 [115-136] | 294 [280-306] | 508 [490-531] | 101 [87-113] | 0.36 / 0.46 / 0.48 | 1.00 / 1.00 / 1.00 | 0.43 / 0.09 / 0.04 |
| adaptive | 123 [113-136] | 286 [274-305] | 502 [490-522] | 101 [90-114] | 0.36 / 0.47 / 0.50 | 0.57 / 0.51 / 0.50 | 0.34 / 0.08 / 0.04 |
| mix50 | 122 [114-132] | 284 [276-300] | 502 [480-521] | 95 [86-112] | 0.39 / 0.53 / 0.55 | 0.51 / 0.50 / 0.50 | 0.29 / 0.07 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.60 | 0.811 |
| adaptive vs calib | 0.54 | 1 |
| adaptive vs shuffled | 0.50 | 1 |
| adaptive vs transfer | 0.46 | 1 |
| adaptive vs mix50 | 0.52 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.58 | 0.574 |
| transfer vs shuffled | 0.54 | 0.625 |
| transfer vs fresh | 0.63 | 0.263 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 19.6 [6.8-50.1], never: 6/30
- calib: 9.2 [2.7-142.2], never: 7/30
- shuffled: 15.1 [3.4-240.0], never: 9/30
- transfer: 8.7 [4.1-19.5], never: 5/30
- adaptive: 12.6 [3.8-30.3], never: 5/30
- mix50: 9.2 [5.2-18.2], never: 4/30

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 120 [110-130] | 278 [262-292] | 491 [482-514] | 102 [89-117] | 0.36 / 0.48 / 0.51 | 0.00 / 0.00 / 0.00 | 0.54 / 0.21 / 0.18 |
| calib | 136 [124-146] | 301 [284-340] | 516 [486-575] | 68 [46-108] | 0.52 / 0.56 / 0.55 | 0.00 / 0.00 / 0.00 | 0.56 / 0.61 / 0.27 |
| shuffled | 128 [113-138] | 288 [258-310] | 494 [436-530] | 117 [69-181] | 0.25 / 0.28 / 0.29 | 0.00 / 0.00 / 0.00 | 0.70 / 0.84 / 0.58 |
| transfer | 137 [132-152] | 313 [296-331] | 539 [519-558] | 72 [48-95] | 0.53 / 0.58 / 0.57 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.93 |
| adaptive | 124 [116-136] | 300 [276-318] | 526 [486-544] | 90 [75-120] | 0.39 / 0.49 / 0.51 | 0.64 / 0.57 / 0.50 | 0.79 / 0.38 / 0.15 |
| mix50 | 128 [120-134] | 296 [277-308] | 509 [479-533] | 102 [86-125] | 0.34 / 0.44 / 0.45 | 0.50 / 0.50 / 0.50 | 0.73 / 0.32 / 0.17 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.67 | 0.123 |
| adaptive vs calib | 0.42 | 0.802 |
| adaptive vs shuffled | 0.58 | 0.802 |
| adaptive vs transfer | 0.33 | 0.123 |
| adaptive vs mix50 | 0.54 | 0.802 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.58 | 0.311 |
| transfer vs shuffled | 0.72 | 0.00577 |
| transfer vs fresh | 0.83 | 3.84e-05 |

Recovery: minutes until the 20-batch rolling best-op share reaches 50% (median [IQR]; never = count of trials that never do):

- fresh: 9.0 [4.9-90.9], never: 6/30
- calib: 4.2 [2.4-185.6], never: 8/30
- shuffled: 240.0 [4.2-240.0], never: 19/30
- transfer: 3.6 [2.3-10.4], never: 5/30
- adaptive: 6.9 [2.9-187.5], never: 8/30
- mix50: 12.4 [5.5-240.0], never: 9/30

## late_riser

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0015 0.0015 0.001  0.0005 0.0002]  
tau (fraction of T): [0.05 0.05 0.05 0.5  0.05 0.05 0.05 0.05]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 130 [117-136] | 302 [282-318] | 628 [607-650] | 273 [252-306] | 0.34 / 0.21 / 0.38 | 0.00 / 0.00 / 0.00 | 0.19 / 0.06 / 0.04 |
| calib | 122 [116-135] | 303 [286-319] | 628 [593-645] | 286 [256-309] | 0.40 / 0.21 / 0.34 | 0.00 / 0.00 / 0.00 | 0.19 / 0.08 / 0.04 |
| shuffled | 121 [109-132] | 306 [282-320] | 641 [589-666] | 270 [246-312] | 0.34 / 0.23 / 0.37 | 0.00 / 0.00 / 0.00 | 0.30 / 0.08 / 0.04 |
| transfer | 123 [113-132] | 299 [286-308] | 636 [586-654] | 282 [247-302] | 0.37 / 0.20 / 0.38 | 1.00 / 1.00 / 1.00 | 0.42 / 0.10 / 0.05 |
| adaptive | 124 [115-137] | 302 [287-327] | 646 [602-664] | 277 [253-319] | 0.39 / 0.22 / 0.34 | 0.58 / 0.52 / 0.50 | 0.30 / 0.08 / 0.04 |
| mix50 | 120 [113-132] | 306 [278-320] | 632 [605-656] | 277 [242-304] | 0.39 / 0.22 / 0.38 | 0.50 / 0.50 / 0.50 | 0.28 / 0.08 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.56 | 1 |
| adaptive vs calib | 0.55 | 1 |
| adaptive vs shuffled | 0.54 | 1 |
| adaptive vs transfer | 0.58 | 1 |
| adaptive vs mix50 | 0.54 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.46 | 1 |
| transfer vs shuffled | 0.45 | 1 |
| transfer vs fresh | 0.46 | 1 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 124 [114-129] | 301 [286-314] | 631 [599-658] | 273 [245-307] | 0.39 / 0.23 / 0.38 | 0.00 / 0.00 / 0.00 | 0.53 / 0.23 / 0.12 |
| calib | 132 [124-141] | 305 [294-323] | 622 [580-651] | 279 [266-309] | 0.48 / 0.21 / 0.30 | 0.00 / 0.00 / 0.00 | 0.53 / 0.61 / 0.19 |
| shuffled | 134 [108-150] | 316 [268-336] | 634 [609-667] | 274 [249-316] | 0.35 / 0.20 / 0.36 | 0.00 / 0.00 / 0.00 | 0.70 / 0.84 / 0.58 |
| transfer | 152 [139-160] | 342 [324-353] | 634 [604-658] | 276 [237-297] | 0.68 / 0.25 / 0.23 | 1.00 / 1.00 / 1.00 | 0.97 / 1.00 / 0.91 |
| adaptive | 135 [130-147] | 310 [299-324] | 614 [567-646] | 287 [272-311] | 0.50 / 0.20 / 0.27 | 0.75 / 0.57 / 0.49 | 0.76 / 0.48 / 0.16 |
| mix50 | 128 [117-136] | 304 [290-318] | 634 [610-646] | 274 [258-306] | 0.46 / 0.21 / 0.33 | 0.50 / 0.50 / 0.50 | 0.72 / 0.33 / 0.16 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.65 | 0.159 |
| adaptive vs calib | 0.56 | 0.987 |
| adaptive vs shuffled | 0.53 | 0.987 |
| adaptive vs transfer | 0.21 | 0.000445 |
| adaptive vs mix50 | 0.57 | 0.987 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.84 | 1.3e-05 |
| transfer vs shuffled | 0.74 | 0.00159 |
| transfer vs fresh | 0.89 | 4.95e-07 |

## depletion

**old** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
**new** theta: [0.004  0.0035 0.003  0.0025 0.0015 0.001  0.0005 0.0002]  
pool (successes): [ 30. 400. 400. 400. 300. 200. 100.  50.]


### N = 500

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 101 [93-109] | 223 [209-236] | 356 [338-372] | 48 [42-52] | 0.27 / 0.27 / 0.24 | 0.00 / 0.00 / 0.00 | 0.20 / 0.06 / 0.04 |
| calib | 98 [88-107] | 216 [200-226] | 350 [334-363] | 47 [35-55] | 0.21 / 0.27 / 0.24 | 0.00 / 0.00 / 0.00 | 0.19 / 0.07 / 0.04 |
| shuffled | 104 [97-112] | 216 [208-227] | 352 [340-361] | 44 [37-52] | 0.25 / 0.24 / 0.20 | 0.00 / 0.00 / 0.00 | 0.33 / 0.07 / 0.04 |
| transfer | 102 [92-111] | 222 [204-228] | 358 [343-366] | 43 [35-55] | 0.26 / 0.26 / 0.23 | 1.00 / 1.00 / 1.00 | 0.45 / 0.08 / 0.05 |
| adaptive | 100 [90-108] | 220 [211-235] | 360 [346-374] | 44 [34-51] | 0.26 / 0.29 / 0.25 | 0.54 / 0.50 / 0.49 | 0.34 / 0.07 / 0.04 |
| mix50 | 104 [100-112] | 226 [212-234] | 354 [343-363] | 41 [34-47] | 0.29 / 0.30 / 0.23 | 0.50 / 0.50 / 0.50 | 0.32 / 0.07 / 0.04 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.47 | 1 |
| adaptive vs calib | 0.60 | 0.833 |
| adaptive vs shuffled | 0.59 | 1 |
| adaptive vs transfer | 0.56 | 1 |
| adaptive vs mix50 | 0.45 | 1 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.54 | 1 |
| transfer vs shuffled | 0.51 | 1 |
| transfer vs fresh | 0.42 | 0.829 |

### N = 5000

| policy | 15m | 1h | 4h | regret@4h | best-op share (0-15m / 15m-1h / 1h-4h) | share T (same windows) | TV F vs T after batch 1 / 15m / 1h |
|---|---|---|---|---|---|---|---|
| fresh | 102 [98-110] | 218 [214-226] | 354 [342-363] | 47 [38-53] | 0.24 / 0.27 / 0.24 | 0.00 / 0.00 / 0.00 | 0.53 / 0.22 / 0.18 |
| calib | 103 [95-107] | 216 [202-227] | 338 [322-358] | 55 [44-66] | 0.22 / 0.18 / 0.18 | 0.00 / 0.00 / 0.00 | 0.53 / 0.42 / 0.20 |
| shuffled | 98 [82-108] | 209 [191-222] | 336 [309-348] | 54 [44-74] | 0.05 / 0.10 / 0.10 | 0.00 / 0.00 / 0.00 | 0.69 / 0.75 / 0.45 |
| transfer | 111 [100-126] | 232 [214-245] | 358 [339-370] | 44 [34-56] | 0.33 / 0.27 / 0.21 | 1.00 / 1.00 / 1.00 | 0.98 / 1.00 / 0.74 |
| adaptive | 94 [86-106] | 210 [196-225] | 348 [328-361] | 53 [36-58] | 0.26 / 0.28 / 0.25 | 0.70 / 0.54 / 0.50 | 0.79 / 0.38 / 0.16 |
| mix50 | 100 [89-107] | 217 [206-229] | 356 [341-366] | 48 [41-55] | 0.27 / 0.27 / 0.23 | 0.50 / 0.50 / 0.50 | 0.76 / 0.30 / 0.15 |

Adaptive vs others, successes at 1h (two-sided MWU, Holm within table; A12 = P(adaptive > other)):

| comparison | A12 | p (Holm) |
|---|---|---|
| adaptive vs fresh | 0.38 | 0.461 |
| adaptive vs calib | 0.45 | 0.851 |
| adaptive vs shuffled | 0.57 | 0.851 |
| adaptive vs transfer | 0.28 | 0.0144 |
| adaptive vs mix50 | 0.42 | 0.851 |

Transfer vs prior controls at 1h (does the old *ranking* matter?):

| comparison | A12 | p (Holm) |
|---|---|---|
| transfer vs calib | 0.70 | 0.0136 |
| transfer vs shuffled | 0.80 | 0.000172 |
| transfer vs fresh | 0.69 | 0.0136 |

# Sensitivity (median successes at 1h / 4h)


## gamma

| scenario | policy | gamma=1.0 | gamma=0.98 | gamma=0.95 |
|---|---|---|---|---|
| close_no_shift | adaptive (N=500) | 300 / 514 | 300 / 520 | 288 / 500 |
| close_no_shift | adaptive (N=5000) | 320 / 548 | 312 / 538 | 307 / 532 |
| close_reversal | adaptive (N=500) | 299 / 510 | 286 / 502 | 292 / 512 |
| close_reversal | adaptive (N=5000) | 306 / 524 | 300 / 526 | 290 / 498 |
| late_riser | adaptive (N=500) | 305 / 647 | 302 / 646 | 300 / 627 |
| late_riser | adaptive (N=5000) | 330 / 640 | 310 / 614 | 314 / 632 |
| depletion | adaptive (N=500) | 222 / 356 | 220 / 360 | 220 / 358 |
| depletion | adaptive (N=5000) | 218 / 348 | 210 / 348 | 216 / 350 |
