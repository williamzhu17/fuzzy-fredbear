#!/bin/bash
# Stage 1 follow-up runs (README runs 6-10; run 5 is in the README). Run from sim/: bash run_next.sh
set -e
PY=${PY:-../.venv/bin/python}
SC=no_shift,mild_shift,reversal,saturation,close_no_shift,close_reversal,late_riser,depletion
# Run 6: rank-correlation sweep (6 draws at level 0.5, 3 draws at levels 1 and 0.2)
$PY rank_sweep.py --level 0.5 --draws 6 --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --out results/rank_L0.5 > /dev/null
for L in 1 0.2; do
  $PY rank_sweep.py --level $L --draws 3 --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --out results/rank_L$L > /dev/null
done
# Run 7: finer N sweep at each level
for L in 1 0.5 0.2; do
  $PY run_stage1.py --scenarios $SC --Ns 1000,2000,5000,20000 --sweeps "" --policies calib,transfer,bmcs_cal,bmcs_cal_r \
      --focus bmcs_cal_r --level $L --out results/nsweep_L$L > /dev/null
done
# Run 8: power check source data (R=200) at level 0.5
$PY run_stage1.py --R 200 --scenarios no_shift,reversal,saturation,close_no_shift,close_reversal --Ns 5000 --sweeps "" \
    --policies fresh,calib,transfer,bmcs_cal,bmcs_cal_r --focus bmcs_cal_r --level 0.5 --out results/power_L0.5 > /dev/null
# Run 9: matched (rescaled) 50/50 control
for L in 1 0.5 0.2; do
  $PY run_stage1.py --scenarios $SC --Ns 5000 --sweeps "" --policies fresh,calib,transfer,mix50_cal,mix50_cal_r,bmcs_cal_r \
      --focus bmcs_cal_r --level $L --out results/mix_L$L > /dev/null
done
# Run 10: consolidated final sweep (~90 min) and its report
mkdir -p results/final
$PY final_sweep.py --out results/final > results/final/run.log 2>&1
$PY final_report.py results/final --reps 2000 > /dev/null
echo done
