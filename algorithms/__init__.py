# Zamanlama algoritmalari paketi
# Bu modul tum CPU zamanlama algoritmalarini icerir

from algorithms.fcfs import first_come_first_serve
from algorithms.sjf import shortest_job_first
from algorithms.srtf import shortest_remaining_first
from algorithms.rr import circular_queue_scheduler
from algorithms.priority_np import priority_nonpreemptive
from algorithms.priority_p import priority_preemptive

# Algoritma kayit defteri - komut satirindan secim icin
ALGORITHMS = {
    "FCFS": {"func": first_come_first_serve, "needs_quantum": False},
    "SJF": {"func": shortest_job_first, "needs_quantum": False},
    "SRTF": {"func": shortest_remaining_first, "needs_quantum": False},
    "RR": {"func": circular_queue_scheduler, "needs_quantum": True},
    "PRIO_NP": {"func": priority_nonpreemptive, "needs_quantum": False},
    "PRIO_P": {"func": priority_preemptive, "needs_quantum": False},
}

