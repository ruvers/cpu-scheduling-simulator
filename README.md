# CPU Scheduling Simulator

Python simulator for six operating-system CPU scheduling algorithms with Gantt charts, execution logs, and performance comparison.

**Stack:** Python 3, Matplotlib  
**Course:** CENG 301 — Operating Systems

## Features

- FCFS, SJF, SRTF, Round Robin, Priority (preemptive & non-preemptive)
- ASCII Gantt charts and per-process statistics
- Side-by-side algorithm comparison and Matplotlib plots

## Run

```bash
pip install -r requirements.txt
python scheduler.py --input processes.txt --algo SRTF
python compare.py
python algorithms_plot.py
```

## Input format

```
# pid arrival_time burst_time priority
P1 0 8 2
P2 1 4 1
```
