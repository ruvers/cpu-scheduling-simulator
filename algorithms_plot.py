# Grafik olusturma modulu
# Algoritma performanslarini gorsel olarak karsilastirir

import os
import copy
import matplotlib.pyplot as plt
from algorithms import ALGORITHMS
from utils.parser import load_process_file
from utils.statistics import calculate_metrics


def create_charts(proc_data, quantum=3):
    """
    Algoritma karsilastirma grafiklerini olusturur

    Parametreler:
        proc_data: Proses listesi
        quantum: Round Robin icin zaman dilimi

    Olusturulan dosyalar:
        graphs/waiting.png - Ortalama bekleme suresi grafigi
        graphs/turnaround.png - Ortalama donus suresi grafigi
    """
    labels = []
    waiting_times = []
    turnaround_times = []

    # Grafik klasorunu olustur
    os.makedirs("graphs", exist_ok=True)

    # Her algortimayi calistir ve sonuclari topla
    for algo_name, algo_config in ALGORITHMS.items():
        handler = algo_config["func"]
        fresh_procs = copy.deepcopy(proc_data)

        # Algortimayi calistir
        if algo_config["needs_quantum"]:
            output = handler(fresh_procs, quantum)
            label = f"{algo_name}(q={quantum})"
        else:
            output = handler(fresh_procs)
            label = algo_name

        # Metrikleri hesapla
        _, avg_values = calculate_metrics(output["processes"])

        # Sonuclari kaydet
        labels.append(label)
        waiting_times.append(avg_values["avg_waiting"])
        turnaround_times.append(avg_values["avg_turnaround"])

    # Ortalama Bekleme Suresi grafigi
    plt.figure()
    plt.bar(labels, waiting_times)
    plt.xlabel("Algorithm")
    plt.ylabel("Average Waiting Time")
    plt.title("Average Waiting Time vs Algorithm")
    plt.tight_layout()
    plt.savefig("graphs/waiting.png")
    plt.close()

    # Ortalama Donus Suresi grafigi
    plt.figure()
    plt.bar(labels, turnaround_times)
    plt.xlabel("Algorithm")
    plt.ylabel("Average Turnaround Time")
    plt.title("Average Turnaround Time vs Algorithm")
    plt.tight_layout()
    plt.savefig("graphs/turnaround.png")
    plt.close()


if __name__ == "__main__":
    # Proses dosyasini oku
    proc_data = load_process_file("processes.txt")

    # Grafikleri olustur
    create_charts(proc_data, quantum=3)
