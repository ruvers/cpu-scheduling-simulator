# Ana zamanlayici modulu
# Komut satiri arayuzu ile zamanlama algoritmalarini calistirir

import argparse

from algorithms import ALGORITHMS
from utils.parser import load_process_file
from utils.statistics import calculate_metrics
from utils.gantt import display_gantt


def execute_algorithm(algo_name, proc_data, quantum=None):
    """
    Secilen zamanlama algoritmasini calistirir

    Parametreler:
        algo_name: Algoritma adi (FCFS, SJF, SRTF, RR, PRIO_NP, PRIO_P)
        proc_data: Proses listesi
        quantum: Zaman dilimi (sadece RR icin gerekli)

    Dondurur:
        Algoritma sonuc sozlugu
    """
    # Algoritma kontrolu
    if algo_name not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algo_name}")

    algo_config = ALGORITHMS[algo_name]
    algo_handler = algo_config["func"]

    # Quantum gerekliligi kontrolu
    if algo_config["needs_quantum"]:
        if quantum is None:
            raise ValueError(f"{algo_name} requires a quantum value")
        return algo_handler(proc_data, quantum)

    return algo_handler(proc_data)


def get_cli_args():
    """
    Komut satiri argumanlarini ayristirir

    Argumanlar:
        --input: Proses dosyasi yolu (zorunlu)
        --algo: Zamanlama algoritmasi (zorunlu)
        --quantum: Zaman dilimi (RR icin zorunlu)
    """
    parser = argparse.ArgumentParser(
        description="CPU Scheduling Simulator"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to process input file"
    )

    parser.add_argument(
        "--algo",
        required=True,
        choices=ALGORITHMS.keys(),
        help="Scheduling algorithm"
    )

    parser.add_argument(
        "--quantum",
        type=int,
        help="Time quantum (required for RR)"
    )

    return parser.parse_args()


def main():
    """
    Ana calistirma fonksiyonu
    Proses dosyasini okur, algortimayi calistirir ve sonuclari yazdirir
    """
    args = get_cli_args()

    # Proses dosyasini oku
    proc_data = load_process_file(args.input)

    # Secilen algortimayi calistir
    result = execute_algorithm(
        algo_name=args.algo,
        proc_data=proc_data,
        quantum=args.quantum
    )

    # Sonuclari ayikla
    execution_timeline = result["timeline"]
    completed_procs = result["processes"]
    switch_count = result["context_switches"]

    # Gantt semasini yazdir
    print("\n" + "=" * 50)
    print("GANTT CHART")
    print("=" * 50)
    display_gantt(execution_timeline)

    # Olay kayitlarini yazdir
    print("\n" + "-" * 50)
    print("EXECUTION LOG")
    print("-" * 50)
    for entry in result["log"]:
        print(f"  {entry}")

    # Istatistikleri hesapla
    metrics, avg_values = calculate_metrics(completed_procs)

    # Proses istatistiklerini yazdir
    print("\n" + "-" * 50)
    print("PROCESS STATISTICS")
    print("-" * 50)
    print("PID    AT    BT    CT   TAT    WT    RT")
    print("-" * 42)
    for s in metrics:
        print(
            f"{s['pid']:>3}  "
            f"{s['arrival']:>4}  "
            f"{s['burst']:>4}  "
            f"{s['completion']:>4}  "
            f"{s['turnaround']:>4}  "
            f"{s['waiting']:>4}  "
            f"{s['response']:>4}"
        )

    # Ortalamalari yazdir
    print("\n" + "-" * 50)
    print("SUMMARY")
    print("-" * 50)
    print(f"  Avg Turnaround Time : {avg_values['avg_turnaround']:.2f}")
    print(f"  Avg Waiting Time    : {avg_values['avg_waiting']:.2f}")
    print(f"  Avg Response Time   : {avg_values['avg_response']:.2f}")
    print(f"  Context Switches    : {switch_count}")
    print("=" * 50)


if __name__ == "__main__":
    main()
