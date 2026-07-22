# Istatistik hesaplama modulu
# Proses performans metriklerini hesaplar

# Formüller:
# Turnaround Time (TAT) = Completion Time - Arrival Time
# Waiting Time (WT) = Turnaround Time - Burst Time
# Response Time (RT) = Start Time - Arrival Time


def calculate_metrics(proc_data):
    """
    Proses istatistiklerini ve ortalamalari hesaplar

    Parametreler:
        proc_data: Tamamlanmis proses listesi
                   Her proses start_time ve completion_time icermeli

    Dondurur:
        (metrics, avg_values) tuple'i
        - metrics: Her proses icin detayli istatistikler
        - avg_values: Ortalama degerler
    """
    sum_wt = 0
    sum_tat = 0
    sum_rt = 0

    metrics = []

    # Her proses icin metrikleri hesapla
    for p in proc_data:
        arrival = p["arrival"]
        burst = p["burst"]
        start = p["start_time"]
        completion = p["completion_time"]

        # Temel metrikleri hesapla
        turnaround = completion - arrival
        waiting = turnaround - burst
        response = start - arrival

        # Toplamlara ekle
        sum_wt += waiting
        sum_tat += turnaround
        sum_rt += response

        # Proses metriklerini kaydet
        metrics.append({
            "pid": p["pid"],
            "arrival": arrival,
            "burst": burst,
            "completion": completion,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response
        })

    # Proses sayisi
    n = len(proc_data)

    # Ortalama degerleri hesapla
    avg_values = {
        "avg_waiting": sum_wt / n,
        "avg_turnaround": sum_tat / n,
        "avg_response": sum_rt / n
    }

    return metrics, avg_values
