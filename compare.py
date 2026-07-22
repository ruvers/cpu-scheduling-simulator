# Algoritma karsilastirma modulu
# Tum zamanlama algoritmalarini calistirir ve sonuclari karsilastirir

import copy
from algorithms import ALGORITHMS
from utils.parser import load_process_file
from utils.statistics import calculate_metrics


def benchmark_all(proc_data, quantum=3):
    """
    Tum algoritmalari calistirir ve sonuclari toplar

    Parametreler:
        proc_data: Proses listesi
        quantum: Round Robin icin zaman dilimi

    Dondurur:
        Algoritma sonuclarinin listesi
    """
    benchmark_data = []

    # Her algortimayi sirayla calistir
    for algo_name, algo_config in ALGORITHMS.items():
        handler = algo_config["func"]

        # Her algoritma icin taze kopya kullan
        # Bu kritik - algoritma orijinal veriyi degistirmemeli
        fresh_procs = copy.deepcopy(proc_data)

        # Algortimayi calistir
        if algo_config["needs_quantum"]:
            output = handler(fresh_procs, quantum)
            label = f"{algo_name}(q={quantum})"
        else:
            output = handler(fresh_procs)
            label = algo_name

        # Istatistikleri hesapla
        _, avg_values = calculate_metrics(output["processes"])

        # Sonuclari kaydet
        benchmark_data.append({
            "algorithm": label,
            "avg_waiting": avg_values["avg_waiting"],
            "avg_turnaround": avg_values["avg_turnaround"],
            "avg_response": avg_values["avg_response"],
            "context_switches": output["context_switches"]
        })

    return benchmark_data


def show_comparison(benchmark_data):
    """
    Karsilastirma tablosunu yazdirir

    Parametreler:
        benchmark_data: Algoritma sonuclari listesi
    """
    print("\nAlgorithm Comparison Table\n")
    print(f"{'Algorithm':<12} {'WT':>8} {'TAT':>8} {'RT':>8} {'CS':>8}")
    print("-" * 55)

    # Her algoritma icin satir yazdir
    for r in benchmark_data:
        print(
            f"{r['algorithm']:<12} "
            f"{r['avg_waiting']:>8.2f} "
            f"{r['avg_turnaround']:>8.2f} "
            f"{r['avg_response']:>8.2f} "
            f"{r['context_switches']:>8}"
        )


if __name__ == "__main__":
    # Proses dosyasini oku
    proc_data = load_process_file("processes.txt")

    # Tum algoritmalari calistir
    benchmark_data = benchmark_all(proc_data, quantum=3)

    # Karsilastirma tablosunu yazdir
    show_comparison(benchmark_data)
